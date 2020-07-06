import os
import sys
import socket
from wakeonlan import send_magic_packet
from PySide2 import QtCore, QtGui, QtWidgets

version="0.1c"
path=os.path.dirname(os.path.abspath(__file__))

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, elements=[], parent=None):
        super(mainWindow, self).__init__(parent)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QtWidgets.QGridLayout(self.widget)
        self.setWindowTitle("Alfred v%s" % (version))
        self.setWindowIcon(QtGui.QIcon(os.path.join(path,"img/logo.png")))
        self.elements=elements

    def build(self):

        saw=shutAllWidget(self.elements,self.widget)
        self.layout.addWidget(saw,4,1)

        for i,e in enumerate(self.elements):
            e.connect()
            self.layout.addWidget(e.getHeaderWidget(self),1,i+2)
            self.layout.addWidget(e.getStatusWidget(self),2,i+2)
            self.layout.addWidget(e.getPowerSwitchWidget(self),3,i+2)
            vpw=vpWidget(e,self)
            self.layout.addWidget(vpw,4,i+2)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,"Message","Are you sure to quit Alfred?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for e in self.elements:
                e.disconnect()
            event.accept()
        else:
            event.ignore()

class vpWidget(QtWidgets.QWidget):

    def __init__(self, vp=None, parent=None):
        super(vpWidget, self).__init__(parent)
        self.vp=vp
        layout=QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        buttonOn=QtWidgets.QPushButton(self)
        buttonOn.setText("Shutter")
        layout.addWidget(buttonOn)
        buttonOn.clicked.connect(self.toggleShutter)

    def toggleShutter(self):
        self.vp.toggleShutter()

class shutAllWidget(QtWidgets.QPushButton):

    def __init__(self, elements, parent=None):
        super(shutAllWidget, self).__init__(parent)
        self.setText("Shut all")
        self.clicked.connect(self.shutAll)
        self.elements=elements

    def shutAll(self):
        for e in self.elements:
            e.enableShutter()

class powerSwitchWidget(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super(powerSwitchWidget, self).__init__(parent)
        # self.setCheckable(True)
        pix=QtGui.QPixmap(os.path.join(path,"img/switch.png"))
        s=24
        self.setIcon(pix.scaled(s, s, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.setIconSize(QtCore.QSize(s,s))

class statusWidget(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(statusWidget, self).__init__(parent)
        super(statusWidget, self).setAlignment(QtCore.Qt.AlignCenter)

    def setReady(self):
        self.setText("Ready")

class headerWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(headerWidget, self).__init__(parent)
        lay=QtWidgets.QVBoxLayout(self)
        self.mainLabel=QtWidgets.QLabel(self)
        self.imgLabel=QtWidgets.QLabel(self)
        self.manLabel=QtWidgets.QLabel(self)
        self.modLabel=QtWidgets.QLabel(self)
        lay.addWidget(self.mainLabel)
        lay.addWidget(self.imgLabel)
        lay.addWidget(self.manLabel)
        lay.addWidget(self.modLabel)

    def setLabel(self,label):
        self.mainLabel.setText(label)
        self.mainLabel.setAlignment(QtCore.Qt.AlignCenter)

    def setImage(self,img):
        pix=QtGui.QPixmap(img).scaled(96, 96, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.imgLabel.setPixmap(pix)
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)

    def setManufacturer(self,manufacturer):
        self.manLabel.setText(manufacturer)
        self.manLabel.setAlignment(QtCore.Qt.AlignCenter)

    def setModel(self,model):
        self.modLabel.setText(model)
        self.modLabel.setAlignment(QtCore.Qt.AlignCenter)

class caveElement:
    def __init__(self, elementType, manufacturer, model, label, ip, port, img):
        self.elementType = elementType
        self.label = label
        self.manufacturer = manufacturer
        self.model = model
        self.ip = ip
        self.port = port
        self.img = img
        self.sWidget = None
        self.hWidget = None
        self.psWidget = None

    def getHeaderWidget(self,parent):
        self.hWidget=headerWidget(parent)
        self.hWidget.setLabel(self.label)
        self.hWidget.setImage(self.img)
        self.hWidget.setManufacturer(self.manufacturer)
        self.hWidget.setModel(self.model)
        return(self.hWidget)

    def getStatusWidget(self,parent):
        self.sWidget=statusWidget(parent)
        status=self.getStatus()
        self.sWidget.setText(status[0])
        if not status[1] is None:
            self.sWidget.setStyleSheet("QLabel { background-color : "+status[1]+";}")
        return(self.sWidget)

    def getPowerSwitchWidget(self,parent):
        self.psWidget=powerSwitchWidget(parent)
        self.psWidget.clicked.connect(self.togglePower)
        return(self.psWidget)

    def getStatus(self):
        return("Unknown",None)

    def enableShutter(self):
        print("Nothing to do")

    def disableShutter(self):
        print("Nothing to do")

    def connect(self):
        print("Nothing to do")

    def disconnect(self):
        print("Nothing to do")

    def togglePower(self):
        print("Nothing to do")

class tracking(caveElement):
    def __init__(self, manufacturer, model, label, ip, port):
        super(tracking, self).__init__("tracking", manufacturer, model, label, ip, port, os.path.join(path,"img/tracking.png"))

class trackpacke(tracking):
    def __init__(self, label, ip, mac):
        super(trackpacke, self).__init__("ART", "Trackpack/E", label, ip, 50105)
        self.mac=mac

    def disconnect(self):
        print("Disconnecting %s." % (self.label))
        self.sock.close()
        
    def command(self,command):
        self.sock.send(command.encode())

    def togglePower(self):
        self.powerOn()
            
    def powerOn(self):
        print("Powering on %s." % (self.label))
        send_magic_packet(self.mac)

    def powerOff(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print("Powering off %s." % (self.label))
        self.command("dtrack2 system shutdown")

class pc(caveElement):
    def __init__(self, manufacturer, model, label, ip, port):
        super(pc, self).__init__("pc", manufacturer, model, label, ip, port, os.path.join(path,"img/pc.png"))

class hpz4(pc):
    def __init__(self, label, ip, mac):
        super(hpz4, self).__init__("HP", "Z4", label, ip, 2050)
        self.mac=mac

    def togglePower(self):
        self.powerOn()
            
    def powerOn(self):
        print("Powering on %s." % (self.label))
        send_magic_packet(self.mac)

class projector(caveElement):
    def __init__(self, manufacturer, model, label, ip, port):
        super(projector, self).__init__("projector", manufacturer, model, label, ip, port, os.path.join(path,"img/projector.png"))

class christie4k10hs(projector):
    def __init__(self, label, ip):
        super(christie4k10hs, self).__init__("Christie", "4k10-hs", label, ip, 3002)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to %s (%s) on port %d" % (self.label,self.ip,self.port))
        try :
            self.sock.connect((self.ip, self.port))
        except :
            print('Something\'s wrong with %s.' % (self.label))

    def disconnect(self):
        print("Disconnecting %s." % (self.label))
        self.sock.close()
        
    def command(self,command):
        self.sock.send(command.encode())

    def request(self,command):
        self.sock.send(command.encode())
        try :
            data = self.sock.recv(1024).decode()
            if data:
                return(data)
            else:
                return(None)
        except:
            print("Something\'s wrong with projector %s." % (self.label))

    def enableShutter(self):
        print("Hidding %s." % (self.label))
        self.command("(SHU1)")

    def disableShutter(self):
        print("Showing %s." % (self.label))
        self.command("(SHU0)")

    def getShutter(self):
        data=self.request("(SHU?)")
        if data == "(SHU!01)":
            ans=True
        else:
            ans=False
        return(ans)

    def getPower(self):
        data=self.request("(PWR?)")
        if data == "(PWR!01)":
            ans=True
        else:
            ans=False
        return(ans)

    def getStatus(self):
        if self.getPower():
            ans="On"
            color="green"
        else:
            ans="Off"
            color="red"
        return(ans,color)

    def toggleShutter(self):
        if self.getShutter():
            self.disableShutter()
        else:
            self.enableShutter()

    def togglePower(self):
        if self.getPower():
            reply = QtWidgets.QMessageBox.question(self.psWidget,"Message","Are you sure to shut down %s?" % (self.label), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.powerOff()
        else:
            self.powerOn()

    def powerOn(self):
        print("Powering on %s." % (self.label))
        self.command("(PWR1)")

    def powerOff(self):
        print("Powering off %s." % (self.label))
        self.command("(PWR0)")


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    app.setStyle('Fusion')
    # app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    twoFace=hpz4("Serveur","192.168.95.11","10-E7-C6-46-3F-BB")
    vpMur=christie4k10hs("VP Mur","192.168.95.21")
    vpSol=christie4k10hs("VP Sol","192.168.95.22")
    tracking=trackpacke("Tracking","192.168.95.31","4C-52-62-0A-8F-BE")

    elementList=[twoFace,vpMur,vpSol,tracking]

    mw=mainWindow(elementList)
    mw.build()

    # vpMur.getStatus()
    # vpSol.connect()

    # vpMur.command('(PWR0)')
    # vpSol.command('(PWR0)')

    # vpMur.command('(PWR1)')
    # vpSol.command('(PWR1)')

    # vpMur.disconnect()
    # vpSol.disconnect()

    mw.show()
    sys.exit(app.exec_())