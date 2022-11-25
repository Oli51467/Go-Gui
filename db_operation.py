import datetime
import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, or_
from sqlalchemy.ext.declarative import declarative_base

import config

Base = declarative_base(config.configs['production'].engine)

Base.metadata.create_all()  # 映射到数据库
Session = sessionmaker()


class User(Base):
    # 表名
    __tablename__ = 'user'
    #  字段
    user_id = Column(type_=String(50), primary_key=True)
    user_name = Column(type_=String(20), nullable=False)
    password = Column(type_=String(50), nullable=True)
    phone = Column(type_=String(20), nullable=False)
    email = Column(type_=String(64), nullable=True)
    level = Column(type_=Integer, nullable=False, default=1)
    avatar = Column(type_=String(512), nullable=True, default="")
    platform = Column(type_=String(50), nullable=False, default="陪伴版")
    win = Column(type_=Integer, nullable=False, default=0)
    lose = Column(type_=Integer, nullable=False, default=0)
    last_modify_time = Column(type_=Integer, nullable=False, default=datetime.datetime.now)
    register_time = Column(DateTime, default=datetime.datetime.now)


class Game(Base):
    __tablename__ = 'game'
    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    user_name = Column(type_=String(255), nullable=False)
    play_info = Column(type_=String(255), nullable=False)
    result = Column(type_=String(255), nullable=False)
    code = Column(type_=String(8096), nullable=False)
    source = Column(type_=Integer, nullable=False)
    level = Column(type_=Integer, nullable=False)
    begin_time = Column(type_=DateTime, default=datetime.datetime.now)
    end_time = Column(type_=DateTime, default=datetime.datetime.now)


# 序列化 解析Game类
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return {
                "id": o.id,
                "user_name": o.user_name,
                "play_info": o.play_info,
                "result": o.result,
                "code": o.code,
                "source": o.source,
                "level": o.level,
                "begin_time": o.begin_time.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": o.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            }


# DAO层 添加一个用户
def v2_add_user(user_id, user_name, phone_number, email, password):
    session = Session()
    add_info = User(user_id=str(user_id), user_name=str(user_name), phone=str(phone_number), email=str(email), password=str(password), platform="陪伴版")
    session.add(add_info)
    session.commit()


# DAO层 根据用户名查找用户信息
def find_by_username(user_name):
    session = Session()
    user = session.query(User).filter_by(user_name=user_name).first()
    session.close()
    return user


# DAO层 根据用户信息查找用户信息
def find_by_phone_number_or_email(phone_number, email):
    session = Session()
    user = session.query(User).filter(or_(User.phone == phone_number, User.email == email)).first()
    session.close()
    return user


# DAO层 根据用户信息查找是否被注册
def check_information_exist(username, phone_number, email, userid):
    session = Session()
    user = session.query(User).filter(or_(User.user_name == username, User.phone == phone_number, User.email == email),
                                      User.user_id != userid).first()
    session.close()
    return user


# 根据id获得棋谱信息
def get_game_by_id(_id):
    session = Session()
    game = session.query(Game).filter_by(id=_id).first()
    return game


# DAO层 保存棋谱
def v1_save_game(game):
    session = Session()
    info = Game(user_name=str(game['userName']), play_info=str(game['playInfo']), result=str(game['result']),
                code=str(game['code']), source=game['source'], level=game['level'])
    session.add(info)
    session.commit()


# DAO层 获得一个用户的所有棋谱信息
def get_all_games(user_name):
    session = Session()
    session.commit()
    games = session.query(Game).filter_by(user_name=user_name)
    game_list = []
    for game in games:
        game_list.append(game)
    return game_list


# DAO层 根据id删除一个棋谱
def delete_game(id_):
    session = Session()
    info = get_game_by_id(id_)
    session.delete(info)
    session.commit()
