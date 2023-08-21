#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys
sys.path.insert(0, '/usr/share/pardus/pardus-lightdm-greeter-settings/')
from MainWindow import MainWindow

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.set_icon_name("lightdm-pardus-greeter-settings")
win.show_all()
Gtk.main()
