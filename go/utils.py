# 根据Java源码计算二维整型列表的hash
def get_deep_hash(obj):
    if obj is None:
        return 0
    result = 1
    for o in obj:
        element_hash = get_hash(o)
        result = 31 * result + element_hash
    return result


# 计算一维整型列表的hash
def get_hash(o):
    if o is None:
        return 0
    result = 1
    for o1 in o:
        result = 31 * result + o1
    return result


# 根据Java Arrays.deepEquals()判断二维列表是否值相同
def deep_equals(a, b):
    if a is b:
        return True
    if a is None or b is None:
        return False
    length = len(a)
    if len(b) != length:
        return False
    for i in range(0, length):
        e1, e2 = a[i], b[i]
        if e1 is e2:
            continue
        if e1 is None:
            return False
        eq = deep_equals0(e1, e2)
        if not eq:
            return False
    return True


# 判断一维列表是否值相同
def deep_equals0(e1, e2):
    assert e1 is not None
    if e1 is e2:
        return True
    if e1 is None or e2 is None:
        return False
    length = len(e1)
    if len(e2) != length:
        return False
    for i in range(0, length):
        if e1[i] != e2[i]:
            return False
    return True


# 将棋盘坐标转化为行列坐标 return: (row, column)
def transform_indexes(index):
    alpha, number = index[0], index[1:]
    cnt = 1
    for c in range(ord('A'), ord('T')):
        c_ = chr(c)
        if c_ == 'I':
            continue
        if c_ == alpha:
            break
        cnt += 1
    return 20 - int(number), cnt


# 将行列坐标转化为棋盘坐标
def get_position2index(x, y):
    cnt_, position_ = 1, ""
    for c_ in range(ord('A'), ord('Z')):
        if chr(c_) == 'I':
            continue
        if cnt_ == y:
            position_ += chr(c_)
            break
        cnt_ += 1
    position_ += str(20 - x)
    return position_


# 接收传来的落子信息并判断是否可以落子 @returns-> param1:是否可以落子True/False, params2: 吃子位置list[...] / []
def check_play(input_, user_board):
    # board为缓存中user_id唯一标识的棋盘
    index_x, index_y = transform_indexes(input_)
    print(index_x, index_y)
    player = user_board.get_player()
    if user_board.play(index_x, index_y, player):
        print('正常落子')
        user_board.next_player()
        last_turn = user_board.game_record.get_last_turn()
        last_move = user_board.get_point(last_turn.x, last_turn.y)  # 上一步
        captured_stones = user_board.captured_stones  # 吃子集合
        result = []  # 将吃子位置转化成棋盘上的坐标
        for stones in captured_stones:
            result.append(get_position2index(stones.x, stones.y))
        print(result)
        return True, result
    else:
        print('无法落子')
        return False, []

