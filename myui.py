from PyQt5 import QtWidgets, QtGui
import sys
import qtawesome
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QMessageBox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fc

from funcs import draw_stars, change_color, switch, check_information_correct
from main import draw_grids

global USER_NAME


def login(self, user_name, password):
    print(user_name, password)
    global USER_NAME
    result = check_information_correct(user_name, password)
    print(result)
    if result == "success":
        USER_NAME = user_name
        QMessageBox.information(self, "成功", "登陆成功", QMessageBox.Yes)
        self.left_widget_enter.setVisible(False)
        self.left_widget_user_name.setVisible(True)
    elif result == "userNameNotExist":
        QMessageBox.critical(self, "错误", "用户名不存在，请先注册")
    elif result == "wrongPassword":
        QMessageBox.critical(self, "错误", "密码错误")


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_image = QLabel(self)
        self.label_username = QtWidgets.QLabel("用户名")
        self.text_username = QtWidgets.QLineEdit()
        self.label_password = QtWidgets.QLabel("密码")
        self.text_password = QtWidgets.QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)
        self.btn_login = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "登陆")
        self.btn_login.clicked.connect(lambda: login(self, self.text_username.text(), self.text_password.text()))
        self.btn_login.setFixedSize(200, 50)
        png = QtGui.QPixmap('images/login_image.png')
        self.label_image.setScaledContents(True)  # 需要在图片显示之前进行设置
        self.label_image.setPixmap(png)
        self.label_image.setFixedSize(300, 300)

        self.right_widget = QtWidgets.QWidget()  # 右侧部件
        self.right_widget.setObjectName('right_layout')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        self.right_layout.addWidget(self.label_username, 0, 0, 1, 1)
        self.right_layout.addWidget(self.text_username, 0, 1, 1, 3)
        self.right_layout.addWidget(self.label_password, 1, 0, 1, 1)
        self.right_layout.addWidget(self.text_password, 1, 1, 1, 3)
        self.right_layout.addWidget(self.btn_login, 2, 1, 1, 2)

        self.main_layout.addWidget(self.label_image, 0, 0, 1, 1)
        self.main_layout.addWidget(self.right_widget, 0, 1, 1, 1)
        self.setFixedSize(600, 300)
        self.setLayout(self.main_layout)


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_username = QtWidgets.QLabel("用户名")
        self.text_username = QtWidgets.QLineEdit()
        self.label_phone = QtWidgets.QLabel("手机号")
        self.text_phone = QtWidgets.QLineEdit()
        self.label_email = QtWidgets.QLabel("邮箱")
        self.text_email = QtWidgets.QLineEdit()
        self.label_password = QtWidgets.QLabel("密码")
        self.text_password = QtWidgets.QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)
        self.label_password_confirm = QtWidgets.QLabel("确认密码")
        self.text_password_confirm = QtWidgets.QLineEdit()
        self.text_password_confirm.setEchoMode(QLineEdit.Password)
        self.btn_login = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "注册")
        self.btn_login.setFixedSize(200, 50)
        self.label_image = QLabel(self)
        png = QtGui.QPixmap('images/register_image.png')
        self.label_image.setScaledContents(True)  # 需要在图片显示之前进行设置
        self.label_image.setPixmap(png)
        self.label_image.setFixedSize(300, 300)

        self.right_widget = QtWidgets.QWidget()  # 右侧部件
        self.right_widget.setObjectName('right_layout')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        self.right_layout.addWidget(self.label_username, 0, 0, 1, 1)
        self.right_layout.addWidget(self.text_username, 0, 1, 1, 3)
        self.right_layout.addWidget(self.label_phone, 1, 0, 1, 1)
        self.right_layout.addWidget(self.text_phone, 1, 1, 1, 3)
        self.right_layout.addWidget(self.label_email, 2, 0, 1, 1)
        self.right_layout.addWidget(self.text_email, 2, 1, 1, 3)
        self.right_layout.addWidget(self.label_password, 3, 0, 1, 1)
        self.right_layout.addWidget(self.text_password, 3, 1, 1, 3)
        self.right_layout.addWidget(self.label_password_confirm, 4, 0, 1, 1)
        self.right_layout.addWidget(self.text_password_confirm, 4, 1, 1, 3)
        self.right_layout.addWidget(self.btn_login, 5, 1, 1, 2)

        self.main_layout.addWidget(self.label_image, 0, 0, 1, 1)
        self.main_layout.addWidget(self.right_widget, 0, 1, 1, 1)
        self.setFixedSize(600, 300)
        self.setLayout(self.main_layout)


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def begin_play(self):
        self.play_setting_widget.setVisible(False)
        self.play_func_widget.setVisible(True)

    def init_ui(self):
        self.fig = plt.Figure()  # 公共属性figure
        self.canvas = fc(self.fig)  # 新建画布，在画布上构建matplotlib图像
        self.fig.patch.set_facecolor((0.85, 0.64, 0.45))  # 背景颜色 可调
        self.ax = self.fig.add_subplot()  # 轴的相对位置
        self.ax.set_axis_off()  # 关闭坐标系显示
        draw_grids(self.ax)  # 画棋盘格
        draw_stars(self.ax)
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

        # 未登陆时显示登陆和注册组件布局
        self.left_widget_enter = QtWidgets.QWidget()  # 创建左上侧部件
        self.left_widget_enter.setObjectName('enter_widget')
        self.left_layout_enter = QtWidgets.QGridLayout()  # 创建左上侧部件的网格布局层
        self.left_widget_enter.setLayout(self.left_layout_enter)  # 设置左上侧部件布局为网格

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
        self.index_image.setFixedSize(300, 300)

        # 按钮
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('mdi6.axe-battle', color='#2c3a45'), "对弈")
        self.left_button_1.setObjectName('play')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.database', color='#2c3a45'), "棋谱")
        self.left_button_2.setObjectName('game')

        self.btn_login = QtWidgets.QPushButton(qtawesome.icon('mdi6.axe-battle', color='#2c3a45'), "登陆")
        self.btn_register = QtWidgets.QPushButton(qtawesome.icon('mdi6.axe-battle', color='#2c3a45'), "注册")
        self.btn_login.setFixedSize(120, 70)
        self.btn_register.setFixedSize(120, 70)
        self.left_layout_enter.addWidget(self.btn_login, 0, 1, 1, 1)
        self.left_layout_enter.addWidget(self.btn_register, 0, 2, 1, 1)

        self.left_layout2.addWidget(self.left_button_1, 0, 0, 1, 3)
        self.left_layout2.addWidget(self.left_button_2, 1, 0, 1, 3)

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
        self.play_layout.addWidget(self.canvas, 0, 0, 12, 10)  # 添加棋盘画布

        self.game_record_widget = QtWidgets.QWidget()
        self.game_record_widget.setObjectName('game_record_widget')
        self.game_record_layout = QtWidgets.QGridLayout()
        self.game_record_widget.setLayout(self.game_record_layout)  # 设置index部件布局为网格
        self.game_record_label = QtWidgets.QLabel("index")
        self.game_record_layout.addWidget(self.game_record_label, 1, 1, 2, 2)
        self.game_record_widget.setVisible(False)  # 默认不显示

        # 右边栏 下棋时的按钮
        self.btn_count = QtWidgets.QPushButton(qtawesome.icon('msc.git-pull-request', color='#2c3a45'), "申请数子")
        self.btn_resign = QtWidgets.QPushButton(qtawesome.icon('mdi6.close-box', color='#2c3a45'), "认输")
        self.btn_peace = QtWidgets.QPushButton(qtawesome.icon('ph.handshake-light', color='#2c3a45'), "和棋")
        self.btn_count.setFixedSize(160, 70)
        self.btn_resign.setFixedSize(160, 70)
        self.btn_peace.setFixedSize(160, 70)

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
        self.edit_rules = QLineEdit("分先")
        self.edit_rules.setReadOnly(True)
        self.edit_komi = QLineEdit("黑贴3又3/4子")
        self.edit_komi.setReadOnly(True)

        self.btn_play = QtWidgets.QPushButton(qtawesome.icon('mdi.language-go', color='#2c3a45'), "开始下棋")
        self.btn_play.setFixedSize(160, 70)
        #self.play_widget.setFixedSize(700, 700)

        self.play_setting_widget = QtWidgets.QWidget()
        self.play_setting_widget.setObjectName('play_setting_widget')
        self.play_setting_layout = QtWidgets.QGridLayout()
        self.play_setting_widget.setLayout(self.play_setting_layout)
        self.play_setting_layout.addWidget(self.label_rules, 1, 0, 1, 1)
        self.play_setting_layout.addWidget(self.edit_rules, 1, 1, 1, 1)
        self.play_setting_layout.addWidget(self.edit_komi, 2, 1, 1, 1)
        self.play_setting_layout.addWidget(self.btn_play, 10, 1, 1, 1)
        self.btn_play.clicked.connect(self.begin_play)

        self.left_layout.addWidget(self.left_widget_enter, 0, 0, 3, 3)  # 左侧部件在第0行第0列，占3行3列
        self.left_layout.addWidget(self.left_widget2, 3, 0, 2, 3)  # 左侧部件在第3行第0列，占2行3列
        self.left_layout.addWidget(self.left_widget3, 9, 0, 6, 3)  # 左侧部件在第9行第0列，占6行3列

        self.main_layout.addWidget(self.left_widget, 1, 0, 12, 3)  # 左侧部件在第1行第0列，占12行2列
        self.main_layout.addWidget(self.play_widget, 1, 3, 12, 7)  # 右侧部件在第1行第3列，占12行9列
        self.main_layout.addWidget(self.game_record_widget, 1, 3, 12, 7)  # 右侧部件在第1行第2列，占12行9列
        self.main_layout.addWidget(self.play_func_widget, 1, 10, 12, 2)
        self.main_layout.addWidget(self.play_setting_widget, 1, 10, 12, 2)
        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 12)  # 头部侧部件在第0行第0列，占1行11列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_layout.setVerticalSpacing(0)
        self.main_layout.setSpacing(0)
        self.top_layout.setSpacing(0)
        self.left_layout.setSpacing(0)
        self.left_layout2.setSpacing(0)
        self.left_layout3.setSpacing(0)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout_enter.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        self.left_layout3.setContentsMargins(0, 0, 0, 0)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.left_button_1.clicked.connect(
            lambda: change_color(self.left_button_1, self.left_button_2))
        self.left_button_2.clicked.connect(
            lambda: change_color(self.left_button_2, self.left_button_1))

        self.left_button_1.clicked.connect(lambda: switch(self.play_widget, self.game_record_widget))
        self.left_button_1.clicked.connect(lambda: switch(self.play_setting_widget))
        self.left_button_2.clicked.connect(lambda: switch(self.game_record_widget, self.play_widget, self.play_func_widget,
                                                          self.play_setting_widget))

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
            QPushButton:hover{background:#e6e6e6;}
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
    login_window = LoginWindow()
    register_window = RegisterWindow()
    gui.btn_login.clicked.connect(login_window.show)
    gui.btn_register.clicked.connect(register_window.show)
    gui.show()
    sys.exit(app.exec_())
