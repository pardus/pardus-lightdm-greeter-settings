# Gtk Window
_("Gtk Window")
self.settings["gtkwindow"].set_data("background",{
    "label":_("Background image"),
     "value": config.get("background","user","gtkwindow"),
     "default": "user"
})
self.settings["gtkwindow"].set_data("allow-empty-password",{
    "label":_("Allow empty password"),
     "value": config.get("allow-empty-password","true","gtkwindow")
})
self.settings["gtkwindow"].set_data("password-cache",{
    "label":_("Login without enter"),
     "value": config.get("password-cache","true","gtkwindow")
})
self.settings["gtkwindow"].set_data("username-cache",{
    "label":_("Remember last username"),
     "value": config.get("username-cache","true","gtkwindow")
})
self.settings["gtkwindow"].set_data("logo",{
    "label":_("Custom logo"),
     "value": config.get("logo","","gtkwindow"),
     "default": ""
})
