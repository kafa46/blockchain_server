import logging
import sys
import time
from typing import List, Union # blockcain timestamp 생성
import json
import hashlib

import requests

from server import utils
from server import db
from server.models import Block, Transaction
from ecdsa import VerifyingKey
from ecdsa import NIST256p
from server.p2p_manager import P2PManager
from server import config

# 시스템 운영 시 필요한 로그 메시지 출력을 위한 설정
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

# MINING_DIFICULTY = 3
# MINING_SENDER = 'BLOCK CHAIN NETWORK'
# MINING_REWARD = 1.0


class BlockChain:
    '''블록체인 클래스'''
    def __init__(self, port: Union[int, str] = None, ) -> None:
        self.port = int(port)

    def create_genesis_block(self,) -> bool:
        '''Genesis Block 생성'''
        block_exist = Block.query.all()
        if block_exist:
            logger.warning({
                'status': 'Fail to create genesis block',
                'error': 'Block(s) aleady exist'
            })
            return False

        genesis_block = Block(
            prev_hash=utils.hash({}),
            nonce=0,
            timestamp=time.time(),
        )
        db.session.add(genesis_block)
        db.session.commit()

        return True


    def valid_proof(
        self,
        transactions: list,
        prev_hash: str,
        nonce: int) -> int:
        '''Difficult 개수만큼 0 일치하는지 검사하는 함수
            Mining 클래스에도 동일하게 존재(코드 중복)
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
        return guess_hash[:config.MINING_DIFFICULTY] == '0' * config.MINING_DIFFICULTY



    def create_block(self, nonce:int, prev_hash:str=None):
        '''블록체인에서의 새로운 단위 블록 생성'''
        try:
            db.session.add(
                Block(
                    prev_hash=prev_hash,
                    nonce=nonce,
                    timestamp=time.time(),
                )
            )
            db.session.commit()
            # 블록이 생성되었으므로 이웃 노드들에게 Transaction 초기화 하라고 요청
            # DB를 사용할 경우는 불필요
            #   -> 개별 block과 transaction은 Foreign Key 연결
            # p2p_manager = P2PManager()
            # active_neighbors = p2p_manager.get_all_active_nodes()
            # active_neighbors = p2p_manager.get_all_active_nodes()
            # active_neighbors = set([node.ip for node in active_neighbors])
            # for neighbor in active_neighbors:
            #     try:
            #         url = f'http://{neighbor}:{config.PORT_BLOCKCHAIN}/transactions/'
            #         requests.delete(
            #             url=url,
            #         )
            #     except Exception as e:
            #         print('Error: {e}')
            return True
        except Exception as e:
            print('Fail to block on database')
            print(f'Error: {e}')
            return False


    def valid_chain(self, chain: List[dict]) -> bool:
        '''블록체인이 올바른지 검증(valid)하여 True/False 리턴'''
        for idx, block in enumerate(chain):
            if idx == 0:
                prev_block = block
                continue
            if block['prev_hash'] != utils.hash(prev_block):
                return False
            valid_success = self.valid_proof(
                transactions=block['transactions'],
                prev_hash=block['prev_hash'],
                nonce=block['nonce'],
            )
            if not valid_success:
                return False
            prev_block = block
        return True


    def resove_conflicts(self,) -> bool:
        '''블록체인의 길이를 비교하여 업데이트'''
        longest_chain = None

        # 자신의 체인을 가장 긴 체인으로 설정
        my_chain = utils.get_blockchain()['chain']
        max_length = len(my_chain)

        p2p_manager = P2PManager()
        active_neighbors = p2p_manager.get_all_active_nodes()
        active_neighbors = set([node.ip for node in active_neighbors])
        for node_ip in active_neighbors:
            try:
                response = requests.get(f'http://{node_ip}:{config.PORT_BLOCKCHAIN}/chain')
                if response.status_code == 200:
                    blockchain = response.json
                    chain = blockchain['chain']
                    chain_length = len(chain)
                    if chain_length > max_length and self.valid_chain(chain):
                        max_length = chain_length
                        longest_chain = chain
            except Exception as e:
                print(f'Error: {e}')
                continue

        if longest_chain:
            '''내 데이터베이스를 longest chain으로 갈아치우기'''
            # DB의 모든 block 삭제
            blocks = Block.query.all()
            for block in blocks:
                db.session.delete(block)
                db.session.commit()

            # DB의 모든 transaction 삭제
            transactions = Transaction.query.all()
            for transaction in transactions:
                db.session.delete(transaction)
                db.session.commit()

            # 새로운 블록체인 생성
            for block in longest_chain:
                # 블록 생성
                block = Block(
                    prev_hash = block['prev_hash'],
                    nonce = block['nonce'],
                    timestamp = block['timestamp'],
                )
                db.session.add(block)
                db.session.commit()
                # 해당 블록의 transaction 정보 생성
                for transaction in block['transactions']:
                    transaction = Transaction(
                        block_id=block.id,
                        send_addr=transaction['send_blockchain_addr'],
                        recv_addr=transaction['recv_blockchain_addr'],
                        amount=transaction['amount'],
                    )
                    db.session.add(transaction)
                    db.session.commit()
            logger.info({
                'action': 'resolve_conflicts',
                'status': 'replaced'
            })

            return True


if __name__=='__main__':
    pass

