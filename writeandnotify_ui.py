# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'writeandnotify_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_writeandnotify_MainWindow(object):
    def setupUi(self, writeandnotify_MainWindow):
        writeandnotify_MainWindow.setObjectName("writeandnotify_MainWindow")
        writeandnotify_MainWindow.resize(293, 266)
        self.writeandnotify_centralwidget = QtWidgets.QWidget(writeandnotify_MainWindow)
        self.writeandnotify_centralwidget.setObjectName("writeandnotify_centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.writeandnotify_centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.email_password_gridLayout = QtWidgets.QGridLayout()
        self.email_password_gridLayout.setObjectName("email_password_gridLayout")
        self.email_lineEdit = QtWidgets.QLineEdit(self.writeandnotify_centralwidget)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.email_password_gridLayout.addWidget(self.email_lineEdit, 0, 0, 1, 1)
        self.password_lineEdit = QtWidgets.QLineEdit(self.writeandnotify_centralwidget)
        self.password_lineEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.email_password_gridLayout.addWidget(self.password_lineEdit, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.email_password_gridLayout)
        self.subject_lineEdit = QtWidgets.QLineEdit(self.writeandnotify_centralwidget)
        self.subject_lineEdit.setObjectName("subject_lineEdit")
        self.verticalLayout.addWidget(self.subject_lineEdit)
        self.include_auto_message_checkBox = QtWidgets.QCheckBox(self.writeandnotify_centralwidget)
        self.include_auto_message_checkBox.setObjectName("include_auto_message_checkBox")
        self.verticalLayout.addWidget(self.include_auto_message_checkBox)
        self.message_textEdit = QtWidgets.QTextEdit(self.writeandnotify_centralwidget)
        self.message_textEdit.setObjectName("message_textEdit")
        self.verticalLayout.addWidget(self.message_textEdit)
        self.cancel_execute_horizontalLayout = QtWidgets.QHBoxLayout()
        self.cancel_execute_horizontalLayout.setObjectName("cancel_execute_horizontalLayout")
        self.cancel_pushButton = QtWidgets.QPushButton(self.writeandnotify_centralwidget)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.cancel_execute_horizontalLayout.addWidget(self.cancel_pushButton)
        self.execute_pushButton = QtWidgets.QPushButton(self.writeandnotify_centralwidget)
        self.execute_pushButton.setObjectName("execute_pushButton")
        self.cancel_execute_horizontalLayout.addWidget(self.execute_pushButton)
        self.verticalLayout.addLayout(self.cancel_execute_horizontalLayout)
        self.version_label = QtWidgets.QLabel(self.writeandnotify_centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.version_label.setFont(font)
        self.version_label.setObjectName("version_label")
        self.verticalLayout.addWidget(self.version_label)
        writeandnotify_MainWindow.setCentralWidget(self.writeandnotify_centralwidget)

        self.retranslateUi(writeandnotify_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(writeandnotify_MainWindow)

    def retranslateUi(self, writeandnotify_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        writeandnotify_MainWindow.setWindowTitle(_translate("writeandnotify_MainWindow", "Write and Notify"))
        self.email_lineEdit.setToolTip(_translate("writeandnotify_MainWindow", "email_toolTip"))
        self.email_lineEdit.setPlaceholderText(_translate("writeandnotify_MainWindow", "email_placeholderText"))
        self.password_lineEdit.setToolTip(_translate("writeandnotify_MainWindow", "password_toolTip"))
        self.password_lineEdit.setPlaceholderText(_translate("writeandnotify_MainWindow", "password_placeholderText"))
        self.subject_lineEdit.setToolTip(_translate("writeandnotify_MainWindow", "subject_toolTip"))
        self.subject_lineEdit.setPlaceholderText(_translate("writeandnotify_MainWindow", "subject_placeholderText"))
        self.include_auto_message_checkBox.setToolTip(_translate("writeandnotify_MainWindow", "include_auto_message_toolTip"))
        self.include_auto_message_checkBox.setText(_translate("writeandnotify_MainWindow", "include_auto_message_checkBox_text"))
        self.message_textEdit.setToolTip(_translate("writeandnotify_MainWindow", "message_toolTip"))
        self.message_textEdit.setPlaceholderText(_translate("writeandnotify_MainWindow", "message_placholderText"))
        self.cancel_pushButton.setToolTip(_translate("writeandnotify_MainWindow", "cancel_toolTip"))
        self.cancel_pushButton.setText(_translate("writeandnotify_MainWindow", "cancel_pushButton"))
        self.execute_pushButton.setToolTip(_translate("writeandnotify_MainWindow", "execute_toolTip"))
        self.execute_pushButton.setText(_translate("writeandnotify_MainWindow", "execute_pushButton"))
        self.version_label.setText(_translate("writeandnotify_MainWindow", "version_label_text"))
