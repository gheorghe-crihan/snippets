#!/bin/sh

java -XstartOnFirstThread \
  -cp ${HOME}/Sandbox/snippets/radio-toggle-button/target/org.eclipse.swt.cocoa.macosx.x86_64-3.131.0.jar \
  -jar ${HOME}/Sandbox/jython/jython-2.7.2_0+installer.darwin_18.noarch/opt/local/share/java/jython/jython.jar \
  radio_toggle_button.py
 