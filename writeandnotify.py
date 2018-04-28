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

from PySide2 import QtWidgets, QtGui, QtCore

import os
import sys
import csv
import functools

import nuke
import smtplib
import writeandnotify_ui

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 216

# server constants
SERVER_INFO = [["yahoo", "smtp.mail.yahoo.com", 587], ["gmail", "smtp.gmail.com", 587]]

# placeholder text
email_lineEdit_placeholderText = "e-mail"
pasword_lineEdit_placeholderText = "password"
to_lineEdit_placeholderText = "send a copy"
subject_lineEdit_placeholderText = "subject"
message_lineEdit_placeholderText = "message"

# widget text
include_auto_message_checkBox_text = "include Write name"
just_send_the_message_checkBox_text = "just send the message"

cancel_pushButton_text = "Cancel"
execute_pushButton_text = "Run"
info_label_text = ""

version_label_text = "v1.4"

# tooltips
email_lineEdit_toolTip = "Type your e-mail address, e.g. myaddress@gmail.com or myaddress@yahoo.com."
pasword_lineEdit_toolTip = "password"
copy_to_lineEdit_toolTip = "Send a copy to recipients."
subject_lineEdit_toolTip = "subject"
include_auto_message_checkBox_toolTip = "The Write node name attached to the end of the message."
just_send_the_message_checkBox_toolTip = "Just send the message, nothing more."
message_lineEdit_toolTip = "message"

cancel_pushButton_toolTip = "Cancel"
execute_pushButton_toolTip = "Run"

# warning messages
no_selected_write_message = "Write is not selected!"
info_label_warning_text = "Wrong e-mail or password!"
render_done_but_not_sent_warning_text = "Render is done but the notification was not sent.\nMissing or wrong e-mail or password."
message_sent = "Message sent."

# for searching
start = "@"
end = "."

address_cache = "address_cache.csv"

auto_complete = True

pocs = 0

# TODO
# - make code more consistent


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

        # try login, used in user_account_check()
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


class AutoCompleteEdit(QtWidgets.QLineEdit):
    def __init__(self, model, separator=' ', addSpaceAfterCompleting=True):
        super(AutoCompleteEdit, self).__init__()
        self._separator = separator
        self._addSpaceAfterCompleting = addSpaceAfterCompleting
        self._completer = QtWidgets.QCompleter(model)
        self._completer.setWidget(self)
        self.connect(
                self._completer,
                QtCore.SIGNAL('activated(QString)'),
                self._insertCompletion)
        self._keysToIgnore = [QtCore.Qt.Key_Enter,
                              QtCore.Qt.Key_Return,
                              QtCore.Qt.Key_Escape,
                              QtCore.Qt.Key_Tab]

    def _insertCompletion(self, completion):
        """
            This is the event handler for the QCompleter.activated(QString) signal,
            it is called when the user selects an item in the completer popup.
        """
        extra = len(completion) - len(self._completer.completionPrefix())
        extra_text = completion[-extra:]
        if self._addSpaceAfterCompleting:
            extra_text += ''
        self.setText(self.text() + extra_text)

    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1
        while i >= 0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(AutoCompleteEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()
        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)
        if len(event.text()) > 0 and len(completionPrefix) > 0:
            self._completer.complete()
        if len(completionPrefix) == 0:
            self._completer.popup().hide()

    def _updateCompleterPopupItems(self, completionPrefix):
        """
            Filters the completer's popup items to only show items
            with the given prefix.
        """
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
                self._completer.completionModel().index(0, 0))


class WriteandNotify(QtWidgets.QMainWindow, writeandnotify_ui.Ui_writeandnotify_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setup_window_location()

        # if auto_complete is True use custom widgets
        if auto_complete:
            self.create_address_cache()

            self.email_password_gridLayout.removeWidget(self.email_lineEdit)
            self.email_lineEdit.deleteLater()
            self.email_lineEdit = None

            self.copy_and_subject_gridLayout.removeWidget(self.copy_to_lineEdit)
            self.copy_to_lineEdit.deleteLater()
            self.copy_to_lineEdit = None

            self.email_lineEdit = AutoCompleteEdit(self.read_csv())
            self.copy_to_lineEdit = AutoCompleteEdit(self.read_csv())
            self.email_password_gridLayout.addWidget(self.email_lineEdit, 0, 0, 1, 1)
            self.copy_and_subject_gridLayout.addWidget(self.copy_to_lineEdit, 0, 0)

            self.email_lineEdit.setFocus()
            self.email_lineEdit.isActiveWindow()
            self.email_lineEdit.raise_()

            self.execute_pushButton.clicked.connect(self.write_csv)
            self.execute_pushButton.clicked.connect(self.update_completer)

        self.setTabOrder(self.email_lineEdit, self.password_lineEdit.focusProxy())
        self.setTabOrder(self.password_lineEdit, self.copy_to_lineEdit)
        self.setTabOrder(self.copy_to_lineEdit.focusProxy(), self.subject_lineEdit)
        self.setTabOrder(self.subject_lineEdit, self.include_auto_message_checkBox)
        self.setTabOrder(self.include_auto_message_checkBox, self.message_textEdit)
        self.setTabOrder(self.message_textEdit, self.cancel_pushButton)
        self.setTabOrder(self.cancel_pushButton, self.execute_pushButton)

        self.setup_ui_text()

        self.cancel_pushButton.clicked.connect(self.quit)
        self.execute_pushButton.clicked.connect(self.render_selected)

        # disable write list widget
#         self.just_send_the_message_checkBox.mousePressEvent = functools.partial(
#                         self.check_button,
#                         source_object=self.just_send_the_message_checkBox)

#     def check_button(self, event, source_object=None):
#         if self.just_send_the_message_checkBox.isChecked():
#             print('enabled')
#             self.just_send_the_message_checkBox.setChecked(False)
#             self.include_auto_message_checkBox.setEnabled(True)
#         else:
#             print('not enabled')
#             self.just_send_the_message_checkBox.setChecked(True)
#             self.include_auto_message_checkBox.setEnabled(False)

    def update_completer(self):
        """
            Update widgets after user input. Required for auto completion.
            TODO
            This is not the best solution but working, rewrite in the future.
        """
        self.your_email = str(self.email_lineEdit.text())
        self.copy_to = str(self.copy_to_lineEdit.text())

        self.email_password_gridLayout.removeWidget(self.email_lineEdit)
        self.email_lineEdit.deleteLater()
        self.email_lineEdit = None

        self.copy_and_subject_gridLayout.removeWidget(self.copy_to_lineEdit)
        self.copy_to_lineEdit.deleteLater()
        self.copy_to_lineEdit = None

        self.email_lineEdit = AutoCompleteEdit(self.read_csv())
        self.copy_to_lineEdit = AutoCompleteEdit(self.read_csv())
        self.email_password_gridLayout.addWidget(self.email_lineEdit, 0, 0, 1, 1)
        self.copy_and_subject_gridLayout.addWidget(self.copy_to_lineEdit, 0, 0)

        self.email_lineEdit.setText(self.your_email)
        self.copy_to_lineEdit.setText(self.copy_to)

        self.setTabOrder(self.email_lineEdit, self.password_lineEdit.focusProxy())
        self.setTabOrder(self.password_lineEdit, self.copy_to_lineEdit)
        self.setTabOrder(self.copy_to_lineEdit.focusProxy(), self.subject_lineEdit)
        self.setTabOrder(self.subject_lineEdit, self.include_auto_message_checkBox)
        self.setTabOrder(self.include_auto_message_checkBox, self.message_textEdit)
        self.setTabOrder(self.message_textEdit, self.cancel_pushButton)
        self.setTabOrder(self.cancel_pushButton, self.execute_pushButton)

        self.setup_ui_text()

    def setup_ui_text(self):
        # setup widget texts
        self.cancel_pushButton.setText(cancel_pushButton_text)
        self.execute_pushButton.setText(execute_pushButton_text)
        self.include_auto_message_checkBox.setText(include_auto_message_checkBox_text)
        self.just_send_the_message_checkBox.setText(just_send_the_message_checkBox_text)
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
        self.just_send_the_message_checkBox.setToolTip(just_send_the_message_checkBox_toolTip)

        self.version_label.setText(version_label_text)

    def quit(self):
        """
            Close the panel.
        """
        self.close()

    def return_not_matches(self, L1, L2):
        return [[x for x in L1 if x not in L2], [x for x in L2 if x not in L1]]

    def return_matches(self, L1, L2):
        return list(set(L1) & set(L2))

    def read_csv(self):
        """
            Read csv file.
        """
        dir = os.path.dirname(__file__)
        csv_filename = os.path.join(dir, address_cache)
        ifile = open(csv_filename, "rb")
        reader = csv.reader(ifile)

        for row in reader:
            pass
        return row

    def write_csv(self):
        """
            Write csv file.
            TODO
            Rewrite in the future.
        """
        # remove whitespaces
        self.e_mail = ''.join(self.email_lineEdit.text().split())
        # split to new list
        self.e_mail = self.e_mail.split(',')
        # filter empty items
        self.e_mail = filter(None, self.e_mail)

        # remove whitespaces
        self.copy_to = ''.join(self.copy_to_lineEdit.text().split())
        # split to new list
        self.copy_to = self.copy_to.split(',')
        # filter empty items
        self.copy_to = filter(None, self.copy_to)

        # build the extended contact list
        self.extended_address_list = self.copy_to + self.e_mail

        dir = os.path.dirname(__file__)
        csv_filename = os.path.join(dir, address_cache)

        if os.stat(csv_filename).st_size == 0:
            # if address_cache size is 0 add initial content
            ifile = open(csv_filename, "wb")

            spamwriter = csv.writer(ifile, sys.stdout, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(self.copy_to)

            ifile.close()
        elif self.extended_address_list == '':
            pass
        elif len(self.e_mail) > 1:
            pass
        elif self.extended_address_list != self.read_csv():
            # add new address to address_cache
            self.current_addresses = self.read_csv()

            self.not_matched_addresses = self.return_not_matches(self.extended_address_list, self.current_addresses)
            self.not_matched_addresses = [j for i in self.not_matched_addresses for j in i]
            self.not_matched_addresses = filter(None, self.not_matched_addresses)

            self.matched_addresses = self.return_matches(self.read_csv(), self.extended_address_list)

            ifile = open(csv_filename, "wb")
            spamwriter = csv.writer(ifile, sys.stdout, delimiter=",", quoting=csv.QUOTE_NONE)
            spamwriter.writerow(self.matched_addresses + self.not_matched_addresses)

            ifile.close()
        else:
            # in all other casese just open the file and close it
            ifile = open(csv_filename, "rb")

            ifile.close()

    def setup_window_location(self):
        """
            Setup window properties.
        """
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        x = screen.width()/2-(WINDOW_WIDTH/2)
        y = screen.height()/2-(WINDOW_HEIGHT/2)-screen.height()/12
        self.move(x, y)

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
            self.info_label.setText(no_selected_write_message)
        elif self.selected_server not in [j for i in SERVER_INFO for j in i]:
            self.execute_render()
            nuke.message(render_done_but_not_sent_warning_text)
        elif self.user_account_check(self.your_email, self.your_password, self.copy_to) == False:
            self.info_label.setText(info_label_warning_text)
        elif self.just_send_the_message_checkBox.isChecked():
            self.info_label.setText(info_label_text)
            self.prepare_and_send_message_only(self.your_email, self.your_password, self.copy_to)
            self.info_label.setText(info_label_text)
            self.quit()
            nuke.message(message_sent)
        else:
            self.info_label.setText(info_label_text)
            self.execute_render()
            # send mail
            self.prepare_and_send_message_after_render(self.your_email, self.your_password, self.copy_to)
            self.info_label.setText(info_label_text)

    def cleanup_write_list_message(self, write_list):
        """
            Reformat the write_list, look better.
        """
        self.write_list = str(write_list)
        self.write_list = self.write_list.replace("'", "")[1:-1]
        return self.write_list

    def prepare_and_send_message_after_render(self, your_email, your_password, copy_to):
        """
            Send message with the write_list.
            TODO
            Rewrite in the future.
        """
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

    def prepare_and_send_message_only(self, your_email, your_password, copy_to):
        """
            Send message with the write_list.
            TODO
            Rewrite in the future.
        """
        self.nodes = nuke.selectedNodes('Write')

        self.write_list = []
        for i, node in enumerate(self.nodes):
            writers = "%s" % (node.name())
            self.write_list.append(writers)

        if self.include_auto_message_checkBox.isChecked():
            self.your_message = self.message_textEdit.toPlainText() + "<br><br>" + self.cleanup_write_list_message(self.write_list)
        else:
            self.your_message = self.message_textEdit.toPlainText()

        self.message = SendMail(self.your_email, self.your_password, self.copy_to)
        self.message.send_message(self.your_subject, self.your_message)

        del self.your_password

    def user_account_check(self, your_email, your_password, copy_to):
        self.message = SendMail(self.your_email, self.your_password, self.copy_to)

        return self.message.ret

    def create_address_cache(self):
        """
            Create address_cache file.
        """
        dir = os.path.dirname(__file__)
        csv_filename = os.path.join(dir, address_cache)

        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w'): pass

        if os.stat(csv_filename).st_size == 0:
            ifile = open(csv_filename, "wb")
            spamwriter = csv.writer(ifile, sys.stdout, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow('')
            ifile.close()


# if __name__ == "__main__":
#     aa = WriteandNotify()
#     aa.show()


def main(a):
    pass
