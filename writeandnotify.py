##################
"""
    write_and_notify
    Levente Vass
    April 2018
    levente.shadow@gmail.com

    Usage:
     1. fill the account details section
     2. setup frame range on selected write node
     3. select one or multiple wite nodes
     4. execute the script in the script editor

    You can execute multiple write nodes, sorted by render order.

    Thanks for the code snippets Morten Andersen and Ricky Wilson.

"""

import nuke
import smtplib

# account details
your_email = 'your email address here'
your_password = 'your password here'

subject_content = "Render is Done" 
message_content = "detailed message"

class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
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

def renderSelected():
    nodes = nuke.selectedNodes('Write')

    # sort by render order
    nodes.sort(key=lambda x: x['render_order'].value())

    # disable proxy
    proxy = nuke.root()['proxy'].value()
    nuke.root()['proxy'].setValue(False)

    # empty tuple for storing frame start/end/incr
    t = ()  # only used in executeMultiple()

    # render!
    c = len(nodes)
    for i, node in enumerate(nodes):
        f = int(node['first'].value())
        l = int(node['last'].value())

        # execute node
        nuke.execute(node, f, l, 1)
        print("%d of %d, %s is done" % (i, c, node.name()))
        if nuke.GUI:
            gm = Gmail(your_email, your_password)
            gm.send_message(subject_content, message_content)
        t = t + ((f, l, 1),)  # only used in executeMultiple()

    # execute multiple write nodes (writeNodes, ranges)
    # nuke.executeMultiple(tuple, tuple(tuple, tuple, tuple,))
    #nuke.executeMultiple(nodes, t)

    # set proxy back to original value
    nuke.root()['proxy'].setValue(proxy)

renderSelected()
