# General
_("Display")
self.settings["monitor"].set_data("mirror",{
    "label":_("Mirror monitors"),
    "value": config.get("mirror","true", "monitor"),
})
self.settings["monitor"].set_data("default-monitor",{
    "label":_("Default monitor"),
    "value": config.get("default-monitor","1", "monitor"),
})
