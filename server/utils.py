from datetime import datetime
import hashlib
import json
import socket
import logging
import collections

from server.blockchain import BlockChain
from server.models import Block, Transaction
from server.wallet import Wallet
# from server.p2p_manager import P2PManager
# from server import db


def print_blockchain(chains):
    '''블록체인 보기좋게 출력'''
    for idx, chain in enumerate(chains):
        print(f"\n\n{'===' * 5} Blockchain {idx} {'===' * 5}")
        for k, v in chain.items():
            print(f'{k:15}{v}')
        print(f"{'***' * 3} End of blockchain {idx} {'***' * 3}")


def sorted_dict_by_key(unsorted_dict: dict):
    '''사전(dict)은 원소의 순서가 보장되지 않음
        -> 같은 사전이라도 순서가 달라지면 hash 값은 엄청난 차이
        -> 사전의 key 값에 따라 일정하게 정렬하여
           동일한 dict은 동일한 hash 값을 보장
    '''
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda keys: keys[0])
    )


def get_current_port_number() -> int:
    '''현재 Flask가 사용중인 Port 번호 리턴'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    return int(port)


def get_current_ip_addr() -> str:
    '''현재 서버의 IP 주소 리턴'''
    host_name = socket.gethostname()
    print(f'host_name: {host_name}')
    ip_addr = socket.gethostbyname(socket.gethostname())
    print(f'ip_addr: {ip_addr}')
    return ip_addr



# cache를 DB라고 가정
cache = dict()

def get_blockchain():
    '''데이터베이스로부터 블록체인 정보 가져오기'''

    # 블록체인이 있는지 확인 실제 DB에 블록체인을 생성하고 저장하기
    # blockchain_eixst = Block.query.order_by(
    #         Block.timestamp.desc(),
    # ).first()
    blockchain_eixst = Block.query.all()

    # 블록체인 없을 경우(블록이 0개) ->최초 1회만 생성
    if not blockchain_eixst:
        block_chain = BlockChain(
            # blockchain_addr=Wallet().blockchain_address,
            port=get_current_port_number()
        )
        block_chain.create_genesis_block()

    # 블록체인 정보를 취합하여 리턴(REST -> json)
    return build_blockchain_json()


def build_blockchain_json() -> dict:
    '''DB로부터 데이터를 추출하여 dict로 가공하여 리턴
    Return: {
        'chain': [list of dict (block and transaction info)
            {
                'nonce': Int,
                'prev_hash': str,
                'timestamp': float,
                'transaction_pool': [],
                'transactions': [ list of dict (transaction objects)
                    {
                        'send_blockchain_addr': str,
                        'recv_blockchain_addr': str,
                        'amount': float,
                    }, ...]
            },
        'transaction_pool': [list of transactions]
        }
    }'''
    # DB에 있는 모든 블록 불러오기
    blocks = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp)

    # 리턴할 dict 정의
    result_dic = {
        'chain': [],
        'transaction_pool': [],
    }

    # 각 블록에 있는 Transaction 정보까지 처리하여 담기
    for block in blocks:
        result_dic['chain'].append(
            {
                'nonce': block.nonce,
                'prev_hash': block.prev_hash,
                'timestamp': block.timestamp,
                'transactions': get_transaction_list(block),
            }
        )

    # 가장 최근(마지막) 생성된 블록일 경우 -> transaction_pool 생성
    last_block = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp.desc()).first()
    result_dic['transaction_pool'] = get_transaction_list(last_block)

    # 정리된 결과 리턴
    return result_dic


def get_transaction_list(block: Block) -> list:
    '''Block의 Transaction 객체를 dict로 변환하여 리턴'''
    transaction_list = []
    transactions = block.transactions
    for transaction in transactions:
        transaction_list.append(
            {
                'send_blockchain_addr': transaction.send_addr,
                'recv_blockchain_addr': transaction.recv_addr,
                'amount': transaction.amount,
            }
        )
    return transaction_list


def hash(block: dict) -> str:
    '''사전을 hash 수행하고 문자열 리턴'''
    sorted_block = json.dumps(block, sort_keys=True)
    return hashlib.sha256(sorted_block.encode()).hexdigest()


def get_last_block() -> dict:
    '''DB에서 마지막 블록을 찾아서 dict으로 변환하여 리턴'''
    last_block = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp.desc()).first()
    return sorted_dict_by_key(last_block.__dict__)


def get_prev_hash() -> str:
    '''DB에서 마지막 블록의 prev_hash 리턴'''
    prev_hash = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp.desc()).first().prev_hash
    return prev_hash


def validate_transaction_params(request_json: dict) -> bool:
    '''필요한 파라미터가 전달되었는지 확인'''
    required_items = (
    'send_public_key',
    'send_blockchain_addr',
    'recv_blockchain_addr',
    'amount',
    'signature',
    )
    return all(k in request_json for k in required_items)


# def get_active_neighbor_ips() -> list:
#     '''블록체인 P2P 네트워크에 연결된 노드의 주소를 검색하여 리턴'''
#     p2p_manager = P2PManager()
#     active_neighbors = p2p_manager.get_all_active_nodes()
#     active_neighbors = set([node.ip for node in active_neighbors])
