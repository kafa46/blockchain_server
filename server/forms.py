import math
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    StringField,
    FloatField,
    TextAreaField,
    BooleanField,
    IntegerField,
    PasswordField,
    EmailField,
    DateField,
    MultipleFileField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Email,
    NumberRange,
)
from wtforms import ValidationError


class MinigForm(FlaskForm):
    '''코인 이체 입력 폼'''
    private_key = StringField(
        label='본인의 비밀키(Private Key)',
        validators=[
            DataRequired('블록체인 전송을 위해서는 본인의 비밀키가 반드시 있어야 합니다.'),
        ]
    )
    public_key = StringField(
        label='본인의 공개키(Public Key)',
        validators=[
            DataRequired('블록체인 전송을 위해서는 본인의 공개키가 반드시 있어야 합니다.'),
        ]
    )
    my_blockchain_addr = StringField(
        label='본인의 지갑 주소',
        validators=[
            DataRequired('본인 지갑 주소는 필수입력 사항입니다.'),
        ]
    )