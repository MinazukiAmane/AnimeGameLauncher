from modules.hl_utils import get_details, get_general, define, read
import modules.resources
import os
from modules.ui_message_box import message_box
from PySide6 import QtCore
import sys
import pathlib
from PySide6.QtCore import (QPoint, QSize)
from PySide6.QtGui import (QScreen, QPixmap, QIcon, QFont)
from PySide6.QtWidgets import (QApplication, QFileDialog, QDialog, QGroupBox, QLabel, QPushButton, QRadioButton, QComboBox, QScrollArea, QWidget)


class StartWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.interface()

        return None
    
    def interface(self):        
        game_name, wallpaper_name, default = get_general()
        del wallpaper_name, default

        gam_ver, ren_ver, game_loc, launcher_loc = get_details(game_name)
        del gam_ver, ren_ver


        self.setWindowTitle('AnimeGameLauncher')
        self.setWindowIcon(QIcon(':/resources/icons/app_icon.png'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(QSize(820, 525))
        screen_size = QScreen.availableGeometry(QApplication.primaryScreen())
        position_x = (screen_size.width() - self.width()) / 2
        position_y = (screen_size.height() - self.height()) / 2
        self.move(position_x, position_y)




        self.lbl_window_title = QLabel(parent=self, text='First Time Configuration', objectName='lbl_window_title')
        
        step = "Define your installation paths for " +  read(game_name, "name")
        self.lbl_current_step = QLabel(parent=self, text=step, objectName='lbl_current_step')



        self.btn_cancel = QPushButton(parent=self, text='Exit', objectName='btn_cancel', flat=True)
        self.btn_cancel.clicked.connect(self.btn_cancel_event)

        self.btn_confirm = QPushButton(parent=self, text='Continue', objectName='btn_confirm', flat=True)
        self.btn_confirm.clicked.connect(self.btn_confirm_event)



        self.lbl_path_t = QLabel(parent=self, text='1. Select the Game Folder Location', objectName='lbl_path_t')
        self.lbl_path = QLabel(parent=self, text=game_loc, objectName='lbl_path')
        
        self.lbl_launcher_path_t = QLabel(parent=self, text='2. Select the Launcher Executable Location', objectName='lbl_launcher_path_t')
        self.lbl_launcher_path = QLabel(parent=self, text=launcher_loc, objectName='lbl_launcher_path')
        


        self.btn_locate_path = QPushButton(parent=self, text=None, objectName='btn_locate_path')
        self.btn_locate_path.clicked.connect(self.btn_locate_path_event)

        self.btn_locate_launcher_path = QPushButton(parent=self, text=None, objectName='btn_locate_launcher_path')
        self.btn_locate_launcher_path.clicked.connect(self.btn_locate_launcher_path_event)


        #default_game = modules.configuration.defaultgame()

        #match default_game:
        #    case 'honkai':
        #        game_index_2 = 0
        #    case 'genshin':
        #        game_index_2 = 1
        #    case 'starrail':
        #        game_index_2 = 2
        #    case _:
        #        pass

        #self.game_list = QComboBox(parent=self.scroll_container, objectName='game_list')
        #self.game_list.addItem('Honkai Impact 3rd')
        #self.game_list.addItem('Genshin Impact')
        #self.game_list.addItem('Honkai: Star Rail')
        #self.game_list.setCurrentIndex(game_index_2)


        match game_name:
            case _:
                self.style()

        self.exec()

        return None

    def style_2(self):
        pass

    def style(self):
        background_image = ':/resources/backgrounds/first_genshin.png'
        go_down = 50

        self.background_image = QLabel(parent=self, text=None, objectName='background_image')
        self.background_image.setFixedSize(QSize(820, 525))
        self.background_image.setScaledContents(True)
        self.background_image.setPixmap(QPixmap(background_image))


        self.lbl_window_title.setFixedSize(QSize(820, 100))
        self.lbl_window_title.move(0, go_down-15)
        self.lbl_window_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_window_title.setStyleSheet(
            """
                QLabel#lbl_window_title {
                    color: rgb(57, 59, 64);
                    font: 25pt "Segoe UI";
                }
            """
        )
        self.lbl_window_title.raise_()

        self.lbl_current_step.setFixedSize(QSize(820, 100))
        self.lbl_current_step.move(0, go_down+30)
        self.lbl_current_step.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_current_step.setStyleSheet(
            """
                QLabel#lbl_current_step {
                    color: rgb(128, 128, 128);
                    font: 15pt "Segoe UI";
                }
            """
        )
        self.lbl_current_step.raise_()



        self.btn_cancel.setFixedSize(QSize(190, 48))
        self.btn_cancel.move(394, 450)
        self.btn_cancel.setStyleSheet(
            """
                QPushButton#btn_cancel, QPushButton#btn_cancel:hover, QPushButton#btn_cancel:pressed {
                    border: 1px solid rgb(204, 204, 204);
                    border-radius: 5px;
                    color: rgb(220, 188, 96);
                    font: 15pt "Segoe UI";
                    text-align: center;
                }

                QPushButton#btn_cancel {
                    background-color: rgb(255, 255, 255);
                }

                QPushButton#btn_cancel:hover {
                    background-color: rgb(251, 248, 239);
                }

                QPushButton#btn_cancel:pressed {
                    background-color: rgb(236, 233, 225);
                }
            """
        )
        self.btn_cancel.raise_()

        self.btn_confirm.setFixedSize(QSize(190, 48))
        self.btn_confirm.move(596, 450)
        self.btn_confirm.setStyleSheet(
            """
                QPushButton#btn_confirm, QPushButton#btn_confirm:hover, QPushButton#btn_confirm:pressed {
                    border-radius: 5px;
                    color: rgb(244, 216, 168);
                    font: 14pt "Segoe UI";
                    text-align: center;
                }

                QPushButton#btn_confirm {
                    background-color: rgb(57, 59, 64);
                }

                QPushButton#btn_confirm:hover {
                    background-color: rgb(77, 79, 83);
                }

                QPushButton#btn_confirm:pressed {
                    background-color: rgb(51, 53, 57);
                }
            """
        )
        self.btn_confirm.raise_()

        

        #self.lbl_default_game.setFixedSize(QSize(150, 30))
        #self.lbl_default_game.move(35, 10)
        #self.lbl_default_game.setStyleSheet(
        #    """
        #        QLabel#lbl_default_game {
        #        	color: rgb(57, 59, 64);
        #            font: 15pt  "Segoe UI";
        #        }
        #    """
        #)

        self.lbl_path_t.setFixedSize(QSize(400, 30))
        self.lbl_path_t.move(70, go_down+150)
        self.lbl_path_t.setStyleSheet(
            """
                QLabel#lbl_path_t {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )
        self.lbl_path_t.raise_()

        self.lbl_path.setFixedSize(QSize(600, 30))
        self.lbl_path.move(105, go_down+185)
        self.lbl_path.setStyleSheet(
            """
                QLabel#lbl_path {
                    color: rgb(148, 150, 153);
                    font: 10pt "Segoe UI";
                }
            """
        )
        self.lbl_path.raise_()

        self.lbl_launcher_path_t.setFixedSize(QSize(400, 30))
        self.lbl_launcher_path_t.move(70, go_down+250)
        self.lbl_launcher_path_t.setStyleSheet(
            """
                QLabel#lbl_launcher_path_t {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )
        self.lbl_launcher_path_t.raise_()

        self.lbl_launcher_path.setFixedSize(QSize(600, 30))
        self.lbl_launcher_path.move(105, go_down+285)
        self.lbl_launcher_path.setStyleSheet(
            """
                QLabel#lbl_launcher_path {
                    color: rgb(148, 150, 153);
                    font: 10pt "Segoe UI";
                }
            """
        )
        self.lbl_launcher_path.raise_()

        self.btn_locate_path.setFixedSize(QSize(30, 30))
        self.btn_locate_path.move(70, go_down+185) # 35, 160
        self.btn_locate_path.setStyleSheet(
            """
                QPushButton#btn_locate_path, QPushButton#btn_locate_path:hover, QPushButton#btn_locate_path:pressed {
                    border: 1px solid rgb(204, 204, 204);
                    border-radius: 5px;
                    color: rgb(220, 188, 96);
                    font: 13pt "Segoe UI";
                }

                QPushButton#btn_locate_path {
                    background-color: rgb(255, 255, 255);
                    background-image: url(:/resources/icons/folder/change_folder.png)
                }

                QPushButton#btn_locate_path:hover {
                    background-color: rgb(251, 248, 239);
                }

                QPushButton#btn_locate_path:pressed {
                    background-color: rgb(236, 233, 225);
                }
            """
        )
        self.btn_locate_path.raise_()

        self.btn_locate_launcher_path.setFixedSize(QSize(30, 30))
        self.btn_locate_launcher_path.move(70, go_down+285) #300, 160
        self.btn_locate_launcher_path.setStyleSheet(
            """
                QPushButton#btn_locate_launcher_path, QPushButton#btn_locate_launcher_path:hover, QPushButton#btn_locate_launcher_path:pressed {
                    border: 1px solid rgb(204, 204, 204);
                    border-radius: 5px;
                    color: rgb(220, 188, 96);
                    font: 13pt "Segoe UI";
                }

                QPushButton#btn_locate_launcher_path {
                    background-color: rgb(255, 255, 255);
                    background-image: url(:/resources/icons/folder/change_folder.png)
                }

                QPushButton#btn_locate_launcher_path:hover {
                    background-color: rgb(251, 248, 239);
                }

                QPushButton#btn_locate_launcher_path:pressed {
                    background-color: rgb(236, 233, 225);
                }
            """
        )
        self.btn_locate_launcher_path.raise_()



        #self.game_list.setFixedSize(QSize(170, 30))
        #self.game_list.move(35, 50)
        #self.game_list.setStyleSheet(
        #    """
        #        QComboBox#game_list {
        #            font: 13pt "Segoe UI";
        #        }
        #    """
        #)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

        return None

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

        return None

    def btn_locate_path_event(self):
        game_name, wallpaper_name, default = get_general()
        del wallpaper_name, default
        
        self.new_game_path = QFileDialog.getExistingDirectory(self, 'Select the game installation folder')

        if not pathlib.Path(self.new_game_path).absolute().joinpath(read(game_name, "game_exe")).is_file():
            message_box("warning", "Game executable could not be found within this directory. \nIf you don't plan to play this game, ignore this warning.")


        match self.new_game_path:
            case '' | None:
                pass
            case _:
                self.lbl_path_t.setStyleSheet("QLabel#lbl_path_t {color: rgb(107,213,149); font: 15pt 'Segoe UI';}")
                self.lbl_path.setText(self.new_game_path)

        return None

    def btn_locate_launcher_path_event(self):

        self.new_launcher_path = QFileDialog.getOpenFileName(self, 'Select the launcher executable')[0]

        match self.new_launcher_path:
            case '' | None:
                pass
            case _:
                self.lbl_launcher_path.setText(self.new_launcher_path)
                self.lbl_launcher_path_t.setStyleSheet("QLabel#lbl_launcher_path_t {color: rgb(107,213,149); font: 15pt 'Segoe UI';}")

        return None

    def btn_cancel_event(self):
        config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
        os.remove(config_file)
        sys.exit()


    def btn_confirm_event(self):
        game_name, wallpaper_name, default = get_general()

        try:
            define(game_name, "launcher_path", self.new_launcher_path)
            define(game_name, "path", self.new_game_path)
        except:
            message_box("warning", "You did not define both paths.\nIf you don't plan to play this game, ignore this warning.")


        if game_name != "honkai":
            define("general", "game", "honkai")  
            self.close()
            StartWindow()
        else:
            define("general", "game", "genshin")
            define("general", "first", 1)  
            self.close()
            
        return None

if __name__ == '__main__':
    pass

