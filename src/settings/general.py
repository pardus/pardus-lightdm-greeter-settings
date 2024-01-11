# General
_("General")
self.settings["main"].set_data("scale", {
    "label": _("Scale"),
    "value": config.get("scale", "1"),
    "digit": "2"
})
self.settings["main"].set_data("gtk-theme", {
    "label": _("GTK theme"),
    "options": util.list_gtk_themes(),
    "value": config.get("gtk-theme", "Adwaita")
})

self.settings["main"].set_data("gtk-icon-theme-name", {
    "label": _("Icon theme"),
    "options": util.list_icon_themes(),
    "value": config.get("gtk-icon-theme-name", "Adwaita")
})

self.settings["main"].set_data("font-size", {
    "label": _("Font Size"),
    "value": config.get("font-size", "10"),
    "digit": "0"
})
self.settings["main"].set_data("dark-theme", {
    "label": _("Prefer dark theme"),
    "value": config.get("dark-theme", "true")
})
self.settings["main"].set_data("touch-mode", {
    "label": _("Touch screen mode"),
    "value": config.get("touch-mode", "false")
})
self.settings["main"].set_data("blank-timeout", {
    "label": _("Black screen timeout (sec)"),
    "value": config.get("blank-timeout", "300")
})
self.settings["main"].set_data("init", {
    "label": _("Initial command"),
    "value": config.get("init", "")
})
self.settings["main"].set_data("prestart", {
    "label": _("Start command before login"),
    "value": config.get("prestart", "")
})
