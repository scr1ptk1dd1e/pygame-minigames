from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
path_to_db = os.path.join(path, '../Database/games.db')


class Ui_MainWindow(object):
    def loadDino(self):
        conn = sqlite3.connect(path_to_db)
        query = 'SELECT * FROM Dino'
        res = conn.execute(query)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Game', 'Score'])
        for row_number, row_data in enumerate(res):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    def loadGun(self):
        conn = sqlite3.connect(path_to_db)
        query = 'SELECT * FROM Gunshot'
        res = conn.execute(query)
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Game', 'Player blue', 'Player red'])
        for row_number, row_data in enumerate(res):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 486)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(30, 70, 551, 361))
        self.table.setGridStyle(QtCore.Qt.SolidLine)
        self.table.setWordWrap(True)
        self.table.setCornerButtonEnabled(True)
        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setCascadingSectionResizes(False)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 551, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dino_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.dino_btn.setObjectName("dino_btn")
        self.horizontalLayout.addWidget(self.dino_btn)
        self.gunshot_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.gunshot_btn.setObjectName("gunshot_btn")
        self.horizontalLayout.addWidget(self.gunshot_btn)
        self.memory_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.memory_btn.setObjectName("memory_btn")
        self.horizontalLayout.addWidget(self.memory_btn)
        
        self.dino_btn.clicked.connect(self.loadDino)
        self.gunshot_btn.clicked.connect(self.loadGun)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scoreboard"))
        self.table.setSortingEnabled(True)
        self.dino_btn.setText(_translate("MainWindow", "Dino"))
        self.gunshot_btn.setText(_translate("MainWindow", "Gunshot"))
        self.memory_btn.setText(_translate("MainWindow", "Memory"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
