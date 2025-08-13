
from app.core.martsLoggingHandler import get_logger

fallback_logger = get_logger("__main__")

    

if __name__ == "__main__":
    fallback_logger.info("Application is starting...")
    from PySide6.QtWidgets import QApplication
    from app.ui_impl.mainWindow import MainWindow
    # from uiMainWindow import Ui_MainWindow

    from app.FileHandling.fileHandler import *
    # from canvasHandler import *
    import sys
    # import logging
    from version import version
    app = QApplication()
    # _main_window = QMainWindow()

    main_window = MainWindow(app)
    # main_window = Ui_MainWindow(app)
    main_window.setWindowTitle(f"Quil2Vec Version: {version}")
    # main_window.setGeometry(100, 100, 800, 500)
    main_window.show()
    fallback_logger.info("GUI has been launched.")
    sys.exit(app.exec())


