from server import db


class Block(db.Model):
    '''블록 -> 단위 블록'''
    id = db.Column(db.Integer, primary_key=True)
    prev_hash = db.Column(db.String(300), nullable=True)
    nonce = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.Float, nullable=True)


class Transaction(db.Model):
    '''거래정보: 하나의 블록에 담겨져 있는 거래 정보'''
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    send_addr = db.Column(db.String(300))
    recv_addr = db.Column(db.String(300))
    amount = db.Column(db.Float())
    blockchain = db.relationship(
        'Block',
        backref=db.backref('transactions')
    )


class MiningNode(db.Model):
    '''블록체인 마이닝(채굴) 노드'''
    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(50))
    port = db.Column(db.String(10))
    domain_name = db.Column(db.String(100))
    timestamp = db.Column(db.Float)
    last_access = db.Column(db.DateTime)
    initial_access = db.Column(db.DateTime, nullable=True)