import hashlib
import logging
import sys
import requests

from ecdsa import NIST256p, VerifyingKey
from server import db
from server import utils
from server.config import BLOCKCHAIN_NETOWRK
from server.models import Block
from server.models import Transaction
from server.p2p_manager import P2PManager
from server import config

# 시스템 운영 시 필요한 로그 메시지 출력을 위한 설정
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class Transfer:
    '''거래 담당 클래스'''
    def __init__(
        self,
        # send_private_key: str,
        send_public_key: str,
        send_blockchain_addr: str,
        recv_blockchain_addr: str,
        amount: float,
        signature: str = None
    ) -> None:
        self.send_public_key = send_public_key
        self.send_blockchain_addr = send_blockchain_addr
        self.recv_blockchain_addr = recv_blockchain_addr
        self.amount = amount
        self.block_id =  Block.query.filter(
            Block.timestamp,).order_by(Block.timestamp.desc()).first().id
        self.signature = signature


    def commit_transaction(self) -> None:
        '''Commit transaction into DB'''
        transaction = Transaction(
            block_id=self.block_id,
            send_addr=self.send_blockchain_addr,
            recv_addr=self.recv_blockchain_addr,
            amount=float(self.amount)
        )
        db.session.add(transaction)
        db.session.commit()


    def add_transaction(self) -> bool:
        '''Add a transaction into DB'''
        transaction = utils.sorted_dict_by_key(
            {
                'send_blockchain_addr': self.send_blockchain_addr,
                'recv_blockchain_addr': self.recv_blockchain_addr,
                'amount': float(self.amount),
            }
        )
        # 마이닝(채굴)하는 사람은 검증없이 transaction pool에 추가
        if self.send_blockchain_addr == BLOCKCHAIN_NETOWRK:
            self.commit_transaction()
            return True

        # transaction 검증 과정
        is_verified = self.verify_transaction_signature(
            self.send_public_key,
            self.signature,
            transaction
        )

        # 검증을 통과하면 DB에 추가
        if is_verified:
            self.commit_transaction()
            return True
        return False


    def create_transaction(self) -> bool:
        '''트랜잭션을 새로 만들고 블록체인 네트워크와 동기화'''
        is_transacted = self.add_transaction()

        # Todo: 트랜잭션이 추가되면, 이웃 노드에게 트랜잭션 정보를 전달
        p2p_manager = P2PManager()
        active_neighbors = p2p_manager.get_all_active_nodes()
        active_neighbors = set([node.ip for node in active_neighbors])
        # active_neighbors = utils.get_neighbor_ips()
        for neighbor in active_neighbors:
            url = f'http://{neighbor}:{config.PORT_BLOCKCHAIN}/transactions/'
            print(f'url: {url}')
            try:
                # 업데이트 요청: put request
                requests.put(
                    url=url,
                    json={
                        'send_public_key': self.send_public_key,
                        'send_blockchain_addr': self.send_blockchain_addr,
                        'recv_blockchain_addr': self.recv_blockchain_addr,
                        'amount': self.amount,
                        'signature': self.signature,
                    }
                )
            except Exception as e:
                print(f'Error: {e}')
                pass
        return is_transacted


    def verify_transaction_signature(
        self,
        send_public_key: str,
        singature: str,
        transaction: dict
    ) -> bool:
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        singature_bytes = bytes().fromhex(singature)
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(send_public_key), curve=NIST256p
        )
        is_verified = verifying_key.verify(
            signature=singature_bytes,
            data=message,
        )
        return is_verified


if __name__=='__main__':
    '''모듈 테스트'''
    pass