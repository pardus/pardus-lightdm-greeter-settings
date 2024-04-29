#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys, os
appdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, appdir)
from MainWindow import MainWindow

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.set_icon_name("lightdm-pardus-greeter-settings")
win.show_all()
Gtk.main()
