#!/usr/bin/env python3
from MainWindow import MainWindow
from gi.repository import Gtk
import gi
gi.require_version("Gtk", "3.0")

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.set_icon_name("lightdm-pardus-greeter-settings")
win.show_all()
Gtk.main()
