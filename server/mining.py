import contextlib
import logging
import sys
import threading
from typing import Tuple

import requests
from server import utils
from server.transfer import Transfer
from server.config import (
    BLOCKCHAIN_NETOWRK,
    MINING_DIFFICULTY,
    MINING_REWARD,
)
from server import config
from server.blockchain import BlockChain
from server.p2p_manager import P2PManager

# 시스템 운영 시 필요한 로그 메시지 출력을 위한 설정
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class Mine:
    '''블록체인 채굴(mining) 클래스'''
    def __init__(
        self,
        difficulty: int = MINING_DIFFICULTY, # 채굴 난이도
        reward: float = MINING_REWARD, # 채굴 보상금
    ) -> None:
        self.difficulty = difficulty
        self.reward = reward
        self.semaphore = threading.Semaphore(1)


    def valid_proof(
        self,
        transactions: list,
        prev_hash: str,
        nonce: int) -> int:
        '''Difficult 개수만큼 0 일치하는지 검사하는 함수
            Blockchain 클래스에도 동일하게 존재(코드 중복)
            -> 리팩토링 과정에서 utils.py로 이동할 것을 고려(코드 중복)
        '''
        guess_block = utils.sorted_dict_by_key(
            {
                'transactions': transactions,
                'nonce': nonce,
                'prev_hash': prev_hash,
            }
        )
        guess_hash = utils.hash(guess_block)
        # Difficulty 개수만큼 일치하면 True, 틀리면 False
        return guess_hash[:self.difficulty] == '0' * self.difficulty


    def proof_of_work(self) -> int:
        # 마지막 블록 추출
        transaction_pool = utils.get_blockchain().get('transaction_pool')
        prev_hash = utils.get_prev_hash()

        # 마이닝 시작: 챌린지 0부터
        nonce: int = 0
        while self.valid_proof(transaction_pool, prev_hash, nonce) is False:
            nonce += 1
        return nonce


    def mining(self, recv_blockcain_addr) -> Tuple[bool, str]:
        '''마이닝 수행 -> 성공 여부(True/False) 리턴'''
        block_chain = utils.get_blockchain()
        transaction_pool = block_chain.get('transaction_pool')

        if not transaction_pool:
            return (False, '실패! 마이닝 할 거래 내역이 없습니다.')

        transfer = Transfer(
            send_public_key='',
            send_blockchain_addr=BLOCKCHAIN_NETOWRK,
            recv_blockchain_addr=recv_blockcain_addr,
            amount=self.reward
        )
        transfer.add_transaction()
        nonce = self.proof_of_work()

        prev_block = block_chain.get('chain')[-1]
        prev_hash = utils.hash(utils.sorted_dict_by_key(prev_block))
        block_chain_obj = BlockChain(utils.get_current_port_number())
        block_chain_obj.create_block(
            nonce=nonce,
            prev_hash=prev_hash
        )

        # 채굴에 성공하면 이웃 노드에게 resolve_conflicts 실행하도록 요청
        p2p_manager = P2PManager()
        active_neighbors = p2p_manager.get_all_active_nodes()
        active_neighbors = set([node.ip for node in active_neighbors])
        for node_ip in active_neighbors:
            try:
                requests.put(f'http://{node_ip}:{config.PORT_BLOCKCHAIN}/resolve_conflicts')
            except Exception as e:
                print(f'Error: {e}')
                continue

        return (True, 'success')


    def start_mining(self,) -> None:
        '''세마포를 이용하여 지속적으로 마이닝 반복'''
        acquire_success = self.semaphore.acquire(blocking=False)
        if acquire_success:
            with contextlib.ExitStack() as stack:
                stack.callback(self.semaphore.release)
                self.mining()
                loop = threading.Timer(30, self.start_mining)
                loop.start()
