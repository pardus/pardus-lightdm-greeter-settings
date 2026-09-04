#!/usr/bin/env python3
import configparser
import os
import pwd
import re
import shutil
import sys

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*\$?$")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".svg"}
MAX_WALLPAPER_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_autologin_user(user):
    if not user:
        return True
    if "\n" in user or "\r" in user:
        return False
    if user == "root" or user.startswith("-"):
        return False
    if not USERNAME_REGEX.match(user) or len(user) > 32:
        return False
    try:
        pwd.getpwnam(user)
        return True
    except KeyError:
        return False


def validate_wallpaper_file(path):
    if not path or not os.path.isabs(path):
        return False
    if os.path.islink(path):
        return False
    if not os.path.isfile(path):
        return False
    try:
        if os.path.getsize(path) > MAX_WALLPAPER_SIZE:
            return False
    except OSError:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS


def main():
    if len(sys.argv) < 4:
        sys.stderr.write(f"Usage: {sys.argv[0]} <config_ini> <background_path> <autologin_user>\n")
        sys.exit(1)

    config = sys.argv[1]
    background = sys.argv[2].strip()
    autologin = sys.argv[3].strip()

    # Validate INI config syntax if non-empty
    if config.strip():
        try:
            parser = configparser.RawConfigParser()
            parser.read_string(config)
        except Exception as e:
            sys.stderr.write(f"Error: Invalid configuration format: {e}\n")
            sys.exit(1)

    # Validate autologin user
    if autologin and not validate_autologin_user(autologin):
        sys.stderr.write(f"Error: Invalid or unauthorized autologin user '{autologin}'.\n")
        sys.exit(1)

    # 1. Write greeter config
    conf_dir = "/etc/pardus/greeter.conf.d"
    if not os.path.isdir(conf_dir):
        os.makedirs(conf_dir, mode=0o755, exist_ok=True)
    with open(os.path.join(conf_dir, "00-greeter-settings.conf"), "w") as f:
        f.write(config)

    # 2. Handle wallpaper
    dest_wallpaper = "/var/lib/lightdm/wallpaper"
    if validate_wallpaper_file(background):
        shutil.copyfile(background, dest_wallpaper)
    else:
        if os.path.isfile(dest_wallpaper) or os.path.islink(dest_wallpaper):
            try:
                os.unlink(dest_wallpaper)
            except OSError:
                pass

    # 3. Handle autologin configuration
    autologin_file = "/usr/share/lightdm/lightdm.conf.d/99-pardus-lightdm-greeter-autologin.conf"
    if autologin:
        data = f"[Seat:*]\nautologin-user={autologin}\n"
        with open(autologin_file, "w") as f:
            f.write(data)
    else:
        if os.path.isfile(autologin_file) or os.path.islink(autologin_file):
            try:
                os.unlink(autologin_file)
            except OSError:
                pass


if __name__ == "__main__":
    main()
