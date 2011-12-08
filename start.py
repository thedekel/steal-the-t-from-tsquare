import sys, subprocess
from PyQt4 import QtCore, QtGui
from main_ui import Ui_ETMITM 

#global variables
myos="ubuntu/backtrack"
depend={
        'dhcp3':{'conf':'/etc/dhcp3/dhcpcd.conf', 'name':'dhcp3', 'type':'dhcpd'},
        'dhcpd':{'conf':'/etc/dhcpd.conf','name':'dhcpd','type':'dhcpd'},
        'airmon-ng':{'name':'airmon-ng','type':'airmon'},
        'gnome-terminal':{'name':'gnome-terminal','type':'term'},
        'dnsmasq':{'name':'dnsmasq','type':'dnsmasq'},
        'driftnet':{'name':'driftnet','type':'driftnet'},
        'urlsnarf':{'name':'urlsnarf','type':'urlsnarf'},
        'dsniff':{'name':'dnsiff','type':'dsniff'},
        'sslstrip':{'name':'sslstrip','type':'sslstrip'}
        }

toInstall = []
installed = {'dhcpd':'', 'airmon':'', 'term':'', 'dnsmasq':'', 'driftnet':'','urlsnarf':'', 'dnsiff':'', 'sslstrip':''}

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
#        QtCore.QObject.connect(self.ui.button_open, QtCore.SIGNAL("clicked()"), self.method)
        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.checkDepend)


    def checkDepend(self):
        # check for arch:
        pp = subprocess.Popen
        p = pp(['uname', '-a'], stdout=subprocess.PIPE)
        out,err = p.communicate()
        global myos
        myos=('arch' if 'ARCH' in out else myos)
        stout = "OS detected as %s\n"%myos
        self.ui.plainTextEdit.insertPlainText(stout)
        # check required programs
        self.lookAtDepend()
        global toInstall
        # begin installing stuff
        if myos == 'arch':
            for i in toInstall:
                p = pp(['yaourt', i])
                p.wait()
        else:
            for i in toInstall:
                p = pp(['apt-get install', i])
                p.wait()
        pass

    def lookAtDepend(self):
        global depend
        global installed
        global toInstall
        # look at all possible required programs
        for x in depend.keys():
            self.ui.plainTextEdit.insertPlainText("looking for %s..."%x)
            try:
                # indicate that you will use a program if its found
                p = subprocess.Popen([x,''],stdout=subprocess.PIPE)
                installed[depend[x]['type']] = depend[x]
                self.ui.plainTextEdit.insertPlainText("found!\n")
                try:
                    p.kill()
                except:
                    pass
            except:
                # add programs that need to be installed to a queue
                self.ui.plainTextEdit.insertPlainText("not found.\n")
                pass




if __name__ == "__main__":
    """
    this acts as the python equivalent of a main function.
    """
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
