# Lightdm
_("User List")
self.settings["userlist"].set_data("enabled", {
    "label": _("Enable username list"),
    "value": config.get("enabled", "true", "userlist")
})
self.settings["userlist"].set_data("show-realname", {
    "label": _("Show real names"),
    "value": config.get("show-realname", "true", "userlist")
})
self.settings["userlist"].set_data("user-hide-button", {
    "label": _("Enable hide user button"),
    "value": config.get("user-hide-button", "true", "userlist")
})
