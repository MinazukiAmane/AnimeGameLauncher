from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox
import sys

def message_box(alert_level, text):
    dialog = QMessageBox()

    dialog.setWindowTitle("AnimeGameLauncher")
    dialog.setWindowIcon(QIcon(':/resources/icons/app_icon.png'))
    match alert_level:
        case 'WARNING' | 'Warning' | 'warning':
            dialog.setIcon(QMessageBox.Warning)
        case 'ERROR' | 'Error' | 'error':
            dialog.setIcon(QMessageBox.Critical)
        case _:
            dialog.setIcon(QMessageBox.Information)
    dialog.setText(str(text))

    dialog.exec()

    return None

if __name__ == '__main__':
    pass
