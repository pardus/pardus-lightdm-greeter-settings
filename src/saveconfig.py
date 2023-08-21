#!/usr/bin/env python3
import sys
import os
import shutil
print(sys.argv)
if len(sys.argv) > 2:
    config = sys.argv[1]
    background = sys.argv[2]
    autologin = sys.argv[3]
    with open("/etc/pardus/greeter.conf.d/00-greeter-settings.conf", "w") as f:
            f.write(config)
    if os.path.isfile(background):
        shutil.copyfile(background, "/var/lib/lightdm/wallpaper")
    else:
        if os.path.isfile("/var/lib/lightdm/wallpaper"):
            os.unlink("/var/lib/lightdm/wallpaper")
    autologin_file = "/usr/share/lightdm/lightdm.conf.d/99-pardus-lightdm-greeter-autologin.conf"
    if not (autologin == "" or autologin == None):
        data = "[Seat:*]\n"
        data += "autologin-user={}\n".format(autologin)
        with open(autologin_file, "w") as f:
            f.write(data)
    else:
        if os.path.isfile(autologin_file):
            os.unlink(autologin_file)
