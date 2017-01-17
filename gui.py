from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QTextEdit, QGridLayout, \
    QWidget, QSystemTrayIcon, QMenu, qApp
from PyQt5.QtGui import QIcon, QTextCursor
import os
import cherrypy_server
import logging
import sys
import cherrypy
import traceback
import webbrowser


class GuiStreamer(object):
    def __init__(self, _write):
        self._write = _write

    def write(self, s):
        self._write(s)

    def flush(self):
        pass


def setup_logging(_write):
    cherrypy.log.screen = False
    stream = GuiStreamer(_write)
    ch = logging.StreamHandler(stream)
    root = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    sys.stdout = stream
    sys.stderr = stream


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.trayIcon = None
        self.kill = False
        self.setupTrayIcon()
        try:
            cherrypy_server.start_server()
        except Exception as e:
            logging.getLogger(__name__).warn("Problem starting print server! {}".format(e))
            traceback.print_exc()

    def reallyClose(self):
        self.kill = True
        self.close()

    def openConsole(self):
        from web.server import cfg
        url = r'https://localhost:{}'.format(cfg.port)
        webbrowser.open(url)


    def initUI(self):

        openAction = QAction("&Open Console", self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Console')
        openAction.triggered.connect(self.openConsole)

        exitAction = QAction(QIcon(os.path.join('web', 'static', 'img', 'exit-icon-3.png')), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.reallyClose)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        wrapper = QWidget()
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setLineWrapMode(QTextEdit.NoWrap)
        txt.setUndoRedoEnabled(False)
        txt.setAcceptDrops(False)
        txt.setAcceptRichText(False)

        font = txt.font()
        font.setFamily("Courier")
        font.setPointSize(9)
        txt.setFont(font)

        policy = txt.sizePolicy()
        policy.setVerticalStretch(1)
        txt.setSizePolicy(policy)

        layout = QGridLayout()
        layout.addWidget(txt)
        wrapper.setLayout(layout)

        self.setCentralWidget(wrapper)

        def _write(s):
            txt.moveCursor(QTextCursor.End)
            txt.insertPlainText(str(s))
            txt.moveCursor(QTextCursor.End)

        setup_logging(_write)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Antix Print Server')

    def setupTrayIcon(self):
        _icon = QIcon(os.path.join('web', 'static', 'img', 'Logo.144x144.png'))
        self.trayIcon = QSystemTrayIcon(_icon, self)
        menu = QMenu(self)
        menu.addAction("Show", self.show)
        menu.addAction("Hide", self.hide)
        menu.addAction("Exit", self.reallyClose)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.show()
        self.trayIcon.showMessage("Antix Printer Server", "Is running")

    def closeEvent(self, evnt):
        if self.kill:
            self.trayIcon.hide()
            try:
                cherrypy_server.stop_server()
            except Exception as e:
                logging.getLogger(__name__).warn("Problem stopping server! {}".format(e))
            qApp.exit(0)
        else:
            evnt.ignore()
            self.hide()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
