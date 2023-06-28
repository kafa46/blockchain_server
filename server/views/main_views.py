from flask import (
    Blueprint,
    jsonify,
    make_response,
    render_template,
    request,
)
from datetime import datetime
from server.models import Block, Transaction
from server.transfer import Transfer
from server.utils import get_blockchain
from server import utils
from server.mining import Mine
from server.forms import MinigForm
from server.wallet import Wallet
from server import db
from server.blockchain import BlockChain

# Blueprint 객체 bp를 생성합니다.
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    '''메인 화면'''
    form = MinigForm()
    return render_template(
        'mining.html',
        form=form,
    )


@bp.route('/get_chain/', methods=['GET'])
def get_chain():
    '''블록체인 가져오기'''
    block_chain = utils.get_blockchain()
    response = {
        # 'chain': 'under testing',
        'chain': block_chain.get('chain'),
    }
    return jsonify(response), 200


@bp.route('/transactions/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def transactions():
    '''Transaction.transaction_pool 정보를 읽어서 리턴'''
    block_chain = get_blockchain()
    if request.method=='GET':
        '''transaction 정보 요청'''
        resp = {
            'transactions': block_chain.get('transaction_pool'),
            'length': len(block_chain.get('transaction_pool')),
        }
        return jsonify(resp), 200

    if request.method=='POST':
        '''transaction 추가'''
        request_json = request.json
        validate_success = utils.validate_transaction_params(request_json)
        if not validate_success:
            return jsonify({'message': 'missing required params'}), 400

        transfer = Transfer(
            send_public_key=request_json.get('send_public_key'),
            send_blockchain_addr=request_json.get('send_blockchain_addr'),
            recv_blockchain_addr=request_json.get('recv_blockchain_addr'),
            amount=request_json.get('amount'),
            signature=request_json.get('signature'),
        )
        is_transacted = transfer.create_transaction()

        if not is_transacted:
            return jsonify({'status': 'fail'}), 400
        return jsonify({'status': 'success'}), 201


    if request.method=='PUT':
        '''transaction 추가요청이 있을 경우 업데이트'''
        request_json = request.json
        validate_success = utils.validate_transaction_params(request_json)

        if not validate_success:
            return jsonify({'message': 'missing required params'}), 400

        transfer = Transfer(
            send_public_key=request_json.get('send_public_key'),
            send_blockchain_addr=request_json.get('send_blockchain_addr'),
            recv_blockchain_addr=request_json.get('recv_blockchain_addr'),
            amount=request_json.get('amount'),
            signature=request_json.get('signature'),
        )
        is_updated = transfer.add_transaction()

        if not is_updated:
            return jsonify({'status': 'fail'}), 400
        return jsonify({'status': 'success'}), 200

    # DB를 사용할 경우 transaction 정보를 삭제하지 않음
    # on-memory cache를 사용할 경우 필요
    # if request.method == 'DELETE':
    #     '''Transaction pool 초기화 요청이 있을 경우 비워버리기'''
    #     transactions = Transaction.query.all()
    #     for transaction in transactions:
    #         db.session.delete(transaction)
    #         db.session.commit()


@bp.route('/mining/', methods=['GET', 'POST'])
def mining():
    '''채굴 실행'''
    json_data = request.json
    recv_blockcain_addr = json_data.get('blockchain_addr')
    print(f'miner_blockchain_addr: {recv_blockcain_addr}')
    mine = Mine()

    # 채굴 성공했을때 보상받을 주소
    # 나중에 wallet server로부터 전달받도록 코딩
    # recv_blockcain_addr = '123'
    mining_success, reason = mine.mining(recv_blockcain_addr)
    if mining_success:
        return jsonify({'status': 'success'}), 200

    return jsonify({
            'status': 'fail',
            'reason': reason,}), 200


@bp.route('/mining/start/', methods=['GET'])
def mining_start():
    '''채굴 실행'''
    mine = Mine()
    mine.start_mining()
    return jsonify({'status': 'success'}), 200


@bp.route('/coin_amount/', methods=['POST'])
def coin_amount():
    blockchain_addr = request.json['blockchain_addr']
    print(f'blockchain_addr: {blockchain_addr}')
    if not blockchain_addr:
        return jsonify({
                'status': 'fail',
                'content': '지갑주소(blockchain address)가 없습니다.'
        })
    return jsonify({
        'status': 'success',
        'content': Wallet().calculate_total_amount(blockchain_addr),
    })

@bp.route('/resolve_conflicts/', methods=['PUT'])
def resolve_conflicts():
    '''가장 긴 블록체인을 찾아서 검증 -> 교체
        - 호출 시기: 개별 노드가 채굴에 성공했을 경우
        - 실행 순서: 채굴 성공 -> 블록 생성 -> 이웃 노드에게 resolve conflict 요청
    '''
    blockchain = BlockChain()
    resolve_result = blockchain.resove_conflicts()
    return jsonify({
        'status': 'success' if resolve_result else 'fail',
        'content': 'resolve_conflicts'
    }), 200