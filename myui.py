# coding: utf8
import numpy as np
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import qtawesome
from PyQt5.QtCore import QCoreApplication, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QAbstractItemView, \
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fc

import db_operation
import funcs
from apis import init_set, tip
from funcs import draw_stars, change_color, draw_grids, moves_map, indexes_map, get_result, get_info, save_game_as_sgf, \
    LEVEL
from go.models import Board, WIDTH
from go.utils import transform_indexes

global USER_NAME
INIT = False
levels = ['9级', '8级', '7级', '6级', '5级', '4级', '3级', '2级', '1级', '1段', '2段', '3段', '4段', '5段', '6段',
          '职业']
games = []
# indexes_map = []  # 位置 eg: [(4, 4), (4, 16), (5, 5)]
# moves_map = []  # 坐标 eg:  [D4, H5, T6]
info_map = []
WINDOW_WIDTH, WINDOW_HEIGHT = 820, 480
BUTTON_HEIGHT, BUTTON_WIDTH = 40, 150
CENTER_HEIGHT, CENTER_WIDTH = 450, 450
OP_BUTTON_HEIGHT, OP_BUTTON_WIDTH = 50, 180
OP_ICON_HEIGHT, OP_ICON_WIDTH = 25, 25
LEVEL_BUTTON_HEIGHT, LEVEL_BUTTON_WIDTH = 50, 65


class ChooseLevelWindow(QWidget):
    def choose_level(self, level):
        gui.btn_choose_level.setText(str(levels[level]))
        funcs.LEVEL = level
        self.close()

    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_image = QLabel(self)
        png = QtGui.QPixmap('images/login_image.png')
        self.label_image.setScaledContents(True)  # 需要在图片显示之前进行设置
        self.label_image.setPixmap(png)
        self.label_image.setFixedSize(350, 350)

        self.right_widget = QtWidgets.QWidget()  # 右侧部件
        self.right_widget.setObjectName('right_layout')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.btn_level1 = QtWidgets.QPushButton("9级")
        self.btn_level1.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level1.clicked.connect(lambda: self.choose_level(0))
        self.btn_level2 = QtWidgets.QPushButton("8级")
        self.btn_level2.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level2.clicked.connect(lambda: self.choose_level(1))
        self.btn_level3 = QtWidgets.QPushButton("7级")
        self.btn_level3.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level3.clicked.connect(lambda: self.choose_level(2))
        self.btn_level4 = QtWidgets.QPushButton("6级")
        self.btn_level4.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level4.clicked.connect(lambda: self.choose_level(3))
        self.btn_level5 = QtWidgets.QPushButton("5级")
        self.btn_level5.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level5.clicked.connect(lambda: self.choose_level(4))
        self.btn_level6 = QtWidgets.QPushButton("4级")
        self.btn_level6.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level6.clicked.connect(lambda: self.choose_level(5))
        self.btn_level7 = QtWidgets.QPushButton("3级")
        self.btn_level7.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level7.clicked.connect(lambda: self.choose_level(6))
        self.btn_level8 = QtWidgets.QPushButton("2级")
        self.btn_level8.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level8.clicked.connect(lambda: self.choose_level(7))
        self.btn_level9 = QtWidgets.QPushButton("1级")
        self.btn_level9.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level9.clicked.connect(lambda: self.choose_level(8))
        self.btn_level10 = QtWidgets.QPushButton("1段")
        self.btn_level10.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level10.clicked.connect(lambda: self.choose_level(9))
        self.btn_level11 = QtWidgets.QPushButton("2段")
        self.btn_level11.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level11.clicked.connect(lambda: self.choose_level(10))
        self.btn_level12 = QtWidgets.QPushButton("3段")
        self.btn_level12.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level12.clicked.connect(lambda: self.choose_level(11))
        self.btn_level13 = QtWidgets.QPushButton("4段")
        self.btn_level13.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level13.clicked.connect(lambda: self.choose_level(12))
        self.btn_level14 = QtWidgets.QPushButton("5段")
        self.btn_level14.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level14.clicked.connect(lambda: self.choose_level(13))
        self.btn_level15 = QtWidgets.QPushButton("6段")
        self.btn_level15.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level15.clicked.connect(lambda: self.choose_level(14))
        self.btn_level16 = QtWidgets.QPushButton("职业")
        self.btn_level16.setFixedSize(LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        self.btn_level16.clicked.connect(lambda: self.choose_level(15))
        self.right_layout.addWidget(self.btn_level1, 0, 0, 1, 1)
        self.right_layout.addWidget(self.btn_level2, 0, 1, 1, 1)
        self.right_layout.addWidget(self.btn_level3, 0, 2, 1, 1)
        self.right_layout.addWidget(self.btn_level4, 0, 3, 1, 1)
        self.right_layout.addWidget(self.btn_level5, 1, 0, 1, 1)
        self.right_layout.addWidget(self.btn_level6, 1, 1, 1, 1)
        self.right_layout.addWidget(self.btn_level7, 1, 2, 1, 1)
        self.right_layout.addWidget(self.btn_level8, 1, 3, 1, 1)
        self.right_layout.addWidget(self.btn_level9, 2, 0, 1, 1)
        self.right_layout.addWidget(self.btn_level10, 2, 1, 1, 1)
        self.right_layout.addWidget(self.btn_level11, 2, 2, 1, 1)
        self.right_layout.addWidget(self.btn_level12, 2, 3, 1, 1)
        self.right_layout.addWidget(self.btn_level13, 3, 0, 1, 1)
        self.right_layout.addWidget(self.btn_level14, 3, 1, 1, 1)
        self.right_layout.addWidget(self.btn_level15, 3, 2, 1, 1)
        self.right_layout.addWidget(self.btn_level16, 3, 3, 1, 1)

        self.main_layout.addWidget(self.label_image, 0, 0, 1, 1)
        self.main_layout.addWidget(self.right_widget, 0, 1, 1, 1)
        self.setFixedSize(700, 350)
        self.setLayout(self.main_layout)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.right_widget.setStyleSheet(
            '''
            QPushButton {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
                font-size: 16px;
            }
            '''
        )


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def begin_play(self):
        self.play_board = Board(WIDTH, WIDTH, 0)
        print("用户所选等级为:", funcs.LEVEL)
        print("用户执:", "黑" if funcs.PLAYER == 1 else "白")
        # 初始化引擎
        data = {"user_id": "djn", "rules": "", "komi": "", "play": str(funcs.PLAYER), "level": "p", "boardsize": "19"}
        resp = init_set(data)
        if not resp:
            QMessageBox.critical(self, "错误", "请检查网络连接")
            print('连接服务器失败')
            return
        # 初始化成功 则开始
        if resp == 1000:
            print('连接引擎成功')
            self.play_setting_widget.setVisible(False)
            self.play_func_widget.setVisible(True)
            self.left_button_2.setEnabled(False)
            self.left_button_1.setEnabled(False)
            # TODO：串口检测 打开串口
            self.port_check()

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            print(list(port)[0])
            # self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            print('无串口')

    # 打开串口
    def port_open(self):
        self.ser = serial.Serial(port="COM17", baudrate=9600)

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)

        if self.ser.isOpen():
            print("串口状态（已开启）")

    def end_play(self):
        message = QMessageBox.question(self, '', '你确定要认输吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if message == QMessageBox.Yes:
            self.save_game_query()

    def save_game_query(self):
        message = QMessageBox.question(self, '', '是否存储棋谱？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            # TODO：棋谱存储
            db_operation.v2_save_game("djn", get_info(), get_result(), save_game_as_sgf(self.play_board), LEVEL)
            print('保存成功')
        self.play_func_widget.setVisible(False)
        self.play_setting_widget.setVisible(True)
        self.left_button_1.setEnabled(True)
        self.left_button_2.setEnabled(True)

    def change_side(self, down, up):
        if down == self.btn_choose_black:
            funcs.PLAYER = 1
        else:
            funcs.PLAYER = 2
        down.setDown(True)
        down.setStyleSheet(
            '''
            background-color:#999999;
            '''
        )
        up.setDown(False)
        up.setStyleSheet(
            '''
            background-color: #ffffff;
            '''
        )

    # 画下棋的棋盘
    def draw_origin_play_board(self):
        self.fig = plt.Figure()  # 公共属性figure
        self.canvas = fc(self.fig)  # 新建画布，在画布上构建matplotlib图像
        self.fig.patch.set_facecolor((0.85, 0.64, 0.45))  # 背景颜色 可调
        self.ax = self.fig.add_subplot()  # 轴的相对位置
        self.ax.set_axis_off()  # 关闭坐标系显示
        draw_grids(self.ax)  # 画棋盘格
        draw_stars(self.ax)
        self.canvas.draw()  # 这里调用才能在画布上显示

    # 画棋谱的棋盘
    def draw_origin_review_board(self):
        self.fig_record = plt.Figure()
        self.canvas_record = fc(self.fig_record)
        self.fig_record.set_facecolor((0.85, 0.64, 0.45))
        self.ax_record = self.fig_record.add_subplot()
        self.ax_record.set_axis_off()
        draw_grids(self.ax_record)
        draw_stars(self.ax_record)
        self.canvas_record.draw()

    # 清空棋盘
    def clear_review_board(self):
        for i in range(20):
            for j in range(20):
                if self.stones_plot_review[i, j] is not None:
                    self.stones_plot_review[i, j].pop().remove()
                    self.stones_plot_review[i, j] = None
                if self.red_point_plot[i, j] is not None:
                    self.red_point_plot[i, j].pop().remove()
                    self.red_point_plot[i, j] = None
        self.canvas_record.draw()

    # 选择一个棋谱的点击事件
    def on_game_click(self, item=None):
        # 如果单元格对象为空
        if item is None:
            return
        else:
            funcs.ROW_CLICK = item.row()  # 获取行数
            self.game_record_table_view.setVisible(False)
            self.view_record_widget.setVisible(True)
            self.cur_pointer, self.undo_pointer = 0, 0
            self.game_item_row = item.row()
            self.board_review = Board(WIDTH, WIDTH, 0)
            self.show_info.setPlainText(info_map[self.game_item_row])
            self.show_info.setAlignment(Qt.AlignLeft)
            self.last_tip_x, self.last_tip_y = 0, 0
            funcs.IS_REVIEW = True

    # 查看棋谱详细信息返回到选择棋谱界面
    def back2select_game(self):
        self.clear_review_board()
        self.view_record_widget.setVisible(False)
        self.select_record_widget.setVisible(True)
        self.game_record_table_view.setVisible(True)
        self.btn_tip.setEnabled(True)
        funcs.IS_REVIEW = False

    # 点击前进的触发事件
    def press_proceed(self):
        self.remove_tip()
        self.btn_tip.setEnabled(True)
        # print("cur_pointer: %s, undo_pointer:%s" % (self.cur_pointer, self.undo_pointer))
        if self.undo_pointer < self.cur_pointer:
            self.redo()
        else:
            if self.cur_pointer >= len(indexes_map[self.game_item_row]):
                return
            self.proceed()

    # 前进一步
    def proceed(self):
        last_x, last_y = self.board_review.game_record.get_last_turn().x, self.board_review.game_record.get_last_turn().y  # 上一步
        player = self.board_review.get_player()  # 当前玩家
        self.board_review.play(indexes_map[self.game_item_row][self.cur_pointer][0],
                               indexes_map[self.game_item_row][self.cur_pointer][1], player)  # 在棋盘上走棋
        self.board_review.next_player()
        index_x, index_y = indexes_map[self.game_item_row][self.cur_pointer][0], indexes_map[self.game_item_row][self.cur_pointer][1]
        # print(index_x, index_y)
        self.stones_plot_review[index_x, index_y] = funcs.draw_stone(index_y - 1, 19 - index_x,
                                                                     'k' if player.get_identifier() == 1 else 'w',
                                                                     self.ax_record)  # 将落子位置关联嵌入
        if self.cur_pointer != 0:  # 画红点标记 先移除上一步的红点标记
            self.red_point_plot[last_x, last_y].pop().remove()
            self.red_point_plot[last_x, last_y] = None
        self.red_point_plot[index_x, index_y] = funcs.draw_red_point(self.ax_record, index_y - 1,
                                                                     19 - index_x)  # 当前位置标记嵌入
        captured_stones = self.board_review.captured_stones  # 走棋后被吃的棋子
        for stones in captured_stones:  # remove the plot
            self.stones_plot_review[stones.x, stones.y].pop().remove()
            self.stones_plot_review[stones.x, stones.y] = None
        self.canvas_record.draw()
        self.cur_pointer += 1
        self.undo_pointer += 1

    # 点击回退的触发事件
    def press_undo(self):
        self.remove_tip()
        self.btn_tip.setEnabled(True)
        print("cur_pointer: %s, undo_pointer:%s" % (self.cur_pointer, self.undo_pointer))
        if self.cur_pointer <= 0 or self.undo_pointer <= 0:
            return
        self.undo()

    # 回退一步
    def undo(self):
        if self.undo_pointer <= 0:
            return
        last_move = self.board_review.get_point(self.board_review.game_record.get_last_turn().x,
                                                self.board_review.game_record.get_last_turn().y)  # 获取上一步
        # 移除棋子plot
        self.stones_plot_review[last_move.x, last_move.y].pop().remove()
        self.stones_plot_review[last_move.x, last_move.y] = None
        # 移除标记plot
        self.red_point_plot[last_move.x, last_move.y].pop().remove()
        self.red_point_plot[last_move.x, last_move.y] = None
        captured_stones = self.board_review.game_record.get_last_turn().captured_stones  # 被吃的棋子
        for stones in captured_stones:  # 恢复被吃的棋子 重新plot进去
            self.stones_plot_review[stones.x, stones.y] = funcs.draw_stone(stones.y - 1, 19 - stones.x,
                                                                           "k" if self.board_review.get_player().get_identifier() == 1 else "w",
                                                                           self.ax_record)
        self.board_review.undo()
        self.undo_pointer -= 1
        # # 重新标记上一步
        if self.undo_pointer != 0 and self.cur_pointer != 0:
            cur_x, cur_y = self.board_review.game_record.get_last_turn().x, self.board_review.game_record.get_last_turn().y
            self.red_point_plot[cur_x, cur_y] = funcs.draw_red_point(self.ax_record, cur_y - 1, 19 - cur_x)

        self.canvas_record.draw()

    def redo(self):
        last_x, last_y = self.board_review.game_record.get_last_turn().x, self.board_review.game_record.get_last_turn().y  # 获取上一步
        # 移除上一步的标记
        if self.undo_pointer != 0 and self.cur_pointer != 0:
            self.red_point_plot[last_x, last_y].pop().remove()
            self.red_point_plot[last_x, last_y] = None
        self.board_review.redo()
        captured_stones = self.board_review.game_record.get_last_turn().captured_stones  # 被吃的棋子
        for stones in captured_stones:  # 移除被吃的棋子 remove the plot
            self.stones_plot_review[stones.x, stones.y].pop().remove()
            self.stones_plot_review[stones.x, stones.y] = None
        # redo后的上一步，此时last_x, last_y是上上步
        last_move = self.board_review.get_point(self.board_review.game_record.preceding.peek().x,
                                                self.board_review.game_record.preceding.peek().y)
        # 将新的一步plot进去
        self.stones_plot_review[last_move.x, last_move.y] = funcs.draw_stone(last_move.y - 1, 19 - last_move.x,
                                                                             'k' if self.board_review.get_player().get_identifier() == 2 else 'w',
                                                                             self.ax_record)
        # 标记新的一步
        self.red_point_plot[last_move.x, last_move.y] = funcs.draw_red_point(self.ax_record, last_move.y - 1,
                                                                             19 - last_move.x)
        self.undo_pointer += 1
        self.canvas_record.draw()

    # 点击快进的触发事件
    def press_fast_proceed(self):
        self.remove_tip()
        self.btn_tip.setEnabled(True)
        for i in range(7):
            if self.undo_pointer < self.cur_pointer:
                self.redo()
            else:
                if self.cur_pointer >= len(indexes_map[self.game_item_row]):
                    return
                self.proceed()

    # 快进 step=7
    def press_fast_undo(self):
        if self.cur_pointer <= 0 or self.undo_pointer <= 0:
            return
        self.remove_tip()
        self.btn_tip.setEnabled(True)
        for i in range(7):
            if self.cur_pointer <= 0 or self.undo_pointer <= 0:
                return
            self.undo()

    def tip(self):
        # 此时局面的索引是undo_pointer指示的
        if self.undo_pointer < self.cur_pointer:
            tip_data = {"user_id": "djn", "initialStones": [],
                        "moves": moves_map[self.game_item_row][:self.undo_pointer]}
        else:
            tip_data = {"user_id": "djn", "initialStones": [],
                        "moves": moves_map[self.game_item_row][:self.undo_pointer]}
        go_resp = tip(tip_data)
        if go_resp == 0:
            QMessageBox.critical(self, "错误", "请检查网络连接")
            return
        self.btn_tip.setEnabled(False)
        engine_x, engine_y = transform_indexes(go_resp)
        self.red_point_plot[engine_x, engine_y] = funcs.draw_tip_point(self.ax_record, engine_y - 1, 19 - engine_x)
        self.last_tip_x, self.last_tip_y = engine_x, engine_y
        self.canvas_record.draw()

    def remove_tip(self):
        if self.red_point_plot[self.last_tip_x, self.last_tip_y] is not None:
            self.red_point_plot[self.last_tip_x, self.last_tip_y].pop().remove()
            self.red_point_plot[self.last_tip_x, self.last_tip_y] = None
            self.last_tip_x, self.last_tip_y = 0, 0

    def init_ui(self):
        self.timer = QTimer(self)
        self.stones_plot_review = np.full((20, 20), None)
        self.red_point_plot = np.full((20, 20), None)
        self.draw_origin_play_board()
        self.draw_origin_review_board()

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.top_widget = QtWidgets.QWidget()  # 创建头部部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()  # 创建头部部件的网格布局层
        self.top_widget.setLayout(self.top_layout)  # 设置头部部件布局为网格

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        # 未登陆时显示登陆和注册组件布局
        self.left_widget_enter = QtWidgets.QWidget()  # 创建左上侧部件
        self.left_widget_enter.setObjectName('enter_widget')
        self.left_layout_enter = QtWidgets.QGridLayout()  # 创建左上侧部件的网格布局层
        self.left_widget_enter.setLayout(self.left_layout_enter)  # 设置左上侧部件布局为网格
        png = QtGui.QPixmap('images/code.jpg')
        self.label_image = QLabel(self)
        self.label_image.setScaledContents(True)  # 需要在图片显示之前进行设置
        self.label_image.setPixmap(png)
        self.label_image.setFixedSize(80, 80)
        self.left_layout_enter.addWidget(self.label_image, 0, 0, 1, 1)

        # 登陆时显示用户信息
        self.left_widget_user_info = QtWidgets.QWidget()  # 创建左上侧部件
        self.left_widget_user_info.setObjectName('enter_widget')
        self.left_layout_user_info = QtWidgets.QGridLayout()  # 创建左上侧部件的网格布局层
        self.left_widget_user_info.setLayout(self.left_layout_user_info)  # 设置左上侧部件布局为网格
        self.user_name_label = QLabel(self)
        self.user_name_label.setText("user_name")
        self.left_widget_user_info.setVisible(False)  # 默认不显示

        self.left_widget2 = QtWidgets.QWidget()  # 创建左中侧部件
        self.left_widget2.setObjectName('left_widget2')
        self.left_layout2 = QtWidgets.QGridLayout()  # 创建左中侧部件的网格布局层
        self.left_widget2.setLayout(self.left_layout2)  # 设置左中侧部件布局为网格

        self.left_widget3 = QtWidgets.QWidget()  # 创建左下侧部件-占位
        self.left_widget3.setObjectName('left_widget3')
        self.left_layout3 = QtWidgets.QGridLayout()  # 创建左下侧部件的网格布局层-占位
        self.left_widget3.setLayout(self.left_layout3)  # 设置左下侧部件布局为网格-占位

        self.index_image = QLabel(self)
        png = QtGui.QPixmap('images/index.png')
        self.index_image.setScaledContents(True)  # 需要在图片显示之前进行设置
        self.index_image.setPixmap(png)
        self.index_image.setFixedSize(100, 100)

        # 按钮
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('mdi6.axe-battle', color='#2c3a45'), "对弈")
        self.left_button_1.setObjectName('play')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.database', color='#2c3a45'), "棋谱")
        self.left_button_2.setObjectName('game')

        self.left_layout2.addWidget(self.left_button_1, 0, 0, 1, 2)
        self.left_layout2.addWidget(self.left_button_2, 1, 0, 1, 2)

        self.left_layout3.addWidget(self.index_image, 0, 0, 1, 1)

        self.left_username = QtWidgets.QLabel("Gobot")
        self.left_username.setObjectName('App')
        self.left_out = QtWidgets.QPushButton(qtawesome.icon('fa.sign-out', color='#808080'), "退出")
        self.left_out.setObjectName('left_out')
        self.left_out.clicked.connect(self.close)  # 点击按钮之后关闭窗口
        self.top_layout.addWidget(self.left_username, 0, 0, 1, 15)
        self.top_layout.addWidget(self.left_out, 0, 16, 1, 1)

        # 中间组件 分开显示
        self.play_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.play_widget.setObjectName('play_widget')
        self.play_layout = QtWidgets.QGridLayout()
        self.play_widget.setLayout(self.play_layout)  # 设置右侧部件布局为网格
        self.play_layout.addWidget(self.canvas, 0, 0, 7, 7)  # 添加棋盘画布

        self.game_record_widget = QtWidgets.QWidget()
        self.game_record_widget.setObjectName('game_record_widget')
        self.game_record_layout = QtWidgets.QGridLayout()
        self.game_record_widget.setLayout(self.game_record_layout)  # 设置index部件布局为网格
        self.game_record_layout.addWidget(self.canvas_record, 0, 0, 7, 7)
        self.game_record_widget.setVisible(False)  # 默认不显示

        # 右边栏 下棋时的按钮
        self.btn_count = QtWidgets.QPushButton(qtawesome.icon('msc.git-pull-request', color='#2c3a45'), "AI判断胜负")
        self.btn_resign = QtWidgets.QPushButton(qtawesome.icon('mdi6.close-box', color='#2c3a45'), "认输")
        self.btn_resign.clicked.connect(lambda: self.end_play())
        self.btn_peace = QtWidgets.QPushButton(qtawesome.icon('ph.handshake-light', color='#2c3a45'), "和棋")
        self.btn_count.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btn_resign.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btn_peace.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.play_func_widget = QtWidgets.QWidget()
        self.play_func_widget.setObjectName('setting_widget')
        self.play_func_layout = QtWidgets.QGridLayout()
        self.play_func_widget.setLayout(self.play_func_layout)
        self.play_func_layout.addWidget(self.btn_count, 3, 1, 1, 1)
        self.play_func_layout.addWidget(self.btn_resign, 4, 1, 1, 1)
        self.play_func_layout.addWidget(self.btn_peace, 5, 1, 1, 1)
        self.play_func_widget.setVisible(False)

        # 右边栏 下棋前的设置
        self.label_rules = QLabel("对局设置")
        self.edit_rules = QLineEdit("分先")
        self.edit_rules.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_rules.setReadOnly(True)
        self.edit_size = QLineEdit("19路棋盘")
        self.edit_size.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_size.setReadOnly(True)
        self.edit_komi = QLineEdit("黑贴3又3/4子")
        self.edit_komi.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_komi.setReadOnly(True)
        self.btn_choose_black = QtWidgets.QPushButton("执黑")
        self.btn_choose_black.setDown(True)
        self.btn_choose_black.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btn_choose_white = QtWidgets.QPushButton("执白")
        self.btn_choose_white.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btn_choose_black.clicked.connect(
            lambda: self.change_side(down=self.btn_choose_black, up=self.btn_choose_white))
        self.btn_choose_white.clicked.connect(
            lambda: self.change_side(down=self.btn_choose_white, up=self.btn_choose_black))
        self.btn_play = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "开始下棋")
        self.btn_play.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btn_choose_level = QtWidgets.QPushButton("选择段位")
        self.btn_choose_level.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.play_setting_widget = QtWidgets.QWidget()
        self.play_setting_widget.setObjectName('play_setting_widget')
        self.play_setting_layout = QtWidgets.QVBoxLayout()
        self.play_setting_layout.setSpacing(13)
        self.play_setting_layout.setContentsMargins(0, 20, 0, 0)
        self.play_setting_widget.setLayout(self.play_setting_layout)
        self.play_setting_layout.addWidget(self.label_rules)
        self.play_setting_layout.addWidget(self.edit_size)
        self.play_setting_layout.addWidget(self.edit_rules)
        self.play_setting_layout.addWidget(self.edit_komi)
        self.play_setting_layout.addWidget(self.btn_choose_black)
        self.play_setting_layout.addWidget(self.btn_choose_white)
        self.play_setting_layout.addWidget(self.btn_choose_level)
        self.play_setting_layout.addWidget(self.btn_play)
        self.play_setting_layout.addStretch()
        self.btn_play.clicked.connect(self.begin_play)

        # 右边 棋谱栏
        self.select_record_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.select_record_widget.setObjectName('select_record_widget')
        self.select_record_layout = QtWidgets.QGridLayout()
        self.select_record_widget.setLayout(self.select_record_layout)  # 设置右侧部件布局为网格
        self.select_record_widget.setVisible(False)

        # QTableWidget在右边展示数据库里的棋谱
        self.game_record_table_view = QTableWidget()
        self.game_record_table_view.verticalHeader().setVisible(False)
        self.game_record_table_view.horizontalHeader().setVisible(False)
        self.game_record_table_view.setColumnCount(1)
        self.game_record_table_view.setRowCount(10)
        self.game_record_table_view.horizontalHeader().setStretchLastSection(True)
        self.game_record_table_view.verticalHeader().setDefaultSectionSize(80)
        self.game_record_table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.game_record_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.game_record_table_view.itemClicked.connect(self.on_game_click)
        for index in range(len(games)):
            game_information = games[index]['play_info'] + "\n" + games[index]['result'] + "\n" + str(
                games[index]['time'])
            item = QTableWidgetItem(game_information)
            # 设置每个位置的文本值
            funcs.get_all_moves_and_merge(games[index]['code'])
            # indexes_map.append(funcs.get_all_moves_and_merge(games[index]['code'])[0])
            info_map.append(game_information)
            self.game_record_table_view.setItem(index, 0, item)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.game_record_table_view.setFixedWidth(180)
        self.select_record_layout.addWidget(self.game_record_table_view, 0, 1, 1, 1)

        # 右边 查看棋谱 操作前进后退
        self.view_record_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.view_record_widget.setObjectName('view_record_widget')
        self.view_record_layout = QtWidgets.QVBoxLayout()
        self.view_record_widget.setLayout(self.view_record_layout)  # 设置右侧部件布局为网格
        self.view_record_widget.setVisible(False)

        # 前进按钮
        self.proceed_button = QtWidgets.QPushButton("前进")
        self.proceed_button.setIcon(QtGui.QIcon('images/icon_proceed.png'))
        self.proceed_button.setIconSize(QtCore.QSize(OP_ICON_HEIGHT, OP_BUTTON_WIDTH))
        self.proceed_button.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.proceed_button.clicked.connect(self.press_proceed)
        # 返回棋谱列表按钮
        self.btn_return2record = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "返回棋谱")
        self.btn_return2record.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.btn_return2record.clicked.connect(self.back2select_game)
        # 后退按钮
        self.undo_button = QtWidgets.QPushButton("后退")
        self.undo_button.setIcon(QtGui.QIcon('images/icon_undo.png'))
        self.undo_button.setIconSize(QtCore.QSize(OP_ICON_HEIGHT, OP_ICON_WIDTH))
        self.undo_button.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.undo_button.clicked.connect(self.press_undo)
        # 快进按钮
        self.fast_proceed_button = QtWidgets.QPushButton("快进")
        self.fast_proceed_button.setIcon(QtGui.QIcon('images/icon_fast_proceed.png'))
        self.fast_proceed_button.setIconSize(QtCore.QSize(OP_ICON_HEIGHT, OP_ICON_WIDTH))
        self.fast_proceed_button.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.fast_proceed_button.clicked.connect(self.press_fast_proceed)
        # 快退按钮
        self.fast_undo_button = QtWidgets.QPushButton("快退")
        self.fast_undo_button.setIcon(QtGui.QIcon('images/icon_fast_undo.png'))
        self.fast_undo_button.setIconSize(QtCore.QSize(OP_ICON_HEIGHT, OP_ICON_WIDTH))
        self.fast_undo_button.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.fast_undo_button.clicked.connect(self.press_fast_undo)
        # 对局信息展示
        self.show_info = QTextEdit()
        self.show_info.setFontPointSize(13)
        self.show_info.setFixedSize(180, 70)
        self.show_info.setReadOnly(True)
        # 提示一手按钮
        self.btn_tip = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "AI选点")
        self.btn_tip.setFixedSize(OP_BUTTON_WIDTH, OP_BUTTON_HEIGHT)
        self.btn_tip.clicked.connect(self.tip)

        self.view_record_layout.addWidget(self.show_info)
        self.view_record_layout.addWidget(self.proceed_button)
        self.view_record_layout.addWidget(self.fast_proceed_button)
        self.view_record_layout.addWidget(self.undo_button)
        self.view_record_layout.addWidget(self.fast_undo_button)
        self.view_record_layout.addWidget(self.btn_tip)
        self.view_record_layout.addWidget(self.btn_return2record)
        self.view_record_layout.setContentsMargins(0, 0, 0, 0)

        self.play_widget.setFixedSize(CENTER_HEIGHT, CENTER_WIDTH)
        self.game_record_widget.setFixedSize(CENTER_HEIGHT, CENTER_WIDTH)

        self.left_layout.addWidget(self.left_widget_enter, 0, 0, 3, 2)  # 左侧部件在第0行第0列，占3行3列
        self.left_layout.addWidget(self.left_widget2, 3, 0, 2, 2)  # 左侧部件在第3行第0列，占2行3列
        self.left_layout.addWidget(self.left_widget3, 9, 0, 6, 2)  # 左侧部件在第9行第0列，占6行3列

        self.main_layout.addWidget(self.left_widget, 1, 0, 12, 2)  # 左侧部件在第1行第0列，占12行2列
        self.main_layout.addWidget(self.play_widget, 1, 2, 12, 7)  # 右侧部件在第1行第3列，占12行9列
        self.main_layout.addWidget(self.game_record_widget, 1, 2, 12, 7)  # 右侧部件在第1行第2列，占12行9列
        self.main_layout.addWidget(self.play_func_widget, 1, 9, 12, 3)
        self.main_layout.addWidget(self.play_setting_widget, 1, 9, 12, 3)
        self.main_layout.addWidget(self.select_record_widget, 1, 9, 12, 3)
        self.main_layout.addWidget(self.view_record_widget, 1, 9, 12, 3)
        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 12)  # 头部侧部件在第0行第0列，占1行11列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_layout.setVerticalSpacing(0)
        self.main_layout.setSpacing(0)
        self.top_layout.setSpacing(0)
        self.left_layout.setSpacing(0)
        self.left_layout2.setSpacing(0)
        self.left_layout3.setSpacing(0)
        self.view_record_layout.setSpacing(0)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout_enter.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        self.left_layout3.setContentsMargins(0, 0, 0, 0)
        self.game_record_table_view.setContentsMargins(0, 0, 0, 0)
        self.view_record_layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.left_button_1.clicked.connect(
            lambda: change_color(self.left_button_1, self.left_button_2))
        self.left_button_2.clicked.connect(
            lambda: change_color(self.left_button_2, self.left_button_1))

        self.left_button_1.clicked.connect(lambda: funcs.switch2play(self))
        self.left_button_2.clicked.connect(lambda: funcs.switch2review(self))

        self.left_button_1.setStyleSheet(
            '''
            *{background-color:#e6e6e6;}
            ''')
        self.btn_choose_black.setStyleSheet(
            '''
            background-color:#999999;
            '''
        )
        self.btn_play.setStyleSheet(
            '''
            background-color:#31a420;
            '''
        )
        self.btn_return2record.setStyleSheet(
            '''
            background-color:#31a420;
            '''
        )

        self.play_widget.setStyleSheet(
            '''
            QLabel{
            border:none;
            font-size:23px;
            font-weight:500;
            color:#2c3a45;
            padding-left:30px;
             }
            ''')
        self.game_record_widget.setStyleSheet(
            '''
            QLabel{
            border:none;
            font-size:25px;
            font-weight:500;
            color:#2c3a45;
            padding-left:30px;
            }
            QPushButton {
                font-size:14px;
            }
            ''')
        self.left_widget_enter.setStyleSheet(
            '''
            *{color:#2c3a45;}
            QPushButton:hover{background:#e6e6e6;}
            QPushButton{
            border:none;
            font-weight:600;
            font-size:14px;
            }
            ''')
        self.left_widget2.setStyleSheet(
            '''
            QPushButton {
                font-size: 18px;
            }
            QPushButton:hover{
                background:#e6e6e6;
            }
            ''')
        self.left_widget3.setStyleSheet(
            '''
            *{background-color:#fafafa;}
            ''')
        self.top_widget.setStyleSheet(
            '''
            *{background-color:#303030;}
            QLabel{
                color:#ffffff;
                border:none;
                font-weight:600;
                font-size:14px;
             }
            QPushButton{
                color:#ffffff;
                border:none;
                font-weight:600;
                font-size:14px;
             }
            ''')
        self.left_widget.setStyleSheet(
            '''
            *{background-color:#fafafa;}
            QPushButton{
                border:none;
                font-size:13px;
                text-align:left;
                padding-left:30px;
                height:70px;
             }
            QPushButton:hover{
                background:red;
            }
            ''')
        self.play_setting_widget.setStyleSheet(
            '''
            QLabel {
                font:bold;
                font-size:18px;
            }
            QPushButton {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
                font-size: 16px;
            }
            QLineEdit {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
            }
            '''
        )
        self.left_out.setStyleSheet(
            '''
            QPushButton { 
                text-align:right;
                padding-right:30px;
                color:#808080;
                font-size:18px;
            }
            ''')
        self.left_username.setStyleSheet(
            '''
            QPushButton { 
                text-align:left;
                padding-left:30px;
                color:#ffffff;
                font-size:14px;
            }
            ''')

        self.play_widget.setStyleSheet(
            '''
            *{background-color:#f2f2f2;}
            QPushButton {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
                font-size: 14px;
            }
            ''')
        self.view_record_widget.setStyleSheet(
            '''
            QPushButton {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
                font-size: 14px;
            }
            QTextEdit {
                border-radius: 10px;
                border: 2px groove gray;
                border-style: outset;
                font-size: 14px;
            }
            '''
        )
        self.game_record_table_view.setStyleSheet(
            '''
            border-radius: 10px;
            border: 2px groove gray;
            border-style: outset;
            font-size: 14px;
            '''
        )


if __name__ == '__main__':
    games = funcs.get_games("")
    # QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    level_gui = ChooseLevelWindow()
    gui.btn_choose_level.clicked.connect(level_gui.show)

    gui.show()
    sys.exit(app.exec_())
