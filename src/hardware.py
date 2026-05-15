import psutil
import platform
import cpuinfo


def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


# =====================================
# CPU
# =====================================

def get_cpu():

    info = cpuinfo.get_cpu_info()

    return {
        "Procesador": info.get("brand_raw"),
        "NucleosFisicos": psutil.cpu_count(logical=False),
        "NucleosTotales": psutil.cpu_count(logical=True),
        "UsoCPU": psutil.cpu_percent(interval=1)
    }


# =====================================
# RAM
# =====================================

def get_ram():

    vm = psutil.virtual_memory()

    return {
        "RAMTotalGB": bytes_to_gb(vm.total),
        "RAMUsadaGB": bytes_to_gb(vm.used),
        "RAMLibreGB": bytes_to_gb(vm.available)
    }


# =====================================
# DISKS
# =====================================

def get_disks():

    disks = []

    for partition in psutil.disk_partitions():

        try:

            usage = psutil.disk_usage(
                partition.mountpoint
            )

            disks.append({
                "Particion": partition.device,
                "SistemaArchivos": partition.fstype,
                "TotalGB": bytes_to_gb(usage.total),
                "LibreGB": bytes_to_gb(usage.free),
                "UsoPorcentaje": usage.percent
            })

        except:
            pass

    return disks