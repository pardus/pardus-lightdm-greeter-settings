#!/usr/bin/env python3
import sys
import os
import pwd
import shutil

WALLPAPER = "/var/lib/lightdm/wallpaper"


def open_as_caller(path):
    """This script runs as root and the path comes from the user, a link in
    the home directory must not reach files the user cannot read."""
    uid = os.environ.get("PKEXEC_UID", "")
    if not uid.isdigit() or os.geteuid() != 0:
        return open(path, "rb")

    entry = pwd.getpwuid(int(uid))
    groups = os.getgrouplist(entry.pw_name, entry.pw_gid)
    saved_groups = os.getgroups()
    try:
        os.setgroups(groups)
        os.setresgid(-1, entry.pw_gid, 0)
        os.setresuid(-1, entry.pw_uid, 0)
        return open(path, "rb")
    finally:
        os.setresuid(-1, 0, 0)
        os.setresgid(-1, 0, 0)
        os.setgroups(saved_groups)


def remove_wallpaper():
    if os.path.lexists(WALLPAPER):
        os.unlink(WALLPAPER)


def copy_wallpaper(path):
    with open_as_caller(path) as source:
        remove_wallpaper()
        # lightdm owns this directory, never follow a link left there
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        with os.fdopen(os.open(WALLPAPER, flags, 0o644), "wb") as target:
            shutil.copyfileobj(source, target)


# print(sys.argv)
if len(sys.argv) > 2:
    config = sys.argv[1]
    background = sys.argv[2]
    autologin = sys.argv[3]
    if autologin not in ["", None]:
        # This goes into a lightdm config, a newline would add a new setting
        try:
            pwd.getpwnam(autologin)
        except KeyError:
            print("Unknown autologin user: {!r}".format(autologin), file=sys.stderr)
            sys.exit(1)
    if not os.path.isdir("/etc/pardus/greeter.conf.d/"):
        os.mkdir("/etc/pardus/greeter.conf.d/")
    with open("/etc/pardus/greeter.conf.d/00-greeter-settings.conf", "w") as f:
        f.write(config)
    # After the first save the path already points at the copy
    if background != WALLPAPER:
        if os.path.isfile(background):
            copy_wallpaper(background)
        else:
            remove_wallpaper()
    autologin_file = "/usr/share/lightdm/lightdm.conf.d/99-pardus-lightdm-greeter-autologin.conf"
    if autologin not in ["", None]:
        data = "[Seat:*]\n"
        data += "autologin-user={}\n".format(autologin)
        with open(autologin_file, "w") as f:
            f.write(data)
    else:
        if os.path.isfile(autologin_file):
            os.unlink(autologin_file)
