from modules.hl_utils import update_versions, update_wallpapers, get_details, update_c_version, get_general, define, get_res, read
import os, subprocess, sys, webbrowser, pathlib, signal, time, re
import modules.ui_settings, modules.ui_message_box, modules.ui_start, modules.resources
from PySide6 import QtCore
from PySide6.QtCore import (QPoint, QSize, QRunnable, Slot, QThreadPool)
from PySide6.QtGui import (QCursor, QScreen, QPixmap, QIcon)
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QCommandLinkButton)



ui_settings = modules.ui_settings.SettingsWindow
ui_message_box = modules.ui_message_box.message_box
ui_start = modules.ui_start.StartWindow


class UpdateThread(QtCore.QThread):

    update = QtCore.Signal()
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        x = update_wallpapers()
        y = update_versions()
        z = update_c_version()
        if x or y or z:
            self.update.emit()
        else:
            pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.interface()

        self.refresh = UpdateThread()
        self.refresh.update.connect(self.update_window)
        self.refresh.start()

        return None

    def update_window(self):
        self.close()
        MainWindow()

    def interface(self):
        game_name, wallpaper_name, fst = get_general()

        self.central_widget = QMainWindow()
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle('AnimeGameLauncher')
        self.setWindowIcon(QIcon(':/resources/icons/app_icon.png'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(QSize(1155, 650))
        screen_size = QScreen.availableGeometry(QApplication.primaryScreen())
        position_x = (screen_size.width() - self.width()) / 2
        position_y = (screen_size.height() - self.height()) / 2
        self.move(position_x, position_y)

        self.background_image = QLabel(self, objectName='background_image')
        self.background_image.setFixedSize(QSize(1155, 650))
        wallpaper = pathlib.Path(__file__).parents[1].resolve().joinpath("backgrounds").joinpath(wallpaper_name)
        self.background_image.setPixmap(QPixmap(wallpaper))
        self.background_image.setScaledContents(True)

        self.top_bar = QLabel(self, text=None, objectName='top_bar')
        self.top_bar.setFixedSize(QSize(1155, 30))
        self.top_bar.setStyleSheet(
            """
                QLabel#top_bar {
                    background-color: rgb(20, 20, 20);
                }
            """
        )

        self.app_title = QLabel(self, text='AnimeGameLauncher', objectName='app_title')
        self.app_title.setFixedSize(QSize(150, 30))
        self.app_title.move(12, 0)
        self.app_title.setStyleSheet(
            """
                QLabel#app_title {
                    color: #FFFFFF;
                    font: 9pt "Segoe UI";
                    text-align: center;
                }
            """
        )

        self.app_version = QLabel(self, text='2.0', objectName='app_version')
        self.app_version.setFixedSize(QSize(40, 30))
        self.app_version.move(95, 0)
        self.app_version.setStyleSheet(
            """
                QLabel#app_version {
                    color: rgb(67, 67, 67);
                    font: 9pt "Segoe UI";
                }
            """
        )

        self.btn_close = QPushButton(self, text=None, objectName='btn_close', flat=True)
        self.btn_close.setFixedSize(QSize(30, 30))
        self.btn_close.move(1125, 0)
        self.btn_close.setStyleSheet(
            """
                QPushButton#btn_close, QPushButton#btn_close:hover, QPushButton#btn_close:pressed {
                    border-radius: 0px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_close {
                    background-image: url(:/resources/icons/top_bar/close/default.png);
                }

                QPushButton#btn_close:hover {
                    background-image: url(:/resources/icons/top_bar/close/hovered.png);
                }

                QPushButton#btn_close:pressed {
                    background-image: url(:/resources/icons/top_bar/close/pressed.png);
                }
            """
        )
        self.btn_close.clicked.connect(self.btn_close_event)

        self.btn_minimize = QPushButton(self, text=None, objectName='btn_minimize', flat=True)
        self.btn_minimize.setFixedSize(QSize(30, 30))
        self.btn_minimize.move(1090, 0)
        self.btn_minimize.setStyleSheet(
            """
                QPushButton#btn_minimize, QPushButton#btn_minimize:hover, QPushButton#btn_minimize:pressed {
                    border-radius: 0px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_minimize {
                    background-image: url(:/resources/icons/top_bar/minimize/default.png);
                }

                QPushButton#btn_minimize:hover {
                    background-image: url(:/resources/icons/top_bar/minimize/hovered.png);
                }

                QPushButton#btn_minimize:pressed {
                    background-image: url(:/resources/icons/top_bar/minimize/pressed.png);
                }
            """
        )
        self.btn_minimize.clicked.connect(self.showMinimized)

        self.btn_settings = QPushButton(self, text=None, objectName='btn_settings', flat=True)
        self.btn_settings.setFixedSize(QSize(30, 30))
        self.btn_settings.move(1055, 0)
        self.btn_settings.setStyleSheet(
            """
                QPushButton#btn_settings, QPushButton#btn_settings:hover, QPushButton#btn_settings:pressed {
                    border-radius: 0px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_settings {
                    background-image: url(:/resources/icons/top_bar/settings/default.png);
                }

                QPushButton#btn_settings:hover {
                    background-image: url(:/resources/icons/top_bar/settings/hovered.png);
                }

                QPushButton#btn_settings:pressed {
                    background-image: url(:/resources/icons/top_bar/settings/pressed.png);
                }
            """
        )
        self.btn_settings.clicked.connect(self.btn_settings_event)

        self.right_bar = QLabel(self, text=None, objectName='right_bar')
        self.right_bar.setFixedSize(QSize(75, 620))
        self.right_bar.move(1080, 30)
        self.right_bar.setStyleSheet(
            """
                QLabel#right_bar {
                    background-color: rgba(0, 0, 0, 0.3)
                }
            """
        )        

        self.btn_url_home = QPushButton(self, text=None, objectName='btn_url_home', flat=True)
        self.btn_url_home.setFixedSize(QSize(40, 40))
        self.btn_url_home.move(1100, 60)
        self.btn_url_home.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_home.setStyleSheet(
            """
                QPushButton#btn_url_home, QPushButton#btn_url_home:hover, QPushButton#btn_url_home:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_home:hover, QPushButton#btn_url_home:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_home {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/home/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_home:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/home/hovered.png);
                }

                QPushButton#btn_url_home:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/home/pressed.png);
                }
            """
        )
        self.btn_url_home.clicked.connect(lambda: self.btn_url_event('home'))

        self.btn_url_facebook = QPushButton(self, text=None, objectName='btn_url_facebook', flat=True)
        self.btn_url_facebook.setFixedSize(QSize(40, 40))
        self.btn_url_facebook.move(1100, 130)
        self.btn_url_facebook.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_facebook.setStyleSheet(
            """
                QPushButton#btn_url_facebook, QPushButton#btn_url_facebook:hover, QPushButton#btn_url_facebook:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_facebook:hover, QPushButton#btn_url_facebook:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_facebook {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/facebook/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_facebook:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/facebook/hovered.png);
                }

                QPushButton#btn_url_facebook:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/facebook/pressed.png);
                }
            """
        )
        self.btn_url_facebook.clicked.connect(lambda: self.btn_url_event('facebook'))

        self.btn_url_twitter = QPushButton(self, text=None, objectName='btn_url_twitter', flat=True)
        self.btn_url_twitter.setFixedSize(QSize(40, 40))
        self.btn_url_twitter.move(1100, 200)
        self.btn_url_twitter.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_twitter.setStyleSheet(
            """
                QPushButton#btn_url_twitter, QPushButton#btn_url_twitter:hover, QPushButton#btn_url_twitter:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_twitter:hover, QPushButton#btn_url_twitter:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_twitter {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/twitter/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_twitter:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/twitter/hovered.png);
                }

                QPushButton#btn_url_twitter:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/twitter/pressed.png);
                }
            """
        )
        self.btn_url_twitter.clicked.connect(lambda: self.btn_url_event('twitter'))

        self.btn_url_instagram = QPushButton(self, text=None, objectName='btn_url_instagram', flat=True)
        self.btn_url_instagram.setFixedSize(QSize(40, 40))
        self.btn_url_instagram.move(1100, 270)
        self.btn_url_instagram.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_instagram.setStyleSheet(
            """
                QPushButton#btn_url_instagram, QPushButton#btn_url_instagram:hover, QPushButton#btn_url_instagram:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_instagram:hover, QPushButton#btn_url_instagram:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_instagram {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/instagram/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_instagram:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/instagram/hovered.png);
                }

                QPushButton#btn_url_instagram:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/instagram/pressed.png);
                }
            """
        )
        self.btn_url_instagram.clicked.connect(lambda: self.btn_url_event('instagram'))

        self.btn_url_youtube = QPushButton(self, text=None, objectName='btn_url_youtube', flat=True)
        self.btn_url_youtube.setFixedSize(QSize(40, 40))
        self.btn_url_youtube.move(1100, 340)
        self.btn_url_youtube.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_youtube.setStyleSheet(
            """
                QPushButton#btn_url_youtube, QPushButton#btn_url_youtube:hover, QPushButton#btn_url_youtube:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_youtube:hover, QPushButton#btn_url_youtube:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_youtube {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/youtube/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_youtube:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/youtube/hovered.png);
                }

                QPushButton#btn_url_youtube:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/youtube/pressed.png);
                }
            """
        )
        self.btn_url_youtube.clicked.connect(lambda: self.btn_url_event('youtube'))

        self.btn_url_hoyolab = QPushButton(self, text=None, objectName='btn_url_hoyolab', flat=True)
        self.btn_url_hoyolab.setFixedSize(QSize(40, 40))
        self.btn_url_hoyolab.move(1100, 410)
        self.btn_url_hoyolab.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_hoyolab.setStyleSheet(
            """
                QPushButton#btn_url_hoyolab, QPushButton#btn_url_hoyolab:hover, QPushButton#btn_url_hoyolab:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_hoyolab:hover, QPushButton#btn_url_hoyolab:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_hoyolab {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/hoyolab/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_hoyolab:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/hoyolab/hovered.png);
                }

                QPushButton#btn_url_hoyolab:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/hoyolab/pressed.png);
                }
            """
        )
        self.btn_url_hoyolab.clicked.connect(lambda: self.btn_url_event('hoyolab'))

        self.btn_url_swap = QPushButton(self, text=None, objectName='btn_url_swap', flat=True)
        self.btn_url_swap.setFixedSize(QSize(63, 63))
        self.btn_url_swap.move(33, 487) # 20, 557
        if (game_name == 'honkai'):
            self.btn_url_swap.hide()
        elif (game_name == 'starrail'):
            self.btn_url_swap.move(33, 557)
        self.btn_url_swap.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_swap.setStyleSheet(
                """
                    QPushButton#btn_url_swap, QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        border-radius: 10px;
                        background-repeat: no-repeat;
                        background-position: center;
                    }

                    QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        background-color: rgba(20, 20, 20, 0.9);
                    }

                    QPushButton#btn_url_swap {
                        border: 2px solid rgba(255, 255, 255, 0);
                        background-image: url(:/resources/icons/change_game/honkai.png);
                        background-color: rgba(20, 20, 20, 0.6);
                    }

                    QPushButton#btn_url_swap:hover {
                        border: 2px solid rgb(255, 225, 145);
                        background-image: url(:/resources/icons/change_game/honkai.png);
                    }

                    QPushButton#btn_url_swap:pressed {
                        border: 2px solid rgb(255, 205, 125);
                        background-image: url(:/resources/icons/change_game/honkai.png);
                    }
                """
                    )
        self.btn_url_swap.clicked.connect(lambda: self.btn_url_event('honkai'))

        self.btn_url_swap2 = QPushButton(self, text=None, objectName='btn_url_swap', flat=True)
        self.btn_url_swap2.setFixedSize(QSize(63, 63))
        self.btn_url_swap2.move(33, 487) # 90, 557
        if game_name == 'genshin':
            self.btn_url_swap2.hide()
        self.btn_url_swap2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_swap2.setStyleSheet(
                """
                    QPushButton#btn_url_swap, QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        border-radius: 10px;
                        background-repeat: no-repeat;
                        background-position: center;
                    }

                    QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        background-color: rgba(20, 20, 20, 0.9);
                    }

                    QPushButton#btn_url_swap {
                        border: 2px solid rgba(255, 255, 255, 0);
                        background-image: url(:/resources/icons/change_game/genshin.png);
                        background-color: rgba(20, 20, 20, 0.6);
                    }

                    QPushButton#btn_url_swap:hover {
                        border: 2px solid rgb(255, 225, 145);
                        background-image: url(:/resources/icons/change_game/genshin.png);
                    }

                    QPushButton#btn_url_swap:pressed {
                        border: 2px solid rgb(255, 205, 125);
                        background-image: url(:/resources/icons/change_game/genshin.png);
                    }
                """
                    )
        self.btn_url_swap2.clicked.connect(lambda: self.btn_url_event('genshin'))

        self.btn_url_swap3 = QPushButton(self, text=None, objectName='btn_url_swap', flat=True)
        self.btn_url_swap3.setFixedSize(QSize(63, 63))
        self.btn_url_swap3.move(33, 557) # 90, 557
        if game_name == 'starrail':
            self.btn_url_swap3.hide()
        self.btn_url_swap3.setDisabled(False)
        self.btn_url_swap3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_url_swap3.setStyleSheet(
                """
                    QPushButton#btn_url_swap, QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        border-radius: 10px;
                        background-repeat: no-repeat;
                        background-position: center;
                    }

                    QPushButton#btn_url_swap:hover, QPushButton#btn_url_swap:pressed {
                        background-color: rgba(20, 20, 20, 0.9);
                    }

                    QPushButton#btn_url_swap {
                        border: 2px solid rgba(255, 255, 255, 0);
                        background-image: url(:/resources/icons/change_game/starrail.png);
                        background-color: rgba(20, 20, 20, 0.6);
                    }

                    QPushButton#btn_url_swap:hover {
                        border: 2px solid rgb(255, 225, 145);
                        background-image: url(:/resources/icons/change_game/starrail.png);
                    }

                    QPushButton#btn_url_swap:pressed {
                        border: 2px solid rgb(255, 205, 125);
                        background-image: url(:/resources/icons/change_game/starrail.png);
                    }
                """
                    )
        self.btn_url_swap3.clicked.connect(lambda: self.btn_url_event('starrail'))

        c_path = read(game_name, "path") + "/" + read(game_name, "game_exe")
        gameversion, currentversion, no_u, no_u_2 = get_details(game_name)
        del no_u, no_u_2 

        if game_name != 'starrail' and pathlib.Path(c_path).is_file() and re.search("\d(.)\d(.)\d", gameversion):

            if currentversion == gameversion:
                solution = 'The game is ready!'
            else:
                solution = 'New update! (' + currentversion + ')'

            gameinfo = 'Version: ' + gameversion +'\n' + solution
                       
            self.game_info = QPushButton(self, text=gameinfo, objectName='btn_game_info', flat=True)
            self.game_info.move(660, 567)
            self.game_info.setFixedSize(QSize(120, 50))
            self.game_info.setDisabled(True)
            self.game_info.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.game_info.setStyleSheet(
                """
                    QPushButton#btn_game_info, QPushButton#btn_game_info:hover, QPushButton#btn_game_info:pressed {
                        color: #FFFFFF;
                        font: 8pt "Segoe UI";
                        background-color: rgba(20, 20, 20, 0.9);
                        border-radius: 20px;
                        background-repeat: no-repeat;
                        background-position: center;
                    }
                """
            )

            self.btn_url_launcher = QPushButton(self, text='', objectName='btn_url_launcher', flat=True)
            self.btn_url_launcher.setFixedSize(QSize(40, 40)) # 40, 40
            self.btn_url_launcher.move(1100, 567) # 750, 565 para a pos inicial
            self.btn_url_launcher.hide()
            self.btn_url_launcher.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.btn_url_launcher.setStyleSheet(
            """
                QPushButton#btn_url_launcher, QPushButton#btn_url_launcher:hover, QPushButton#btn_url_launcher:pressed {
                    border-radius: 20px;
                    background-repeat: no-repeat;
                    background-position: center;
                }

                QPushButton#btn_url_launcher:hover, QPushButton#btn_url_hoyolab:pressed {
                    background-color: rgba(20, 20, 20, 0.9);
                }

                QPushButton#btn_url_launcher {
                    border: 2px solid rgba(255, 255, 255, 0);
                    background-image: url(:/resources/icons/right_bar/launcher/default.png);
                    background-color: rgba(20, 20, 20, 0.6);
                }

                QPushButton#btn_url_launcher:hover {
                    border: 2px solid rgb(255, 225, 145);
                    background-image: url(:/resources/icons/right_bar/launcher/hovered.png);
                }

                QPushButton#btn_url_launcher:pressed {
                    border: 2px solid rgb(255, 205, 125);
                    background-image: url(:/resources/icons/right_bar/launcher/pressed.png);
                }
            """
            )
            self.btn_url_launcher.clicked.connect(self.btn_launcher_event)

        
        launch_text = 'Not installed'
        
        self.btn_main_launch = QPushButton(self, text=launch_text, objectName='btn_main_launch', flat=True)
        self.btn_main_launch.setEnabled(False)

        gameversion, currentversion, no_u, no_u_2 = get_details(game_name)
        del no_u, no_u_2

        if pathlib.Path(c_path).is_file() and re.search("\d(.)\d(.)\d", gameversion):
            self.btn_main_launch.setEnabled(True)
            if (gameversion != currentversion):
                self.btn_main_launch.setText('Update')
                self.btn_main_launch.clicked.connect(self.btn_launcher_event)
            else:
                self.btn_main_launch.setText('Launch')
                self.btn_main_launch.clicked.connect(self.btn_launch_event)
            
            
        if read(game_name, "enabled") == 0:
                launch_text = 'Soon'
                self.btn_main_launch = QPushButton(self, text=launch_text, objectName='btn_main_launch', flat=True)
                self.btn_main_launch.setEnabled(False)
        
        gameversion, currentversion, no_u, no_u_2 = get_details(game_name)
        del no_u, no_u_2
        

        self.btn_main_launch.setFixedSize(QSize(240, 65))
        self.btn_main_launch.move(800, 555)
        self.btn_main_launch.setStyleSheet(
            """
                QPushButton#btn_main_launch, QPushButton#btn_main_launch:hover, QPushButton#btn_main_launch:pressed {
                    color: #704A16;
                    border-radius: 5px;
                    font: 18pt "Segoe UI";
                    text-align: center;
                }

                QPushButton#btn_main_launch {
                    background-color: #FFCF0D;
                }

                QPushButton#btn_main_launch:hover {
                    background-color: #FFD426;
                }

                QPushButton#btn_main_launch:pressed {
                    background-color: #E5BA0C;
                }
            """
        )
        

        self.background_dim = QLabel(self, text=None, objectName='background_dim')
        self.background_dim.setFixedSize(QSize(1155, 650))
        self.background_dim.move(0, 0)
        self.background_dim.setStyleSheet(
            """
                QLabel#background_dim {
                    background-color: rgba(0, 0, 0, 0.3)
                }
            """
        )
        self.background_dim.hide()

        self.show()

        return None

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

        return None

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

        return None

    def btn_settings_event(self):
        self.background_dim.show()
        ui_settings()
        self.close()
        MainWindow()
        return None

    def btn_url_event(self, destination):
        url_list = [
        'https://honkaiimpact3.mihoyo.com/global', 'https://genshin.mihoyo.com',
        'https://www.facebook.com/HonkaiImpact3rd', 'https://www.facebook.com/Genshinimpact',
        'https://twitter.com/HonkaiImpact3rd', 'https://twitter.com/GenshinImpact',
        'https://www.instagram.com/honkaiimpact3rd', 'https://www.instagram.com/genshinimpact',
        'https://www.youtube.com/channel/UCko6H6LokKM__B03i5_vBQQ', 'https://www.youtube.com/c/GenshinImpact',
        'https://www.hoyolab.com/?lang=en-us&utm_source=launcher&utm_medium=game&utm_id=1', 'https://www.hoyolab.com/genshin/?lang=en-us&utm_source=launcher&utm_medium=game&utm_id=2',
        'https://github.com/shirooo39/mihoyo_launcher','https://hsr.hoyoverse.com/'
        ]

        game_name, wallpaper_name, default = get_general()
        del wallpaper_name, default

        match game_name:
            case 'honkai':
                match destination:
                    case 'home':
                        webbrowser.open(url_list[0], new=2)
                    case 'facebook':
                        webbrowser.open(url_list[2], new=2)
                    case 'twitter':
                        webbrowser.open(url_list[4], new=2)
                    case 'instagram':
                        webbrowser.open(url_list[6], new=2)
                    case 'youtube':
                        webbrowser.open(url_list[8], new=2)
                    case 'hoyolab':
                        webbrowser.open(url_list[10], new=2)
                    case 'genshin':
                        define('general','game','genshin')
                        self.close()
                        MainWindow()
                    case 'starrail':
                        define('general','game','starrail')
                        self.close()
                        MainWindow()
                    case _:
                        pass
            case 'genshin':
                match destination:
                    case 'home':
                        webbrowser.open(url_list[1], new=2)
                    case 'facebook':
                        webbrowser.open(url_list[3], new=2)
                    case 'twitter':
                        webbrowser.open(url_list[5], new=2)
                    case 'instagram':
                        webbrowser.open(url_list[7], new=2)
                    case 'youtube':
                        webbrowser.open(url_list[9], new=2)
                    case 'hoyolab':
                        webbrowser.open(url_list[11], new=2)
                    case 'honkai':
                        define('general','game','honkai')
                        self.close()
                        MainWindow()
                    case 'starrail':
                        define('general','game','starrail')
                        self.close()
                        MainWindow() 
                    case _:
                        pass
            case 'starrail':
                match destination:
                    case 'home':
                        webbrowser.open(url_list[13], new=2)
                    case 'facebook':
                        webbrowser.open('https://www.facebook.com/HonkaiStarRail.PT', new=2)
                    case 'twitter':
                        webbrowser.open('https://twitter.com/honkaistarrail', new=2)
                    case 'instagram':
                        webbrowser.open('https://www.instagram.com/honkaistarrail/', new=2)
                    case 'youtube':
                        webbrowser.open('https://www.youtube.com/channel/UC2PeMPA8PAOp-bynLoCeMLA', new=2)
                    case 'hoyolab':
                        webbrowser.open(url_list[11], new=2)
                    case 'honkai':
                       define('general','game','honkai')
                       self.close()
                       MainWindow()
                    case 'genshin':
                        define('general','game','genshin')
                        self.close()
                        MainWindow() 
                    case _:
                        pass
            case _:
                pass
        
        return None

    def btn_launch_event(self):
        game, wallpaper_name, default = get_general()
        del wallpaper_name, default
        gam_ver, ren_ver, game_exe_path, lau_loc = get_details(game)
        del gam_ver, ren_ver, lau_loc
        screen_width, screen_height = get_res(game)

        game_exe_path += "\\" + read(game, "game_exe")
        launch_command = f'{game_exe_path} -screen-fullscreen 1 -screen-width {screen_width} -screen-height {screen_height}'

        try:
            subprocess.Popen(launch_command, shell=False, close_fds=True)
        except Exception as launch_error:
            ui_message_box(
                'error',
                f'Unable to launch the executable!\n\n' + 
                f'{launch_error}'
            )

            return None
        else:
            sys.exit(0)

    def btn_launcher_event(self):
        game, wallpaper_name, default = get_general()
        del wallpaper_name, default
        gam_ver, ren_ver, game_exe_path, launcher_exe_path = get_details(game)
        del gam_ver, ren_ver, game_exe_path
        
        launch_command = f'{launcher_exe_path}'

        try:
            subprocess.Popen(launch_command, shell=False, close_fds=True)
        except Exception as launch_error:
            ui_message_box(
                'error',
                f'Unable to open the launcher!\n\n' + 
                f'{launch_error}'
            )

            return None
        else:
            sys.exit(0)

    def btn_close_event(self):
        self.close()
        return None

if __name__ == '__main__':
    pass

