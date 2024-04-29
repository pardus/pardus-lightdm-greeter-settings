# General
_("Notes")
self.settings["notes"].set_data("enabled", {
    "label": _("Enable notes"),
    "value": config.get("enabled", "true", "notes"),
})
self.settings["notes"].set_data("editable", {
    "label": _("Editable"),
    "value": config.get("editable", "true", "notes"),
})
self.settings["notes"].set_data("text-file", {
    "label": _("Text file"),
    "value": config.get("text-file", "", "notes"),
})
