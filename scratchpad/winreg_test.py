import winreg


def _read_registry(root, key, value):

    try:
        hkey = winreg.OpenKey(root, key)
        (val, typ) = winreg.QueryValueEx(hkey, value)
    except OSError:
        val = None
    winreg.CloseKey(hkey)
    return val


oneDrivePath = _read_registry(
    winreg.HKEY_CURRENT_USER, "Environment", "OneDriveConsumer"
)
print("OneDrivePath : ", oneDrivePath)
