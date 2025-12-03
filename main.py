from PyQt6.QtWidgets import QApplication
from logic import *

def main() -> None:
    """
    Runs the program and opens the main window.
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()

if __name__=="__main__":
    main()

