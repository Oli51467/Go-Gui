# Go-Gui
嵌入式版围棋图形界面，串口通信

安装Docker 官方文档
### 创建环境容器
#### 1. 拉取一个ubuntu镜像作为基础系统 --platform 指定系统架构
```
docker pull ubuntu:20.04 --platform linux/arm
```
#### 2. 利用该镜像制作一个容器
```
docker create --name pyqt_arm -it ubuntu:20.04
```
#### 3. 启动容器
```
docker start pyqt_arm
```
#### 4. 进入容器
```
docker attach pyqt_arm
```
### 配置容器环境
#### 1. 更新
```
sudo apt-get update
```
#### 2. 安装必要的工具
```
apt-get install tmux
apt-get install ssh
apt-get install vim 
apt-get install git
```
#### 3. 安装python环境
```
python3 -V # 查看python3版本 ssh会自动安装python3.8
```
```
ln -sf /usr/bin/python3.8 /usr/bin/python3 # 建立软连接
```
#### 4. 安装pip3
```
sudo apt-get update
sudo apt-get install python3-pip
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple # 换源
pip3 -V # 查看pip3版本
```
#### 5. 安装PyQt5环境
```
sudo apt-get update # 更新
sudo python3 -m pip3 install --upgrade pip # 更新pip3
sudo apt-get install python3.8-dev 
sudo apt install pyqt5*		# 安装pyqt5依赖
sudo apt install qt5-default qttools5-dev-tools
sudo pip3 install pyqt5
```
#### 6. 安装其他环境和依赖包
```
pip3 install matplotlib
pip3 install pyserial
pip3 install sqlalchemy
pip3 install pymysql
pip3 install qtawesome
```
#### 7. 下载中文字库
准备： 下载一个中文字库，例如 syht.ttf，放到容器内，假设路径为$PATH2TTF
在用户目录下补充中文字体，并刷新字体
```
cd ~/.local/share
mkdir fonts
cd fonts
mkdir myfonts
cp $PATH_TO_TTF ./
mkfontscale
mkfontdir
fc-cache -fv
```
#### 8. 配置中文环境
```
检查容器支持的语言环境
locale -a
修改配置文件
sudo vim /etc/profile
# 添加以下内容
export LANG=zh_CN.UTF-8
source /etc/profile
```
### 创建镜像
#### 1. 退出容器
```ctrl + d```
#### 2. 创建容器的镜像：CONTAINER为容器名，如pyqt_arm。IMAGE_NAME:TAG为构建的镜像名。
```
docker commit CONTAINER IMAGE_NAME:TAG
```
#### 3. 将创建的镜像导出到本地文件中
```
docker save -o IMAGE_NAME.tar IMAGE_NAME:TAG
```
#### 4. 将镜像文件拷贝到开发板上

### 加载镜像
#### 1. ssh到开发板上，进入开发板终端
#### 2. 将镜像从文件中加载出来
```
docker load -i IMAGE_NAME.tar
```
#### 3. 查看本地镜像
```
docker images
```

### 配置显示回调
#### 1. 安装XServer
```
sudo apt install x11-xserver-utils
```
#### 2. 增加许可网络连接
```
sudo vim /etc/lightdm/lightdm.conf # 在lightdm.conf中添加如下内容：
[SeatDefaults]
xserver-allow-tcp=true
```
#### 3. 重启XServer
```
sudo systemctl restart lightdm
```
#### 4. 查看当前显示的环境变量值 必须在显示屏的终端查看，其他ssh终端无效
```
echo $DISPLAY # 假设为 0.0
# 或者通过socket文件分析
ll /tmp/.X11-unix/ # 假设为 0.0
```
#### 5. 查看开发板的ip地址
```
# 接入网线
ifconfig
```

### 创建容器并进入开发环境
#### 1. 创建容器 并配置显示回调
```
docker run -itd --name CONTAINER_NAME -h 开发板ip地址 --privileged \
           -v /tmp/.X11-unix:/tmp/.X11-unix  \
           -e DISPLAY=$DISPLAY IMAGE_NAME
```
其中CONTAINER_NAME为要创建的容器的名称，自定义。
IMAGE_NAME为镜像名。
¥DISPLAY为显示的环境变量值
#### 2. 查看容器是否被成功创建
```
docker ps
```
#### 3. 进入容器
```
docker attach CONTAINER_NAME
```
#### 4. 查看环境是否正确配置
```
python3 -V
Python 3.8.10
python3 # 进入交互命令行
>>> import PyQt5, matplotlib, pymysql, ...
>>> 
```
#### 5. git clone项目代码
#### 6. 进入项目目录 尝试运行
```
python myui.py
```
若报错：qt.qpa.plugin:Could not load the Qt platform plugin “xcb“，参考：
Ubuntu18.04下解决Qt出现qt.qpa.plugin:Could not load the Qt platform plugin “xcb“问题

### 开发版修改竖屏
#### 1. 非持久化修改
```
xrandr -o left #向左旋转90度，用于横屏转竖屏
xrandr -o right #向右旋转90度
xrandr -o inverted #上下翻转
xrandr -o normal #正常显示
```
#### 2. 持久化修改
```
sudo vim /etc/X11/Xsession.d/55gnome-session_gnomerc
```
在打开的文件末端添加
```
xrandr  --output HDMI-1 --rotate left
```
#### 3. 触摸板触摸位置跟随修改
1. 进入目录/usr/share/X11/xorg.conf.d/
```
cd /usr/share/X11/xorg.conf.d/
```
2. 将文件40-libinput.conf复制到/etc/X11/xorg.conf.d/目录下，一开始xorg.conf.d这个目录在/etc/X11可能没有，需要自己创建。
```
sudo mkdir /etc/X11/xorg.conf.d # 如果没有目录则创建
sudo cp ./40-libinput.conf /etc/X11/xorg.conf.d/
```
3. 修改40-libinput.conf
```
sudo vim /etc/X11/xorg.conf.d/40-libinput.conf
```
4. 找到touchscreen section，在Identifier下添加一行 Option “CalibrationMatrix” “你的校准矩阵”。具体参数如下：
- 90度   "0 -1 1 1 0 0 0 0 1"
- 180度  "-1 0 1 0  -1  1 0 0 1"
- 270度 "0 1 0  -1 0 1 0 0 1"
- x，y对调  "-1 0 1 1 0  0  0 0 1"
40-libinput.conf完整代码如下：
```
# Match on all types of devices but joysticks
Section "InputClass"
        Identifier "libinput pointer catchall"
        MatchIsPointer "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection
 
Section "InputClass"
        Identifier "libinput keyboard catchall"
        MatchIsKeyboard "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection
 
Section "InputClass"
        Identifier "libinput touchpad catchall"
        MatchIsTouchpad "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection
 
Section "InputClass"
        Identifier "libinput touchscreen catchall"
	Option "CalibrationMatrix" "0 -1 1 1 0 0 0 0 1"
        MatchIsTouchscreen "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection
 
Section "InputClass"
        Identifier "libinput tablet catchall"
        MatchIsTablet "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection
```
