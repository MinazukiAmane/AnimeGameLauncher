from email.policy import default
from modules.hl_utils import get_details, get_res, get_general, define
import modules.resources
from modules.hl_utils import update_c_version
from PySide6 import QtCore
from PySide6.QtCore import (QPoint, QSize)
from PySide6.QtGui import (QScreen, QPixmap, QIcon, QFont)
from PySide6.QtWidgets import (QApplication, QFileDialog, QDialog, QGroupBox, QLabel, QPushButton, QRadioButton, QComboBox, QScrollArea, QWidget)


class SettingsWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.interface()

        return None
    
    def interface(self):        
        game_name, wallpaper_name, default = get_general()
        del wallpaper_name, default

        screen_width, screen_height = get_res(game_name)
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


        self.lbl_window_title = QLabel(parent=self, text='Settings', objectName='lbl_window_title')


        self.btn_close = QPushButton(parent=self, text=None, objectName='btn_close', flat=True)
        self.btn_close.clicked.connect(self.close)

        self.btn_menu_1 = QPushButton(parent=self, text='General', objectName='btn_menu_1', flat=True)
        self.btn_menu_1.clicked.connect(self.btn_menu_1_event)

        self.btn_menu_2 = QPushButton(parent=self, text='Screen resolution', objectName='btn_menu_2', flat=True)
        self.btn_menu_2.clicked.connect(self.btn_menu_2_event)

        self.btn_menu_3 = QPushButton(parent=self, text='About', objectName='btn_menu_3', flat=True)
        self.btn_menu_3.clicked.connect(self.btn_menu_3_event)

        self.btn_cancel = QPushButton(parent=self, text='Cancel', objectName='btn_cancel', flat=True)
        self.btn_cancel.clicked.connect(self.close)

        self.btn_confirm = QPushButton(parent=self, text='Confirm', objectName='btn_confirm', flat=True)
        self.btn_confirm.clicked.connect(self.btn_confirm_event)

        #
        # Defines below any items to be put inside the scroll area
        #

        self.scroll_area = QScrollArea(parent=self, objectName='scroll_area')
        self.scroll_container = QWidget(parent=self, objectName='scroll_container')
        self.scroll_area.setWidget(self.scroll_container)


        #self.lbl_default_game = QLabel(parent=self.scroll_container, text='Default game', objectName='lbl_default_game')

        self.lbl_path_t = QLabel(parent=self.scroll_container, text='Game Folder Location', objectName='lbl_path_t')
        self.lbl_path = QLabel(parent=self.scroll_container, text=game_loc, objectName='lbl_path')
        
        self.lbl_launcher_path_t = QLabel(parent=self.scroll_container, text='Launcher Executable Location', objectName='lbl_launcher_path_t')
        self.lbl_launcher_path = QLabel(parent=self.scroll_container, text=launcher_loc, objectName='lbl_launcher_path')
        
        self.lbl_screen_resolution = QLabel(parent=self.scroll_container, text='Screen resolution', objectName='lbl_screen_resolution')
        
        
        self.lbl_launcher_version = QLabel(parent=self.scroll_container, text='Launcher version', objectName='lbl_launcher_version')
        self.lbl_current_version = QLabel(parent=self.scroll_container, text='Current version: 1.1', objectName='lbl_current_version')
        self.lbl_about = QLabel(parent=self.scroll_container, text='About', objectName='lbl_about')
        source_code_url = '<a href="http://github.com/MinazukiAmane/AnimeGameLauncher" style="text-decoration: none; color: rgb(220, 188, 96); font: 13pt "Segoe UI";">View source code</a>'
        self.lbl_source_code = QLabel(parent=self.scroll_container, text=source_code_url, objectName='lbl_source_code')
        self.lbl_source_code.setOpenExternalLinks(True)

        self.btn_locate_path = QPushButton(parent=self.scroll_container, text=None, objectName='btn_locate_path')
        self.btn_locate_path.clicked.connect(self.btn_locate_path_event)

        self.btn_locate_launcher_path = QPushButton(parent=self.scroll_container, text=None, objectName='btn_locate_launcher_path')
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
        background_image = ':/resources/backgrounds/settings_genshin.png'


        self.background_image = QLabel(parent=self, text=None, objectName='background_image')
        self.background_image.setFixedSize(QSize(820, 525))
        self.background_image.setScaledContents(True)
        self.background_image.setPixmap(QPixmap(background_image))


        self.lbl_window_title.setFixedSize(QSize(150, 50))
        self.lbl_window_title.move(32, 18)
        self.lbl_window_title.setStyleSheet(
            """
                QLabel#lbl_window_title {
                    color: rgb(57, 59, 64);
                    font: 20pt "Segoe UI";
                }
            """
        )
        self.lbl_window_title.raise_()


        self.btn_close.setFixedSize(QSize(20, 20))
        self.btn_close.move(765, 35)
        self.btn_close.setStyleSheet(
            """
                QPushButton#btn_close, QPushButton#btn_close:hover, QPushButton#btn_close:pressed {
                    border: 0px solid rgba(0, 0, 0, 0);
                    border-radius: 0px;
                }

                QPushButton#btn_close {
                    background-image: url(:/resources/icons/btn_close/default.png);
                }

                QPushButton#btn_close:hover, QPushButton#btn_close:pressed {
                    background-image: url(:/resources/icons/btn_close/hovered.png);
                }
            """
        )
        self.btn_close.raise_()

        self.btn_menu_1.setFixedSize(QSize(216, 50))
        self.btn_menu_1.move(9, 87)
        self.btn_menu_1.setDown(True)
        self.btn_menu_1.setStyleSheet(
            """
                QPushButton#btn_menu_1, QPushButton#btn_menu_1:hover, QPushButton#btn_menu_1:pressed {
                    border-radius: 0px;
                    font: 13pt "Segoe UI";
                    padding-right: 97px;
                }

                QPushButton#btn_menu_1 {
                    color: rgb(117, 118, 121);
                }

                QPushButton#btn_menu_1:hover, QPushButton#btn_menu_1:pressed {
                    color: rgb(57, 59, 63);
                }

                QPushButton#btn_menu_1:pressed {
                    background-color: rgb(233, 233, 233);
                }
            """
        )
        self.btn_menu_1.raise_()

        self.btn_menu_2.setFixedSize(QSize(216, 50))
        self.btn_menu_2.move(9, 137)
        self.btn_menu_2.setDown(False)
        self.btn_menu_2.setStyleSheet(
            """
                QPushButton#btn_menu_2, QPushButton#btn_menu_2:hover, QPushButton#btn_menu_2:pressed {
                    border-radius: 0px;
                    font: 13pt "Segoe UI";
                    padding-right: 24px;
                }

                QPushButton#btn_menu_2 {
                    color: rgb(117, 118, 121);
                }

                QPushButton#btn_menu_2:hover, QPushButton#btn_menu_2:pressed {
                    color: rgb(57, 59, 63);
                }

                QPushButton#btn_menu_2:pressed {
                    background-color: rgb(233, 233, 233);
                }
            """
        )
        self.btn_menu_2.raise_()

        self.btn_menu_3.setFixedSize(QSize(216, 50))
        self.btn_menu_3.move(9, 187)
        self.btn_menu_3.setDown(False)
        self.btn_menu_3.setStyleSheet(
            """
                QPushButton#btn_menu_3, QPushButton#btn_menu_3:hover, QPushButton#btn_menu_3:pressed {
                    border-radius: 0px;
                    font: 13pt "Segoe UI";
                    padding-right: 107px;
                }

                QPushButton#btn_menu_3 {
                    color: rgb(117, 118, 121);
                }

                QPushButton#btn_menu_3:hover, QPushButton#btn_menu_3:pressed {
                    color: rgb(57, 59, 63);
                }

                QPushButton#btn_menu_3:pressed {
                    background-color: rgb(233, 233, 233);
                }
            """
        )
        self.btn_menu_3.raise_()

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

        #
        # Define styling for items in the scroll area
        #

        self.scroll_area.setFixedSize(QSize(582, 350))
        self.scroll_area.move(225, 75)
        self.scroll_area.setStyleSheet(
            """
                QScrollArea#scroll_area {
                    border: 0px;
                }

                QScrollBar::vertical {
                    border: none;
                    background-color: #FFFFFF;
                    width: 6px;
                }

                QScrollBar::handle:vertical {
                    border-radius: 3px;
                    background-color: #E9ECF0;
                }

                QScrollBar::handle:vertical:hover, QScrollBar::handle:vertical:pressed {
                    background-color: #D2D5D8;
                }
            """
        )
        self.scroll_area.raise_()

        self.scroll_container.setFixedSize(QSize(576, 990))
        self.scroll_container.move(0, 0)
        self.scroll_container.setStyleSheet(
            """
                QWidget#scroll_container {
                    background-color: #FFFFFF
                }
            """
        )


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
        self.lbl_path_t.move(35, 20)
        self.lbl_path_t.setStyleSheet(
            """
                QLabel#lbl_path_t {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )

        self.lbl_path.move(70, 55)
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
        self.lbl_launcher_path_t.move(35, 120)
        self.lbl_launcher_path_t.setStyleSheet(
            """
                QLabel#lbl_launcher_path_t {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )

        self.lbl_launcher_path.move(70, 155)
        self.lbl_launcher_path.setStyleSheet(
            """
                QLabel#lbl_launcher_path {
                    color: rgb(148, 150, 153);
                    font: 10pt "Segoe UI";
                }
            """
        )
        self.lbl_path.raise_()

        self.btn_locate_path.setFixedSize(QSize(30, 30))
        self.btn_locate_path.move(35, 50) # 35, 160
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

        self.btn_locate_launcher_path.setFixedSize(QSize(30, 30))
        self.btn_locate_launcher_path.move(35, 150) #300, 160
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


        self.lbl_screen_resolution.setFixedSize(QSize(150, 30))
        self.lbl_screen_resolution.move(35, 420) #-30
        self.lbl_screen_resolution.setStyleSheet(
            """
                QLabel#lbl_screen_resolution {
                    color: rgb(57, 59, 64);
                    font: 15pt  "Segoe UI";
                }
            """
        )

        self.lbl_launcher_version.setFixedSize(QSize(150, 30))
        self.lbl_launcher_version.move(35, 825) #-30
        self.lbl_launcher_version.setStyleSheet(
            """
                QLabel#lbl_launcher_version {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )

        self.lbl_current_version.setFixedSize(QSize(165, 30))
        self.lbl_current_version.move(35, 860)
        self.lbl_current_version.setStyleSheet(
            """
                QLabel#lbl_current_version {
                    color: rgb(117, 118, 121);
                    font: 13pt "Segoe UI";
                }
            """
        )

        self.lbl_about.setFixedSize(QSize(60, 30))
        self.lbl_about.move(35, 920)
        self.lbl_about.setStyleSheet(
            """
                QLabel#lbl_about {
                    color: rgb(57, 59, 64);
                    font: 15pt "Segoe UI";
                }
            """
        )

        self.lbl_source_code.setFixedSize(QSize(140, 30))
        self.lbl_source_code.move(35, 950)
        self.lbl_source_code.setStyleSheet(
            """
                QLabel#lbl_source_code {
                    color: rgb(220, 188, 96);
                    font: 13pt "Segoe UI";
                }
            """
        )


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

    def btn_menu_1_event(self):
        self.btn_menu_1.setDown(True)
        self.btn_menu_2.setDown(False)
        self.btn_menu_3.setDown(False)

        self.scroll_area.verticalScrollBar().setValue(10)
        
        return None

    def btn_menu_2_event(self):
        self.btn_menu_1.setDown(False)
        self.btn_menu_2.setDown(True)
        self.btn_menu_3.setDown(False)

        self.scroll_area.verticalScrollBar().setValue(360)
    
        return None
    
    def btn_menu_3_event(self):
        self.btn_menu_1.setDown(False)
        self.btn_menu_2.setDown(False)
        self.btn_menu_3.setDown(True)

        self.scroll_area.verticalScrollBar().setValue(745)

        return None

    def btn_locate_path_event(self):
        
        self.new_game_path = QFileDialog.getExistingDirectory(self.scroll_container, 'Select the game installation folder')

        match self.new_game_path:
            case '' | None:
                pass
            case _:
                self.lbl_path.setText(self.new_game_path)

        return None

    def btn_locate_launcher_path_event(self):

        self.new_launcher_path = QFileDialog.getOpenFileName(self.scroll_container, 'Select the launcher executable')[0]

        match self.new_launcher_path:
            case '' | None:
                pass
            case _:
                self.lbl_launcher_path.setText(self.new_launcher_path)

        return None


    def btn_confirm_event(self):
        game_name, wallpaper_name, default = get_general()
        del wallpaper_name, default

        try:
            define(game_name, "path", self.new_game_path)
            define(game_name, "launcher_path", self.new_launcher_path)
        except:
            pass

        self.close()

        return None

if __name__ == '__main__':
    pass

