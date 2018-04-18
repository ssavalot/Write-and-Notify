""" 
    Write and Notify v1.0.0
    Copyright (C) 2018 Levente Vass

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from PySide2 import QtWidgets, QtGui

import nuke

import smtplib
import writeandnotify_ui

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 216

YAHOO_MAIL = "yahoo.com"
YAHOO_SMTP_SERVER = "smtp.mail.yahoo.com"
YAHOO_SMTP_PORT = 587

GMAIL_MAIL = "gmail.com"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

version_label_text = "v1.0.0"

cancel_pushButton_text = "Cancel"
execute_pushButton_text = "Run"

email_lineEdit_text = "email"
pasword_lineEdit_text = "password"
subject_lineEdit_text = "subject"
message_lineEdit_text = "message"

cancel_pushButton_toolTip_text = "Cancel"
execute_pushButton_toolTip_text = "Run"

email_lineEdit_toolTip_text = "Type your email address, e.g. myaddress@gmail.com or myaddress@yahoo.com."
pasword_lineEdit_toolTip_text = "password"
subject_lineEdit_toolTip_text = "subject"
message_lineEdit_toolTip_text = "message"
include_auto_message_checkBox_toolTip_text = "The Write node name attached to the end of the message."

include_auto_message_checkBox_text = "include write name"

no_selected_write_message = "Write is not selected!"

## @ToDo
# - implement some warning and error messages
# missing_email_or_password_message = "Notification is not sent, missing email or password!"
# wrong_email_or_password_message = "Notification is not sent, wrong email or password!"
## @Refactor
# - make code more consistent
# - render_selected function too big
# - beautify mail server switcher code
# - implement regexp validator
## @Ideas
# UI/UX
# - implement completer and store email address in current session
# - auto generated body content


class SendMail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

        # mail server switcher
        if self.email[-9:] == YAHOO_MAIL:
            self.server = YAHOO_SMTP_SERVER
            self.port = YAHOO_SMTP_PORT
        elif self.email[-9:] == GMAIL_MAIL:
            self.server = GMAIL_SMTP_SERVER
            self.port = GMAIL_SMTP_PORT

        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, subject, body):
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + self.email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            self.email,
            headers + "\r\n\r\n" + body)


class WriteandNotify(QtWidgets.QMainWindow, writeandnotify_ui.Ui_writeandnotify_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.location_on_the_screen()
        self.set_ui_text()

        self.cancel_pushButton.clicked.connect(self.quit)
        self.execute_pushButton.clicked.connect(self.render_selected)

    def quit(self):
        self.close()

    def location_on_the_screen(self):
        # setup window properties
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width()/2-(WINDOW_WIDTH/2)
        y = screen.height()/2-(WINDOW_HEIGHT/2)-screen.height()/12
        self.move(x, y)

    def set_ui_text(self):
        # setup text content
        self.cancel_pushButton.setText(cancel_pushButton_text)
        self.execute_pushButton.setText(execute_pushButton_text)

        self.email_lineEdit.setPlaceholderText(email_lineEdit_text)
        self.password_lineEdit.setPlaceholderText(pasword_lineEdit_text)
        self.subject_lineEdit.setPlaceholderText(subject_lineEdit_text)
        self.message_textEdit.setPlaceholderText(message_lineEdit_text)

        self.include_auto_message_checkBox.setText(include_auto_message_checkBox_text)

        # setup tooltip text content
        self.cancel_pushButton.setToolTip(cancel_pushButton_toolTip_text)
        self.execute_pushButton.setToolTip(execute_pushButton_toolTip_text)

        self.email_lineEdit.setToolTip(email_lineEdit_toolTip_text)
        self.password_lineEdit.setToolTip(pasword_lineEdit_toolTip_text)
        self.subject_lineEdit.setToolTip(subject_lineEdit_toolTip_text)
        self.message_textEdit.setToolTip(message_lineEdit_toolTip_text)

        self.include_auto_message_checkBox.setToolTip(include_auto_message_checkBox_toolTip_text)

        self.version_label.setText(version_label_text)

    def render_selected(self):
        self.nodes = nuke.selectedNodes('Write')

        if self.execute_pushButton.clicked:
            self.quit()

        if self.nodes == []:
            nuke.message(no_selected_write_message)

        # sort by render order
        self.nodes.sort(key=lambda x: x['render_order'].value())

        # disable proxy
        proxy = nuke.root()['proxy'].value()
        nuke.root()['proxy'].setValue(False)

        # empty tuple for storing frame start/end/incr
        t = ()  # only used in executeMultiple()

        # render!
        c = len(self.nodes)
        message_list = []
        for i, node in enumerate(self.nodes):
            f = int(node['first'].value())
            l = int(node['last'].value())

            # execute node
            nuke.execute(node, f, l, 1)

            t = t + ((f, l, 1),)  # only used in executeMultiple()
            # write_is_done = "%d of %d, %s is done" % (i + 1, c, node.name())
            write_is_done = "%s is done" % (node.name())
            message_list.append(write_is_done)

        # set proxy back to original value
        nuke.root()['proxy'].setValue(proxy)

        # cleanup message
        self.auto_message = str(message_list)
        self.auto_message_clean = self.auto_message.replace("'", "")

        # send mail
        self.your_email = str(self.email_lineEdit.text())
        self.your_password = str(self.password_lineEdit.text())
        self.your_subject = self.subject_lineEdit.text()
        if self.include_auto_message_checkBox.isChecked():
            self.your_message_body = self.message_textEdit.toPlainText() + "<br><br>" + self.auto_message_clean[1:-1]
        else:
            self.your_message_body = self.message_textEdit.toPlainText()

        if len(self.your_email) and len(self.your_password) == 0:
            nuke.message("Render is done but the notification was not sent. Missing email or password.")
        else:
            mm = SendMail(self.your_email, self.your_password)
            mm.send_message(self.your_subject, self.your_message_body)

        del self.your_password


def main(a):
    pass
