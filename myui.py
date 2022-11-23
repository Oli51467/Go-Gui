from PyQt5 import QtCore, QtWidgets
import sys
import qtawesome
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fc

from main import draw_grids, draw_star_points


def change_color(button_pressed, button_not_pressed):
    button_pressed.setStyleSheet(
        '''
        *{background-color:#e6e6e6;}
        ''')
    button_not_pressed.setStyleSheet(
        '''
        *{background-color:#ffffff;}
        ''')


def switch(hide_widget, show_widget):
    hide_widget.setVisible(False)
    show_widget.setVisible(True)


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.fig = plt.Figure()  # 公共属性figure
        self.canvas = fc(self.fig)  # 新建画布，在画布上构建matplotlib图像
        self.fig.patch.set_facecolor((0.85, 0.64, 0.45))  # 背景颜色 可调
        ax = self.fig.add_subplot()  # 轴的相对位置
        ax.set_axis_off()  # 关闭坐标系现实
        draw_grids(ax)  # 画棋盘格
        # 画星位
        for i in range(3, 16, 6):
            for j in range(3, 16, 6):
                draw_star_points(ax, i, j)
        self.canvas.draw()  # 这里调用才能在画布上现实
        self.setFixedSize(1200, 800)
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

        self.left_widget1 = QtWidgets.QWidget()  # 创建左上侧部件
        self.left_widget1.setObjectName('left_widget1')
        self.left_layout1 = QtWidgets.QGridLayout()  # 创建左上侧部件的网格布局层
        self.left_widget1.setLayout(self.left_layout1)  # 设置左上侧部件布局为网格

        self.left_widget2 = QtWidgets.QWidget()  # 创建左中侧部件
        self.left_widget2.setObjectName('left_widget2')
        self.left_layout2 = QtWidgets.QGridLayout()  # 创建左中侧部件的网格布局层
        self.left_widget2.setLayout(self.left_layout2)  # 设置左中侧部件布局为网格

        self.left_widget3 = QtWidgets.QWidget()  # 创建左下侧部件-占位
        self.left_widget3.setObjectName('left_widget3')
        self.left_layout3 = QtWidgets.QGridLayout()  # 创建左下侧部件的网格布局层-占位
        self.left_widget3.setLayout(self.left_layout3)  # 设置左下侧部件布局为网格-占位

        self.btn_play = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "开始下棋")
        self.btn_count = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "申请数子")
        self.btn_resign = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "认输")
        self.btn_peace = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "和棋")
        self.btn_play.setFixedSize(160, 70)
        self.btn_count.setFixedSize(160, 70)
        self.btn_resign.setFixedSize(160, 70)
        self.btn_peace.setFixedSize(160, 70)
        self.play_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.play_widget.setObjectName('play_widget')
        self.play_layout = QtWidgets.QGridLayout()
        self.play_widget.setLayout(self.play_layout)  # 设置右侧部件布局为网格
        self.play_layout.addWidget(self.canvas, 0, 0, 12, 10)  # 添加棋盘画布
        self.play_layout.addWidget(self.btn_play, 1, 12, 1, 1)
        self.play_layout.addWidget(self.btn_count, 1, 12, 4, 1)
        self.play_layout.addWidget(self.btn_resign, 1, 12, 7, 1)
        self.play_layout.addWidget(self.btn_peace, 1, 12, 10, 1)
        self.play_widget.setVisible(False)

        self.index_widget = QtWidgets.QWidget()  # 创建index部件
        self.index_widget.setObjectName('index_widget')
        self.index_layout = QtWidgets.QGridLayout()
        self.index_widget.setLayout(self.index_layout)  # 设置index部件布局为网格
        self.index_label = QtWidgets.QLabel("index")
        self.index_layout.addWidget(self.index_label, 1, 1, 2, 2)

        self.left_layout.addWidget(self.left_widget1, 0, 0, 3, 3)  # 左侧部件在第0行第0列，占3行3列
        self.left_layout.addWidget(self.left_widget2, 3, 0, 2, 3)  # 左侧部件在第3行第0列，占2行3列
        self.left_layout.addWidget(self.left_widget3, 9, 0, 6, 3)  # 左侧部件在第9行第0列，占6行3列

        self.main_layout.addWidget(self.left_widget, 1, 0, 12, 3)  # 左侧部件在第1行第0列，占12行2列
        self.main_layout.addWidget(self.play_widget, 1, 3, 12, 9)  # 右侧部件在第1行第2列，占12行9列
        self.main_layout.addWidget(self.index_widget, 1, 3, 12, 9)  # 右侧部件在第1行第2列，占12行9列
        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 12)  # 头部侧部件在第0行第0列，占1行11列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_layout.setVerticalSpacing(0)
        self.main_layout.setSpacing(0)
        self.top_layout.setSpacing(0)
        self.left_layout.setSpacing(0)
        self.left_layout2.setSpacing(0)
        self.left_layout3.setSpacing(0)
        self.play_layout.setSpacing(0)

        self.left_out = QtWidgets.QPushButton(qtawesome.icon('fa.sign-out', color='#808080'), "退出登录")
        self.left_out.setObjectName('left_out')
        self.left_out.clicked.connect(self.close)  # 点击按钮之后关闭窗口

        self.left_username = QtWidgets.QLabel("Gobot")
        self.left_username.setObjectName('App')

        # 按钮
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='#2c3a45'), "首页")
        self.left_button_1.setObjectName('home')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "对弈")
        self.left_button_2.setObjectName('play')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "难度")
        self.left_button_3.setObjectName('level')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='#2c3a45'), "棋谱")
        self.left_button_4.setObjectName('game')

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("UserName")  # 设置按钮文本
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        # 按钮布局位置
        self.left_layout1.addWidget(self.recommend_button_1, 0, 0, 1, 1)

        self.left_layout2.addWidget(self.left_button_1, 0, 0, 1, 3)
        self.left_layout2.addWidget(self.left_button_2, 1, 0, 1, 3)
        self.left_layout2.addWidget(self.left_button_3, 2, 0, 1, 3)
        self.left_layout2.addWidget(self.left_button_4, 3, 0, 1, 3)

        self.top_layout.addWidget(self.left_username, 0, 0, 1, 15)
        self.top_layout.addWidget(self.left_out, 0, 16, 1, 1)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout1.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        self.left_layout3.setContentsMargins(0, 0, 0, 0)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.left_button_2.clicked.connect(lambda: change_color(self.left_button_2, self.left_button_1))
        self.left_button_2.clicked.connect(lambda: switch(self.index_widget, self.play_widget))
        self.left_button_1.clicked.connect(lambda: switch(self.play_widget, self.index_widget))
        self.left_button_1.clicked.connect(lambda: change_color(self.left_button_1, self.left_button_2))

        self.left_button_1.setStyleSheet(
            '''
            *{background-color:#e6e6e6;}
            ''')

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
        self.index_widget.setStyleSheet(
            '''
            QLabel{
            border:none;
            font-size:23px;
            font-weight:500;
            color:#2c3a45;
            padding-left:30px;
             }
            ''')
        self.left_widget1.setStyleSheet(
            '''
            *{color:#2c3a45;}
    
            QToolButton{
            border:none;
            font-weight:600;
            font-size:14px;
            }
            ''')
        self.left_widget2.setStyleSheet(
            '''
            QPushButton:hover{background:#e6e6e6;}
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
            QPushButton:hover{background:red;}
            ''')
        self.left_out.setStyleSheet(
            '''
            QPushButton{ text-align:right;padding-right:30px;color:#808080;font-size:14px;}
            ''')
        self.left_username.setStyleSheet(
            '''
            QPushButton{ text-align:left;padding-left:30px;color:#ffffff;font-size:16px;}
            ''')

        self.play_widget.setStyleSheet(
            '''
            *{background-color:#f2f2f2;}
            ''')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
