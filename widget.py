import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk



class settings_object(Gtk.Box):
    def __init__(self):
        super().__init__()


class object_onoff(settings_object):
    def __init__(self):
        super().__init__()
        self.switch = Gtk.Switch()
        self.image = Gtk.Image()
        self.label = Gtk.Label()
        self.pack_start(self.image,False, False, 3)
        self.pack_start(self.label,False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.switch,False, False, 3)
        self.show_all()

    def set_data(self,data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)

    def get_value(self):
        return self.switch.get_state()

class object_entry(settings_object):
    def __init__(self):
        super().__init__()
        self.entry = Gtk.Entry()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.entry, False, False, 3)
        self.show_all()

    def set_data(self, data):
        if "label" in data:
           self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "value" in data:
           self.entry.set_text(data["value"])

    def get_value(self):
        return self.entry.get_text()
class object_number(settings_object):
    def __init__(self):
        super().__init__()
        self.spinbutton = Gtk.SpinButton()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.spinbutton, False, False, 3)
        self.show_all()

    def set_data(self, data):
        if "label" in data:
           self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "min" in data and "max" in data:
           step = 1
           if "step" in data:
              step = int(data["step"])
           self.spinbutton.set_increments(step, step)
           self.spinbutton.set_range(int(data["min"]), int(data["max"]))
        if "value" in data:
            self.spinbutton.set_value(int(data["value"]))

    def get_value(self):
        return self.spinbutton.get_value()

class object_selection(settings_object):
    def __init__(self):
        super().__init__()
        self.label = Gtk.Label()
        self.combo = Gtk.ComboBoxText()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.combo, False, False, 3)
        self.show_all()

    def set_data(self,data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "options" in data:
            print(data["options"])
            for opt in data["options"]:
                print(opt)
                self.combo.append_text(opt)
            self.combo.set_active(0)

    def get_value(self):
        tree_iter = self.combo.get_active_iter()
        if tree_iter is not None:
            model = self.combo.get_model()
            return model[tree_iter][0]
        return ""


class Settings:
    def __init__(self):
        self.ONOFF=0
        self.COMBO=1
        self.ENTRY=2
        self.NUMBER=3
        self.widgets = {}

    def get(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for w in self.widgets:
            box.pack_start(self.widgets[w], False, False, 5)
        box.show()
        return box

    def add_option(self, name="", type=-1, data=None):
        if type == self.ONOFF:
            obj = object_onoff()
        if type == self.COMBO:
            obj = object_selection()
        if type == self.ENTRY:
            obj = object_entry()
        if type == self.NUMBER:
            obj = object_number()
        self.widgets[name] = obj
        obj.set_data(data)

    def dump(self):
        ret = {}
        for w in self.widgets:
            ret[w] = self.widgets[w].get_value()
        return ret

if __name__ == "__main__":
    w = Gtk.Window()
    s = Settings()
    s.add_option("test",s.ONOFF,{"label":"Test","image":"gtk-ok"})
    s.add_option("testf",s.COMBO,{"label":"Test", "image": "user-home","options":{"gtk-no","gtk-yes"}})
    s.add_option("test2",s.ENTRY,{"label":"Test", "image": "gtk-no", "value":"test"})
    s.add_option("test3",s.NUMBER,{"label":"Test", "image": "gtk-no", "min":0, "max": 10, "value":5})
    w.add(s.get())
    w.show()
    print(s.dump())
    Gtk.main()