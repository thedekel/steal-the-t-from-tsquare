import sys, subprocess
from pyqt4 import QtCore, QtGui
from main_ui import Ui_ETMITM 

#global variables


class StartQT4(QtGui.QMainWindow):
    """
    this class will act as the main GUI
    """
    def __init__(self, parent = None):
        """
        Initialize the GUI in accordance with qt. Also set up the signals listeners
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ETMITM()
        self.ui.setupUi(self)
#        QtCore.QObject.connect(self.ui.button_open.SIGNAL("clicked()"), self.method)

    def checkDepend(self):
        pass


if __name__ == "__main__":
    """
    this acts as the python equivalent of a main function.
    """
    app = QtGui.QApplicaation(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
