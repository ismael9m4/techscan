import platform
import socket
import subprocess
import os
import datetime
import psutil

try:
    import distro
except:
    distro = None

if platform.system() == "Windows":
    import winreg


# =====================================
# DEVICE TYPE
# =====================================

def get_device_type():

    battery = psutil.sensors_battery()

    if battery:
        return "Notebook"

    return "PC"


# =====================================
# BIOS MODE
# =====================================

def get_bios_mode():

    os_type = platform.system()

    try:

        if os_type == "Windows":

            output = subprocess.getoutput(
                'powershell "(Confirm-SecureBootUEFI)"'
            )

            if "True" in output or "False" in output:
                return "UEFI"

            return "Legacy"

        elif os_type == "Linux":

            if os.path.exists("/sys/firmware/efi"):
                return "UEFI"

            return "Legacy"

        elif os_type == "Darwin":
            return "UEFI"

    except:
        pass

    return "Desconocido"


# =====================================
# INSTALL DATE
# =====================================

def get_install_date():

    os_type = platform.system()

    try:

        if os_type == "Windows":

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            )

            install_time = winreg.QueryValueEx(
                key,
                "InstallDate"
            )[0]

            return datetime.datetime.fromtimestamp(
                install_time
            ).strftime("%Y-%m-%d %H:%M:%S")

        elif os_type == "Linux":

            stat = os.stat('/')

            return datetime.datetime.fromtimestamp(
                stat.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")

        elif os_type == "Darwin":

            stat = os.stat('/')

            return datetime.datetime.fromtimestamp(
                stat.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")

    except:
        return "No disponible"


# =====================================
# UPTIME
# =====================================

def get_uptime_hours():

    try:

        boot_time = datetime.datetime.fromtimestamp(
            psutil.boot_time()
        )

        now = datetime.datetime.now()

        uptime = now - boot_time

        return round(
            uptime.total_seconds() / 3600,
            2
        )

    except:
        return "No disponible"


# =====================================
# SYSTEM INFO
# =====================================

def get_system():

    os_type = platform.system()

    data = {
        "Hostname": socket.gethostname(),
        "Arquitectura": platform.machine(),
        "Kernel": platform.release(),
        "TipoEquipo": get_device_type(),
        "BIOS": get_bios_mode(),
        "FechaInstalacion": get_install_date(),
        "UptimeHoras": get_uptime_hours()
    }

    # WINDOWS
    if os_type == "Windows":

        try:

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            )

            product_name = winreg.QueryValueEx(
                key,
                "ProductName"
            )[0]

            display_version = winreg.QueryValueEx(
                key,
                "DisplayVersion"
            )[0]

            current_build = winreg.QueryValueEx(
                key,
                "CurrentBuild"
            )[0]

            ubr = winreg.QueryValueEx(
                key,
                "UBR"
            )[0]

            data.update({
                "Sistema": product_name,
                "Version": display_version,
                "Build": f"{current_build}.{ubr}"
            })

        except Exception as e:
            data["ErrorWindows"] = str(e)

    # LINUX
    elif os_type == "Linux":

        try:

            if distro:

                data.update({
                    "Sistema": distro.name(pretty=True),
                    "Version": distro.version(),
                    "Codename": distro.codename()
                })

            else:

                data.update({
                    "Sistema": platform.platform()
                })

        except Exception as e:
            data["ErrorLinux"] = str(e)

    # MACOS
    elif os_type == "Darwin":

        try:

            version = subprocess.getoutput(
                "sw_vers"
            )

            data.update({
                "Sistema": "macOS",
                "Info": version
            })

        except Exception as e:
            data["ErrorMac"] = str(e)

    return data