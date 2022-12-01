import numpy as np
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import qtawesome
from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QComboBox, QListView, QHeaderView, QAbstractItemView, \
    QTableWidget, QTableWidgetItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fc

import funcs
from funcs import draw_stars, change_color, draw_grids
from go.models import Board, WIDTH

global USER_NAME
INIT = False
levels = ["1段", "2段", "3段", "4段", "5段"]
games = []
code_map = []
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500
BUTTON_HEIGHT, BUTTON_WIDTH = 40, 150
CENTER_HEIGHT, CENTER_WIDTH = 460, 460
OP_BUTTON_HEIGHT, OP_BUTTON_WIDTH = 50, 180
OP_ICON_HEIGHT, OP_ICON_WIDTH = 25, 25


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def begin_play(self):
        self.play_setting_widget.setVisible(False)
        self.play_func_widget.setVisible(True)
        self.left_button_2.setEnabled(False)
        self.left_button_1.setEnabled(False)
        # TODO：串口检测 打开串口
        self.port_check()
        print(funcs.LEVEL)
        print(funcs.PLAYER)

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
        message = QMessageBox.question(self, '退出', '你确定要认输吗?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if message == QMessageBox.Yes:
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

    def change_level(self, i):
        funcs.LEVEL = i

    def draw_origin_play_board(self):
        self.fig = plt.Figure()  # 公共属性figure
        self.canvas = fc(self.fig)  # 新建画布，在画布上构建matplotlib图像
        self.fig.patch.set_facecolor((0.85, 0.64, 0.45))  # 背景颜色 可调
        self.ax = self.fig.add_subplot()  # 轴的相对位置
        self.ax.set_axis_off()  # 关闭坐标系显示
        draw_grids(self.ax)  # 画棋盘格
        draw_stars(self.ax)
        self.canvas.draw()  # 这里调用才能在画布上显示

    def draw_origin_review_board(self):
        self.fig_record = plt.Figure()
        self.canvas_record = fc(self.fig_record)
        self.fig_record.set_facecolor((0.85, 0.64, 0.45))
        self.ax_record = self.fig_record.add_subplot()
        self.ax_record.set_axis_off()
        draw_grids(self.ax_record)
        draw_stars(self.ax_record)
        self.canvas_record.draw()

    def draw_board(self, board_state):
        self.clear_review_board()
        for i in range(1, 20):
            for j in range(1, 20):
                if board_state[i][j] == 1:
                    self.stones_plot_review[i, j] = funcs.draw_stone(i, j, "k", self.ax_record)
                elif board_state[i][j] == 2:
                    self.stones_plot_review[i, j] = funcs.draw_stone(i, j, "w", self.ax_record)
        self.canvas_record.draw()

    def clear_review_board(self):
        for i in range(20):
            for j in range(20):
                if self.stones_plot_review[i, j] is not None:
                    self.stones_plot_review[i, j].pop().remove()
                    self.stones_plot_review[i, j] = None
        self.canvas_record.draw()

    def on_game_click(self, Item=None):
        # 如果单元格对象为空
        if Item is None:
            return
        else:
            funcs.ROW_CLICK = Item.row()  # 获取行数
            # print(code_map[Item.row()])
            self.game_record_table_view.setVisible(False)
            self.view_record_widget.setVisible(True)
            self.cur_pointer, self.undo_pointer = 0, 0
            self.game_item_row = Item.row()
            self.board_review = Board(WIDTH, WIDTH, 0)

    def back2select_game(self):
        self.clear_review_board()
        self.view_record_widget.setVisible(False)
        self.select_record_widget.setVisible(True)
        self.game_record_table_view.setVisible(True)

    def press_proceed(self):
        print("cur_pointer: %s, undo_pointer:%s" % (self.cur_pointer, self.undo_pointer))
        if self.undo_pointer < self.cur_pointer:
            self.redo()
        else:
            if self.cur_pointer >= len(code_map[self.game_item_row]):
                return
            self.proceed()

    def proceed(self):
        player = self.board_review.get_player()
        self.board_review.play(code_map[self.game_item_row][self.cur_pointer][0],
                               code_map[self.game_item_row][self.cur_pointer][1], player)
        self.board_review.next_player()
        index_x, index_y = code_map[self.game_item_row][self.cur_pointer][0], code_map[self.game_item_row][self.cur_pointer][1]
        print(index_x, index_y)
        self.stones_plot_review[index_x, index_y] = funcs.draw_stone(index_y - 1, 19 - index_x,
                                                                     'k' if player.get_identifier() == 1 else 'w',
                                                                     self.ax_record)
        captured_stones = self.board_review.captured_stones
        for stones in captured_stones:
            self.stones_plot_review[stones.x, stones.y].pop().remove()  # remove the plot
            self.stones_plot_review[stones.x, stones.y] = None
        self.canvas_record.draw()
        self.cur_pointer += 1
        self.undo_pointer += 1

    def press_undo(self):
        print("cur_pointer: %s, undo_pointer:%s" % (self.cur_pointer, self.undo_pointer))
        if self.cur_pointer <= 0 or self.undo_pointer <= 0:
            return
        self.undo()

    def undo(self):
        last_move = self.board_review.get_point(self.board_review.game_record.get_last_turn().x,
                                                self.board_review.game_record.get_last_turn().y)
        self.stones_plot_review[last_move.x, last_move.y].pop().remove()  # remove the plot
        self.stones_plot_review[last_move.x, last_move.y] = None
        captured_stones = self.board_review.game_record.get_last_turn().captured_stones
        for stones in captured_stones:
            self.stones_plot_review[stones.x, stones.y] = funcs.draw_stone(stones.y - 1, 19 - stones.x, "k" if self.board_review.get_player().get_identifier() == 1 else "w", self.ax_record)
        self.board_review.undo()
        self.canvas_record.draw()
        self.undo_pointer -= 1

    def redo(self):
        self.board_review.redo()
        captured_stones = self.board_review.game_record.get_last_turn().captured_stones
        for stones in captured_stones:
            self.stones_plot_review[stones.x, stones.y].pop().remove()  # remove the plot
            self.stones_plot_review[stones.x, stones.y] = None
        last_move = self.board_review.get_point(self.board_review.game_record.preceding.peek().x,
                                                self.board_review.game_record.preceding.peek().y)
        self.stones_plot_review[last_move.x, last_move.y] = funcs.draw_stone(last_move.y - 1, 19 - last_move.x,
                                                                             'k' if self.board_review.get_player().get_identifier() == 2 else 'w',
                                                                             self.ax_record)
        self.undo_pointer += 1
        self.canvas_record.draw()

    def press_fast_proceed(self):
        for i in range(7):
            if self.undo_pointer < self.cur_pointer:
                self.redo()
            else:
                if self.cur_pointer >= len(code_map[self.game_item_row]):
                    return
                self.proceed()

    def press_fast_undo(self):
        for i in range(7):
            if self.cur_pointer <= 0:
                return
            self.undo()

    def init_ui(self):
        self.timer = QTimer(self)
        self.stones_plot_review = np.full((20, 20), None)
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
        self.btn_count = QtWidgets.QPushButton(qtawesome.icon('msc.git-pull-request', color='#2c3a45'), "申请数子")
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
        self.label_rules = QLabel("规则")
        self.label_level = QLabel("选择段位")
        self.edit_rules = QLineEdit("分先")
        self.edit_rules.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_rules.setReadOnly(True)
        self.edit_size = QLineEdit("19路棋盘")
        self.edit_size.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_size.setReadOnly(True)
        self.edit_komi = QLineEdit("黑贴3又3/4子")
        self.edit_komi.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.edit_komi.setReadOnly(True)
        self.comboBox_level = QComboBox(self)
        self.comboBox_level.addItems(levels)
        self.comboBox_level.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.comboBox_level.setStyleSheet("QAbstractItemView::item {height: 70px;}")
        self.comboBox_level.setView(QListView())
        # 信号
        # self.comboBox_level.currentIndexChanged[str].connect(self.change_level)  # 条目发生改变，发射信号，传递条目内容
        self.comboBox_level.currentIndexChanged[int].connect(self.change_level)  # 条目发生改变，发射信号，传递条目索引

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
        self.game_record_table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.game_record_table_view.setColumnCount(1)
        self.game_record_table_view.setRowCount(5)
        self.game_record_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.game_record_table_view.itemClicked.connect(self.on_game_click)
        for index in range(len(games)):
            item = QTableWidgetItem(games[index]['play_info'] + "\n" + games[index]['result'])
            # 设置每个位置的文本值
            code_map.append(funcs.get_all_moves_and_merge(games[index]['code']))
            self.game_record_table_view.setItem(index, 0, item)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.game_record_table_view.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.game_record_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.game_record_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.game_record_table_view.resizeColumnsToContents()
        self.game_record_table_view.resizeRowsToContents()
        self.game_record_table_view.setVerticalScrollBarPolicy(0)
        self.game_record_table_view.setFixedWidth(180)
        self.select_record_layout.addWidget(self.game_record_table_view, 0, 1, 1, 1)

        # 右边 查看棋谱 操作前进后退
        self.view_record_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.view_record_widget.setObjectName('view_record_widget')
        self.view_record_layout = QtWidgets.QGridLayout()
        self.view_record_widget.setLayout(self.view_record_layout)  # 设置右侧部件布局为网格
        self.view_record_widget.setVisible(False)

        # 几个操作按钮 前进按钮
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
        # 一键到底按钮

        self.view_record_layout.addWidget(self.proceed_button, 2, 1, 1, 2)
        self.view_record_layout.addWidget(self.fast_proceed_button, 3, 1, 1, 2)
        self.view_record_layout.addWidget(self.undo_button, 4, 1, 1, 2)
        self.view_record_layout.addWidget(self.fast_undo_button, 5, 1, 1, 2)
        self.view_record_layout.addWidget(self.btn_return2record, 6, 1, 1, 2)

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
        self.play_widget.setFixedSize(CENTER_HEIGHT, CENTER_WIDTH)
        self.game_record_widget.setFixedSize(CENTER_HEIGHT, CENTER_WIDTH)

        self.play_setting_widget = QtWidgets.QWidget()
        self.play_setting_widget.setObjectName('play_setting_widget')
        self.play_setting_layout = QtWidgets.QVBoxLayout()
        self.play_setting_layout.setSpacing(15)
        self.play_setting_layout.setContentsMargins(10, 20, 0, 0)
        self.play_setting_widget.setLayout(self.play_setting_layout)
        self.play_setting_layout.addWidget(self.label_rules)
        self.play_setting_layout.addWidget(self.edit_size)
        self.play_setting_layout.addWidget(self.edit_rules)
        self.play_setting_layout.addWidget(self.edit_komi)
        self.play_setting_layout.addWidget(self.btn_choose_black)
        self.play_setting_layout.addWidget(self.btn_choose_white)
        self.play_setting_layout.addWidget(self.label_level)
        self.play_setting_layout.addWidget(self.comboBox_level)
        self.play_setting_layout.addWidget(self.btn_play)
        self.play_setting_layout.addStretch()
        self.btn_play.clicked.connect(self.begin_play)

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
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

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
            font-size:23px;
            font-weight:500;
            color:#2c3a45;
            padding-left:30px;
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
                font-size: 24px;
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
                font-size:16px;
             }
            QPushButton{
                color:#ffffff;
                border:none;
                font-weight:600;
                font-size:16px;
             }
            ''')
        self.left_widget.setStyleSheet(
            '''
            *{background-color:#fafafa;}
            QPushButton{
                border:none;
                font-size:15px;
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
            }
            '''
        )
        self.left_out.setStyleSheet(
            '''
            QPushButton { 
                text-align:right;
                padding-right:30px;
                color:#808080;
                font-size:14px;
            }
            ''')
        self.left_username.setStyleSheet(
            '''
            QPushButton { 
                text-align:left;
                padding-left:30px;
                color:#ffffff;
                font-size:16px;
            }
            ''')

        self.play_widget.setStyleSheet(
            '''
            *{background-color:#f2f2f2;}
            ''')


if __name__ == '__main__':
    games = funcs.get_games("")
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
