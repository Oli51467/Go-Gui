import re

import db_operation


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


def switch(*args):
    args[0].setVisible(True)
    for i in range(1, len(args)):
        args[i].setVisible(False)


# 画棋子
def draw_stone(x, y, color, ax):
    stone = ax.plot(x, y, 'o', markersize=20, markeredgecolor=(0, 0, 0), markerfacecolor=color, markeredgewidth=1)
    return stone


# 画星位
def draw_stars(ax):
    for i in range(3, 16, 6):
        for j in range(3, 16, 6):
            draw_star_points(ax, i, j)


# 画星位
def draw_star_points(ax, x, y):
    ax.plot(x, y, 'o', markersize=8, markeredgecolor=(0, 0, 0), markerfacecolor='k', markeredgewidth=1)


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
