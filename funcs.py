import json
import re

import db_operation
import go.utils

LEVEL = 0
PLAYER = 1
ROW_CLICK = 0


def change_color(*args):
    args[0].setStyleSheet(
        '''
        *{background-color:#e6e6e6;}
        ''')
    for i in range(1, len(args)):
        args[i].setStyleSheet(
            '''
            *{background-color:#ffffff;}
            ''')


def switch2play(window):
    window.game_record_widget.setVisible(False)
    window.select_record_widget.setVisible(False)
    window.play_func_widget.setVisible(False)
    window.view_record_widget.setVisible(False)
    window.play_setting_widget.setVisible(True)
    window.play_widget.setVisible(True)


def switch2review(window):
    window.game_record_widget.setVisible(True)
    window.game_record_table_view.setVisible(True)
    window.select_record_widget.setVisible(True)
    window.play_widget.setVisible(False)
    window.play_func_widget.setVisible(False)
    window.play_setting_widget.setVisible(False)
    window.view_record_widget.setVisible(False)


# 画棋子
def draw_stone(x, y, color, ax):
    stone = ax.plot(x, y, 'o', markersize=12, markeredgecolor=(0, 0, 0), markerfacecolor=color, markeredgewidth=1)
    return stone


# 画星位
def draw_stars(ax):
    for i in range(3, 16, 6):
        for j in range(3, 16, 6):
            draw_star_points(ax, i, j)


# 画星位
def draw_star_points(ax, x, y):
    ax.plot(x, y, 'o', markersize=5, markeredgecolor=(0, 0, 0), markerfacecolor='k', markeredgewidth=1)


# 画红点
def draw_red_point(ax, x, y):
    red = ax.plot(x, y, 'o', markersize=4, markeredgecolor=(0, 0, 0), markerfacecolor='r', markeredgewidth=1)
    return red


# 画格
def draw_grids(ax):
    # 竖线
    for x in range(19):
        ax.plot([x, x], [0, 18], 'k')
    # 横线
    for y in range(19):
        ax.plot([0, 18], [y, y], 'k')
    ax.set_position([0, 0, 1, 1])


def check_email_format(email):
    re_format = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(re_format, email)


def check_phone_format(phone):
    re_format = r'^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$'
    return re.match(re_format, phone)


def check_password_format(password):
    if len(password) < 3 or len(password) > 15:
        return False
    return True


def check_information_exist(user_name, phone_number, email, user_id, password):
    user = db_operation.check_information_exist(user_name, phone_number, email, user_id)
    if user is not None:
        add_user(user_id, user_name, phone_number, email, password)
    else:
        return False


def add_user(user_id, user_name, phone_number, email, password):
    db_operation.v2_add_user(user_id, user_name, phone_number, email, password)


def check_information_correct(user_name, password):
    user = db_operation.find_by_username(user_name)
    if user is None:
        return "userNameNotExist"
    elif user.password == password:
        return "success"
    else:
        return "wrongPassword"


def get_games(user_name):
    game_result = db_operation.get_all_games(user_name)
    response_body = []
    for o in game_result:
        obj = {"id": o.id, "play_info": o.play_info, "result": o.result, "code": o.code}
        response_body.append(obj)
    return response_body


def transform_indexes(index):
    alpha, beta = index[1], index[0]
    count = 1
    for c in range(ord('A'), ord('T')):
        c_ = chr(c)
        if beta == c_:
            break
        count += 1
    cnt = 1
    for c in range(ord('A'), ord('T')):
        c_ = chr(c)
        if c_ == alpha:
            break
        cnt += 1
    return count, cnt


def get_black_moves_from_code(sgf):
    moves = re.findall(r";B\[(.+?)]", sgf)
    result = []
    for move in moves:
        result.append(transform_indexes(move.upper()))
    return result


def get_white_moves_from_code(sgf):
    moves = re.findall(r";W\[(.+?)]", sgf)
    result = []
    for move in moves:
        result.append(transform_indexes(move.upper()))
    return result


def get_all_moves_and_merge(sgf):
    black_moves = get_black_moves_from_code(sgf)
    white_moves = get_white_moves_from_code(sgf)
    i, j = 0, 0
    result = []
    while i < len(black_moves) and j < len(white_moves):
        if i <= j:
            result.append(black_moves[i])
            i += 1
        else:
            result.append(white_moves[j])
            j += 1
    return result
