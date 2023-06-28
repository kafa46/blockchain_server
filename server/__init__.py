'''Init factory module'''

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from server.filters import format_datetime, format_datetime_simple
# from blockchain_practice.servers.blockchain_server.p2p_net.p2p_network import BlockChainNode
# from server import utils
import server.config as config

migrate = Migrate()
# csrf = CSRFProtect()
db = SQLAlchemy()

# Initialize Login Manager
login_manager = LoginManager()

# Blockchain P2P 네트워크
# node = BlockChainNode(
#     host=utils.get_current_ip_addr(),
#     port=config.PORT,
# )
# node.start()

def create_app(): # 함수 생성
    '''create app'''
    app = Flask(__name__)
    app.config.from_object(config)
    # login_manager.init_app(app)
    # csrf.init_app(app)
    db.init_app(app)

    # Using Batch Mode: [SQL: ALTER TABLE user DROP COLUMN XX] 방지
    #   참고 블로그: https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite
    migrate.init_app(app, db, render_as_batch=True)

    # Filters
    from .filters import format_datetime, make_short_string, short_img_path
    from .filters import format_datetime_for_input_calendar, get_num_of_lines
    from .filters import none_filter, get_num_attendance, url_trim_peniel, make_short_string_gallery
    from .filters import make_short_string_home, format_datetime_for_abbreviated
    from .filters import format_datetime_simple_with_dash, make_short_string_7, make_short_string_10
    app.jinja_env.filters['datetime'] = format_datetime # '%Y년 %m월 %d일 %H:%M'
    app.jinja_env.filters['datetime_simple'] = format_datetime_simple # '%Y년 %m월 %d일'
    app.jinja_env.filters['datetime_calendar'] = format_datetime_for_input_calendar # '%Y-%m-%d'
    app.jinja_env.filters['datetime_abbreviated'] = format_datetime_for_abbreviated # '22.9.21.


    # Model import
    # from . import models

    # View import
    from .views import main_views

    app.register_blueprint(main_views.bp)

    # 템플릿에서 continue, break 사용할 수 있도록 익스텐션 추가
    # 참고 블로그: https://blog.weirdx.io/post/53619
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    # Return App
    return app
