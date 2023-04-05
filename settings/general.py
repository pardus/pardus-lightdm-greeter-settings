# General
self.settings["main.json"].set_data("scale",{
    "label":_("Scale"),
    "value": config.get("scale","1")
})
self.settings["main.json"].set_data("gtk-theme",{
    "label":_("Gtk theme"),
    "options": util.list_gtk_themes(),
    "value": config.get("gtk-theme","Adwaita")
})
self.settings["main.json"].set_data("font-size",{
    "label":_("Font Size"),
    "value": config.get("font-size","10")
})
self.settings["main.json"].set_data("dark-theme",{
    "label":_("Prefer dark theme"),
    "value": config.get("dark-theme","true")
})
self.settings["main.json"].set_data("blank-timeout",{
    "label":_("Black screen timeout (sec)"),
    "value": config.get("blank-timeout","300")
})
self.settings["main.json"].set_data("init",{
    "label":_("Initial command"),
    "value": config.get("init","")
})
self.settings["main.json"].set_data("prestart",{
    "label":_("Start command before login"),
     "value": config.get("prestart","")
})

