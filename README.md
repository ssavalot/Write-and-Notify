Write and Notify
v1.0.0
Levente Vass
April 2018
levente.shadow@gmail.com

INSTALL:

    1.)
    Copy these files to the .nuke directory.

    writeandnotify.py 
    writeandnotify_ui.py

    2.)
    Add these lines to the menu.py file. The tool will be added to the Other menu.

    ## setup Write and Notify tool
    import writeandnotify
    writeandnotify_form = writeandnotify.WriteandNotify()
    menu.addCommand("Other/Write and Notify", "writeandnotify.main(writeandnotify_form.show())", "")

USAGE:

    1. Setup frame range on renderable write node(s).
    2. Type your e-mail and password, subject and message are optional.
    3. Select one or multiple wite nodes.
    4. Press Run button.

    The tool currently only works with g-mail and yahoo accounts.
    You can execute multiple write nodes, the rendering is sorted by render order.

SECURITY:

    The entered password is not encrypted, please use temp account for messaging.

COMPATIBILTY:

    NUKE 11 and above


Thanks for the code snippets Morten Andersen and Ricky Wilson.
