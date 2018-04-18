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

# server constants
YAHOO_MAIL = "yahoo.com"
YAHOO_SMTP_SERVER = "smtp.mail.yahoo.com"
YAHOO_SMTP_PORT = 587

GMAIL_MAIL = "gmail.com"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

SERVER_INFO = [["yahoo", "smtp.mail.yahoo.com", 587], ["gmail", "smtp.gmail.com", 587]]

# placeholder text
email_lineEdit_placeholderText = "e-mail"
pasword_lineEdit_placeholderText = "password"
to_lineEdit_placeholderText = "send a copy"
subject_lineEdit_placeholderText = "subject"
message_lineEdit_placeholderText = "message"

# widget text
include_auto_message_checkBox_text = "include Write name"

cancel_pushButton_text = "Cancel"
execute_pushButton_text = "Run"
info_label_text = ""

version_label_text = "v1.1.0"

# tooltips
email_lineEdit_toolTip = "Type your e-mail address, e.g. myaddress@gmail.com or myaddress@yahoo.com."
pasword_lineEdit_toolTip = "password"
copy_to_lineEdit_toolTip = "Send a copy to recipients."
subject_lineEdit_toolTip = "subject"
include_auto_message_checkBox_toolTip = "The Write node name attached to the end of the message."
message_lineEdit_toolTip = "message"

cancel_pushButton_toolTip = "Cancel"
execute_pushButton_toolTip = "Run"

# warning messages
no_selected_write_message = "Write is not selected!"
info_label_warning_text = "Wrong e-mail or password!"
render_done_but_not_sent_warning_text = "Render is done but the notification was not sent.\nMissing or wrong e-mail or password."

# for searching
start = "@"
end = "."

# @ToDo
# - implement some warning and error messages
# missing_email_or_password_message = "Notification is not sent, missing email or password!"
# wrong_email_or_password_message = "Notification is not sent, wrong email or password!"
# @Refactor
# - make code more consistent
# - render_selected function too big
# - beautify mail server switcher code
# - implement regexp validator
# @Ideas
# - add a send a copy field


class SendMail(object):
    def __init__(self, email, password, copyto):
        self.email = email
        self.password = password
        self.copyto = copyto

        self.server = self.select_server()[0]
        self.port = self.select_server()[1]

        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo
        try:
            self.ret = True
            session.login(self.email, self.password)
            self.session = session
        except:
            self.ret = False

    def send_message(self, subject, body):

        self.copyto = self.copyto.split(',')
        self.recipients = [[self.email], self.copyto]
        self.recipients = [j for i in self.recipients for j in i]

        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + "," .join(self.recipients),
            "MIME-Version: 1.0",
            "Content-Type: text/html"]

        headers = "\r".join(headers)

        self.session.sendmail(
            self.email,
            self.recipients,
            headers + "\r\n\r\n" + body)

        self.session.close()

    def select_server(self):
        for i in SERVER_INFO:
            if self.email[self.email.find(start) + len(start):self.email.rfind(end)] == i[0]:
                self.server = i[1]
                self.port = i[2]

        return [self.server, self.port]


class WriteandNotify(QtWidgets.QMainWindow, writeandnotify_ui.Ui_writeandnotify_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setup_window_location()
        self.setup_ui_text()

        self.cancel_pushButton.clicked.connect(self.quit)
        self.execute_pushButton.clicked.connect(self.render_selected)

    def quit(self):
        self.close()

    def setup_window_location(self):
        # setup window properties
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width()/2-(WINDOW_WIDTH/2)
        y = screen.height()/2-(WINDOW_HEIGHT/2)-screen.height()/12
        self.move(x, y)

    def setup_ui_text(self):
        # setup widget texts
        self.cancel_pushButton.setText(cancel_pushButton_text)
        self.execute_pushButton.setText(execute_pushButton_text)
        self.include_auto_message_checkBox.setText(include_auto_message_checkBox_text)
        self.info_label.setText(info_label_text)

        # setup placeholder texts
        self.email_lineEdit.setPlaceholderText(email_lineEdit_placeholderText)
        self.password_lineEdit.setPlaceholderText(pasword_lineEdit_placeholderText)
        self.copy_to_lineEdit.setPlaceholderText(to_lineEdit_placeholderText)
        self.subject_lineEdit.setPlaceholderText(subject_lineEdit_placeholderText)
        self.message_textEdit.setPlaceholderText(message_lineEdit_placeholderText)

        # setup tooltips
        self.cancel_pushButton.setToolTip(cancel_pushButton_toolTip)
        self.execute_pushButton.setToolTip(execute_pushButton_toolTip)

        self.email_lineEdit.setToolTip(email_lineEdit_toolTip)
        self.password_lineEdit.setToolTip(pasword_lineEdit_toolTip)
        self.copy_to_lineEdit.setToolTip(copy_to_lineEdit_toolTip)
        self.subject_lineEdit.setToolTip(subject_lineEdit_toolTip)
        self.message_textEdit.setToolTip(message_lineEdit_toolTip)

        self.include_auto_message_checkBox.setToolTip(include_auto_message_checkBox_toolTip)

        self.version_label.setText(version_label_text)

    def execute_render(self):

        if self.execute_pushButton.clicked:
            self.quit()

        # sort by render order
        self.nodes.sort(key=lambda x: x['render_order'].value())

        # disable proxy
        proxy = nuke.root()['proxy'].value()
        nuke.root()['proxy'].setValue(False)

        # empty tuple for storing frame start/end/incr
        t = ()  # only used in executeMultiple()

        # render!
        # c = len(self.nodes)
        self.write_list = []
        for i, node in enumerate(self.nodes):
            self.first_frame = int(node['first'].value())
            self.last_frame = int(node['last'].value())

            # execute node
            nuke.execute(node, self.first_frame, self.last_frame, 1)
            t = t + ((self.first_frame, self.last_frame, 1),)  # only used in executeMultiple()
            write_is_done = "%s is done" % (node.name())
            self.write_list.append(write_is_done)

        # set proxy back to original value
        nuke.root()['proxy'].setValue(proxy)

    def render_selected(self):
        self.your_email = str(self.email_lineEdit.text())
        self.your_password = str(self.password_lineEdit.text())
        self.copy_to = str(self.copy_to_lineEdit.text())
        self.your_subject = self.subject_lineEdit.text()

        self.selected_server = self.your_email[self.your_email.find(start) + len(start):self.your_email.rfind(end)]

        self.nodes = nuke.selectedNodes('Write')

        if self.nodes == []:
            nuke.message(no_selected_write_message)
        elif self.selected_server not in [j for i in SERVER_INFO for j in i]:
            self.info_label.setText(info_label_text)
            self.execute_render()
            nuke.message(render_done_but_not_sent_warning_text)
        elif self.user_account_check(self.your_email, self.your_password, self.copy_to) == False:
            self.info_label.setText(info_label_warning_text)
        else:
            self.info_label.setText(info_label_text)
            self.execute_render()
            # send mail
            self.prepare_and_send_message(self.your_email, self.your_password, self.copy_to)

    def cleanup_write_list_message(self, write_list):
        self.write_list = str(write_list)
        self.write_list = self.write_list.replace("'", "")[1:-1]
        return self.write_list

    def prepare_and_send_message(self, your_email, your_password, copy_to):
        if self.include_auto_message_checkBox.isChecked():
            self.your_message_body = self.message_textEdit.toPlainText() + "<br><br>" + self.cleanup_write_list_message(self.write_list)
        else:
            self.your_message_body = self.message_textEdit.toPlainText()

        if not self.your_email or not self.your_password:
            pass
        else:
            self.message = SendMail(self.your_email, self.your_password, self.copy_to)
            self.message.send_message(self.your_subject, self.your_message_body)

        del self.your_password

    def user_account_check(self, your_email, your_password, copy_to):
        self.message = SendMail(self.your_email, self.your_password, self.copy_to)

        return self.message.ret


# if __name__ == "__main__":
#     aa = WriteandNotify()
#     aa.show()


def main(a):
   pass
