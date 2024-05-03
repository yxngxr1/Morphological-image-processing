# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1086, 709)
        MainWindow.setMinimumSize(QtCore.QSize(776, 513))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(220, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.radio_erosion = QtWidgets.QRadioButton(self.groupBox)
        self.radio_erosion.setGeometry(QtCore.QRect(10, 30, 82, 17))
        self.radio_erosion.setChecked(True)
        self.radio_erosion.setObjectName("radio_erosion")
        self.radio_dilation = QtWidgets.QRadioButton(self.groupBox)
        self.radio_dilation.setGeometry(QtCore.QRect(10, 50, 82, 17))
        self.radio_dilation.setObjectName("radio_dilation")
        self.radio_opening = QtWidgets.QRadioButton(self.groupBox)
        self.radio_opening.setGeometry(QtCore.QRect(10, 70, 82, 17))
        self.radio_opening.setObjectName("radio_opening")
        self.radio_closing = QtWidgets.QRadioButton(self.groupBox)
        self.radio_closing.setGeometry(QtCore.QRect(10, 90, 82, 17))
        self.radio_closing.setObjectName("radio_closing")
        self.btn_process = QtWidgets.QPushButton(self.groupBox)
        self.btn_process.setGeometry(QtCore.QRect(90, 190, 81, 23))
        self.btn_process.setObjectName("btn_process")
        self.btn_clear = QtWidgets.QPushButton(self.groupBox)
        self.btn_clear.setGeometry(QtCore.QRect(10, 220, 161, 23))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_to_black = QtWidgets.QPushButton(self.groupBox)
        self.btn_to_black.setGeometry(QtCore.QRect(10, 190, 71, 23))
        self.btn_to_black.setObjectName("btn_to_black")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(10, 160, 161, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 161, 21))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy)
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")
        self.verticalLayout_3.addWidget(self.label_status)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1086, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.menu.addAction(self.action_open)
        self.menu.addAction(self.action_save)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Морфологическая обработка изображений"))
        self.label_2.setText(_translate("MainWindow", "Исходное изображение"))
        self.label_3.setText(_translate("MainWindow", "Изображение после обработки"))
        self.groupBox.setTitle(_translate("MainWindow", "Выбор обработки"))
        self.radio_erosion.setText(_translate("MainWindow", "Сужение"))
        self.radio_dilation.setText(_translate("MainWindow", "Расширение"))
        self.radio_opening.setText(_translate("MainWindow", "Открытие"))
        self.radio_closing.setText(_translate("MainWindow", "Закрытие"))
        self.btn_process.setText(_translate("MainWindow", "Обработать"))
        self.btn_clear.setText(_translate("MainWindow", "Сбросить"))
        self.btn_to_black.setText(_translate("MainWindow", "Ч/Б"))
        self.comboBox.setItemText(0, _translate("MainWindow", "По алгоритму"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Scikit-Image"))
        self.label_4.setText(_translate("MainWindow", "Способ обработки:"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action_open.setText(_translate("MainWindow", "Открыть"))
        self.action_save.setText(_translate("MainWindow", "Сохранить"))