import base64
from server.secret import csrf_token_secrete
from datetime import timedelta
import os
from p2p_net.config import SQLALCHEMY_DATABASE_URI as p2p_database_uri

BASE_DIR = os.path.dirname(__file__)
# BASE_DIR = '/home/kafa46/workspace/flask_app/path_to_project'

# SQLALCHEMY_DATABASE_URI -> DB 접속 주소
# 프로젝트 루트 디렉토리와 우리가 생성할 DB (hello_cju.db) 연결
# 'sqlite:///' -> 사용할 DB는 SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(BASE_DIR, 'blockhain.db')
)

P2P_DATABASE_URI = p2p_database_uri

# ORM 객체의 변경사항을 지속적으로 추적하고 변동 이벤트에 대한 메시지 출력
# 불필요한 경우 False로 꺼놓는 것을 추천
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Seret key for CSRF token
SECRET_KEY = csrf_token_secrete

# 채굴자에게 보내는 블록체인 네트워크 이름
BLOCKCHAIN_NETOWRK= 'BLOCK CHAIN NETWORK'

# Mining Difficulty
MINING_DIFFICULTY = 5

# Mining Reward
MINING_REWARD = 15.0

# 블록체인 네트워크 P2P node 통신에 사용할 포트
PORT_P2P_NETWORK = 22901

# 블록체인 네트워크가 사용할 포트
PORT_BLOCKCHAIN = 7000

