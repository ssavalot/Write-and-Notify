Write and Notify
v1.2
Levente Vass
April 2018
levente.shadow@gmail.com

CHANGELOG

v1.2
- Auto completion feature have benn added.
  This change affects the 'e-mail' and 'send a copy' fields.
  The addresses are automatically added to the completion list and
  stored in the .nuke/address_cache.csv file.

  You can edit manually the address_cache.csv, if you want to change something.
  Follow this format:
      example1@any.com,example2@any.com,example3@any.com...

v1.1
- Send a copy field have been added. You can send a copy of the message to multiple recipients.
- Code cleanup and better error handling.

INSTALL

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

USAGE

    1. Setup frame range on renderable write node(s).
    2. Type your e-mail and password if you want to receive a notification, everything else are optional.
    3. Select one or multiple wite nodes.
    4. Press Run button. If you leave the fields blank, you can execute selected Write nodes.

    The tool currently only works with g-mail and yahoo accounts.
    You can execute multiple write nodes, the rendering is sorted by render order.

SECURITY

    The entered password is not encrypted, please use temp account for messaging.

COMPATIBILTY

    NUKE 11 and above


Thanks for the code snippets Morten Andersen and Ricky Wilson.
