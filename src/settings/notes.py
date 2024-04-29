# General
_("Display")
self.settings["notes"].set_data("enabled", {
    "label": _("Enable Notes"),
    "value": config.get("notes", "true", "enabled"),
})
self.settings["notes"].set_data("editable", {
    "label": _("Editable"),
    "value": config.get("editable", "true", "editable"),
})
self.settings["notes"].set_data("text-file", {
    "label": _("Text file"),
    "value": config.get("text-file", "", "editable"),
})
