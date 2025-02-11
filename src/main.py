#!/usr/bin/env python3
import os
import sys

from MainWindow import MainWindow

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

appdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, appdir)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.set_icon_name("lightdm-pardus-greeter-settings")
win.show_all()
Gtk.main()
