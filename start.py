import sys, subprocess
from PyQt4 import QtCore, QtGui
from main_ui import Ui_ETMITM 

#global variables
pp = subprocess.Popen
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
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.installStuff)
        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL('clicked()'), self.startAttack)



    def checkDepend(self):
        # check for arch:
        p = pp(['uname', '-a'], stdout=subprocess.PIPE)
        out,err = p.communicate()
        global myos
        myos=('arch' if 'ARCH' in out else myos)
        stout = "OS detected as %s\n"%myos
        self.ui.plainTextEdit.insertPlainText(stout)
        # check required programs
        self.lookAtDepend()

    def installStuff(self):
        global toInstall
        self.ui.plainTextEdit.insertPlainText("trying to install %d dependancies\n"%len(toInstall))
        # begin installing stuff
        if myos == 'arch':
            for i in toInstall:
                self.ui.plainTextEdit.insertPlainText("installing " + i + "\n")
                p = pp(['yaourt', i])
                p.wait()
        else:
            for i in toInstall:
                self.ui.plainTextEdit.insertPlainText("installing " + i + "\n")
                p = pp(['apt-get install', i])
                p.wait()

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

    def startAttack(self):
        global depend
        for a in depend.keys():
            if depend[a]=='':
                self.ui.plainTextEdit.insertPlainText("please install dependancies before attempting attack\n")
                return
        self.checkdhcpdconf()

    def checkdhcpdconf(self):
        mainLog = self.ui.plainTextEdit.insertPlainText
        global depend
        reply = QtGui.QMessageBox.question(self,'add conf settings?', 'Would you like me to add the required settings to dhcpd.conf?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.ui.plainTextEdit.insertPlainText("setting up dhcpd.conf\n")
            gerp = pp(['grep', self.ui.lineEdit_4.text(), depend['dhcpd']['conf']],stdout=subprocess.PIPE)
            out, err = gerp.communicate()
            if out:
                self.ui.plainTextEdit.insertPlainText("current settings may already exist, please edit %s and select 'No' next time you are asked to modify dhcpd.conf\n"%depend['dhcpd']['conf'])
                return
            else:
                dhcpdconfile = file(depend['dhcpd']['conf'],'r')
                mainLog('creating backup of dhcpd.conf...\n')
                file('dhcpd.conf.bak', 'w').write(dhcpdconfile.read())
                dhcpdconfile.close()
                dhcpdconfile = file(depend['dhcpd']['conf'],'a')
                dhcpdconfile.write("option domain-name-servers %s;\n"%self.ui.lineEdit_4.text())
                dhcpdconfile.write("subnet %s netmask %s{\n"%(self.ui.lineEdit_5.text(),self.ui.lineEdit_6.text()))
                dhcpdconfile.write("range %s %s;\n"%(self.ui.lineEdit_7.text(), self.ui.lineEdit_9.text()))
                dhcpdconfile.write("option routers %s;\n"%self.ui.lineEdit_8.text())
                dhcpdconfile.write("option domain-name-servers %s;\n"%self.ui.lineEdit_4.text())
                dhcpdconfile.write("}\n")
        else:
            pass



if __name__ == "__main__":
    """
    this acts as the python equivalent of a main function.
    """
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())