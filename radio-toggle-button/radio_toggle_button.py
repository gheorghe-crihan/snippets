#!/usr/bin/env jython

from org.eclipse.swt import SWT
from org.eclipse.swt.layout import FillLayout
from org.eclipse.swt.widgets import Button, Control, Display, Event, Listener, Shell

def main():
# Not implemented on OSX!
#    display = Display()
    display = Display.getCurrent()
    shell = Shell(display)
    shell.setLayout(FillLayout())
    class MyListener(Listener):
        def handleEvent(self, e):
            children = shell.getChildren()
            for i in range(len(children)):
                child = children[i]
                if e.widget != child: 
                   if isinstance(child, Button) and \
                      (child.getStyle() & SWT.TOGGLE) != 0:
                      child.setSelection(False)
                else:
                    print("[B%d] selected.\n" % (i, ))
            e.widget.setSelection(True)

    listener = MyListener()
    for i in range(20):
        button = Button(shell, SWT.TOGGLE)
        button.setText("B%d" % (i,))
        button.addListener(SWT.Selection, listener)
        if i == 0:
            button.setSelection(True)
    shell.pack()
    shell.open()
    while not shell.isDisposed():
        if not display.readAndDispatch():
            display.sleep()
    display.dispose()

try:
    main()
except AttributeError:
    # Somehow, at first the display object DOES NOT get initialized,
    # giving AttributeError, so try a second time. And have a double
    # window as present! :)
    main()
