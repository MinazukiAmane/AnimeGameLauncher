import sys
from PySide6.QtWidgets import QApplication
from modules.ui_main import MainWindow
from time import gmtime, time
import pathlib
import shutil
from modules.ui_start import StartWindow
from modules.hl_utils import read

def main():
    config_file = pathlib.Path(__file__).parents[2].resolve().joinpath('AGL/settings.json')
    file_folder = pathlib.Path(__file__).parents[2].resolve().joinpath('AGL')
    if not file_folder.is_dir():
        file_folder.mkdir()
    if not config_file.is_file():
        shutil.copyfile(str(pathlib.Path(__file__).parents[0].resolve().joinpath('default_settings.json')), str(config_file))
    app = QApplication([])
    if read("general","first") == 0:
        StartWindow()
        MainWindow()
    else:
        MainWindow()
    x = gmtime(time())
    print(str(x[3]) + ':' + str(x[4]) + ':' + str(x[5]) + ' Window launched')
    app.exec()
    print(str(x[3]) + ':' + str(x[4]) + ':' + str(x[5]) + ' Every Window was closed. Exiting...')
    sys.exit()

if __name__ == '__main__':
    main()
    