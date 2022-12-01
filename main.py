import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from apis import init_set, go
from go.models import stones_plot, Board, WIDTH
from go.utils import get_position2index, transform_indexes

board_play = Board(WIDTH, WIDTH, 0)


# 画棋盘
def draw_board():
    fig = plt.figure(figsize=[7, 7])
    fig.patch.set_facecolor((0.85, 0.64, 0.45))  # 背景颜色
    ax = fig.add_subplot(221)  # 相对位置
    ax.set_axis_off()
    return fig, ax


# 画格
def draw_grids(ax):
    # 竖线
    for x in range(19):
        ax.plot([x, x], [0, 18], 'k')
    # 横线
    for y in range(19):
        ax.plot([0, 18], [y, y], 'k')
    ax.set_position([0, 0, 1, 1])


# 画星位
def draw_star_points(ax, x, y):
    ax.plot(x, y, 'o', markersize=8, markeredgecolor=(0, 0, 0), markerfacecolor='k', markeredgewidth=1)


# 画棋子
def draw_stone(x, y, color):
    stone = ax.plot(x, y, 'o', markersize=10, markeredgecolor=(0, 0, 0), markerfacecolor=color, markeredgewidth=1)
    return stone


# 点击事件
def on_click(event):
    # get the points clicked on the board
    if event.xdata is None or event.ydata is None:
        return
    x = int(round(event.xdata))
    y = int(round(event.ydata))

    # Draw the stone on the board
    if 0 <= x <= 18 and 0 <= y <= 18:
        if event.button == 1:
            index_x, index_y = 19 - y, x + 1
            print("xy坐标：" + str(index_x) + str(index_y))
            play_index = get_position2index(index_x, index_y)
            print("棋盘坐标：" + play_index)
            player_ = board_play.get_player()
            play(index_x, index_y, play_index, True, player_)
        else:
            return
    else:
        return


def play(index_x, index_y, board_index, is_engine, player):
    if board_play.play(index_x, index_y, player) is True:
        print('正常落子')
        # 坐标变换后插入到plot
        stones_plot[index_x][index_y] = draw_stone(index_y - 1, 19 - index_x, 'k' if player.get_identifier() == 1 else 'w')
        board_play.next_player()
        captured_stones = board_play.captured_stones  # 吃子集合
        result = []
        for stones in captured_stones:
            stones_plot[stones.x, stones.y].pop().remove()  # remove the plot
            stones_plot[stones.x, stones.y] = None
            result.append(get_position2index(stones.x, stones.y))
        print("被吃子的位置：", result)
        plt.draw()
        # send to engine if is_engine is True
        if is_engine:
            go_data = {"user_id": "djn", "board": board_index, "current_player": "1"}
            go_resp = go(go_data)
            engine_x, engine_y = transform_indexes(go_resp)
            print(engine_x, engine_y, resp)
            # 引擎再下一步，is_engine = False
            play(engine_x, engine_y, go_resp, False, board_play.get_player())
    else:
        print('not allowed to play')


if __name__ == '__main__':
    fig, ax = draw_board()
    draw_grids(ax)
    for i in range(3, 16, 6):
        for j in range(3, 16, 6):
            draw_star_points(ax, i, j)
    fig.canvas.mpl_connect('button_press_event', on_click)
    buttonaxe = plt.axes([0.01, 0.01, 0.08, 0.05])
    button1 = Button(buttonaxe, 'begin', color='grey', hovercolor='grey')
    data = {"user_id": "djn", "rules": "", "komi": "", "play": "1", "level": "p", "boardsize": "19"}
    resp = init_set(data)
    if not resp:
        print('连接服务器失败')
        exit(0)
    # 初始化成功 则开始
    if resp == 1000:
        plt.show()
