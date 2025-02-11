# General
_("Display")
self.settings["monitor"].set_data("mirror", {
    "label": _("Mirror monitors"),
    "value": config.get("mirror", "true", "screen"),
})
self.settings["monitor"].set_data("default-monitor-name", {
    "label": _("Default monitor"),
    "options": util.list_monitors(),
    "value": config.get("default-monitor-name", util.list_monitors()[0], "screen")
})

settings = self.settings


def mirror_state_event(widget, state):
    global settings
    settings["monitor"].widgets["default-monitor-name"].set_sensitive(
        not state)


state = config.get("mirror", "true", "screen").lower() == "true"
settings["monitor"].widgets["default-monitor-name"].set_sensitive(not state)
self.settings["monitor"].widgets["mirror"].state_event = mirror_state_event
