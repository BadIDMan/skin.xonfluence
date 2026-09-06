import sys
from datetime import datetime

import xbmc
import xbmcgui
import xbmcvfs

TITLE = "Xonfluence - Settings backup"
SETTINGS_FILE = ("special://profile/addon_data/skin.xonfluence/settings.xml")

def notify(message):
    xbmcgui.Dialog().notification(TITLE, message, xbmcgui.NOTIFICATION_INFO, 4000)

def error(message):
    xbmcgui.Dialog().ok(TITLE, message)

def switch_to_estuary():
    xbmc.executebuiltin("LoadSkin(skin.estuary)")
    xbmc.sleep(2500)

def switch_to_xonfluence():
    xbmc.executebuiltin("LoadSkin(skin.xonfluence)")
    xbmc.sleep(2500)

# =========================================================
# SAVE BACKUP
# =========================================================
def save_backup():
    if not xbmcvfs.exists(SETTINGS_FILE):
        error("Xonfluence settings.xml was not found.")
        return

    backup_dir = xbmcgui.Dialog().browseSingle(
        3,
        "Select folder for Xonfluence backup",
        "",
        "",
        False,
        False,
        ""
    )

    if not backup_dir:
        return

    if not backup_dir.endswith("/"):
        backup_dir += "/"

    backup_name = "xonfluence_settings_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xml"
    backup_file = backup_dir + backup_name

    if not xbmcvfs.copy(SETTINGS_FILE, backup_file):
        error("Backup could not be saved.")
        return

    notify("Backup saved successfully.")

# =========================================================
# LOAD BACKUP
# =========================================================
def load_backup():
    backup_file = xbmcgui.Dialog().browseSingle(
        1,
        "Select Xonfluence backup",
        "",
        ".xml",
        False,
        False,
        ""
    )

    if not backup_file:
        return

    if not xbmcvfs.exists(backup_file):
        error("Selected backup file was not found.")
        return

    answer = xbmcgui.Dialog().yesno(
        TITLE,
        "Load the selected Xonfluence settings?"
    )

    if not answer:
        return

    try:
        switch_to_estuary()

        if xbmcvfs.exists(SETTINGS_FILE):
            xbmcvfs.delete(SETTINGS_FILE)

        if not xbmcvfs.copy(backup_file, SETTINGS_FILE):
            raise RuntimeError("Backup file could not be copied.")

        xbmc.sleep(1000)
        switch_to_xonfluence()

    except Exception as exc:
        error("Backup could not be restored.\n\n" + str(exc))

# =========================================================
# RESET SETTINGS
# =========================================================
def reset_settings():
    answer = xbmcgui.Dialog().yesno(
        TITLE,
        "Reset Xonfluence settings to defaults?"
    )

    if not answer:
        return

    try:
        switch_to_estuary()

        if xbmcvfs.exists(SETTINGS_FILE):
            xbmcvfs.delete(SETTINGS_FILE)

        xbmc.sleep(1000)
        switch_to_xonfluence()

    except Exception as exc:
        error("Settings could not be reset.\n\n" + str(exc))

# =========================================================
# MAIN
# =========================================================
def main():
    if len(sys.argv) < 2:
        error("No operation was specified.")
        return

    action = sys.argv[1].lower()

    if action == "backup":
        save_backup()
    elif action == "restore":
        load_backup()
    elif action == "reset":
        reset_settings()
    else:
        error("Unknown operation: " + action)

if __name__ == "__main__":
    main()