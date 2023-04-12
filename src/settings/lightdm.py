# Lightdm
self.settings["lightdm"].set_data("allow-root-login",{
    "label":_("Allow login as root"),
     "value": config.get("allow-root-login","true")
})
self.settings["lightdm"].set_data("allow-autologin",{
    "label":_("Allow autologin"),
     "value": config.get("allow-autologin","true")
})
self.settings["lightdm"].set_data("autologin-user",{
    "label":_("Autologin username"),
     "value": config.get("autologin-user","")
})

