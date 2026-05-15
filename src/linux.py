import json

from system_info import get_system
from hardware import get_cpu, get_ram, get_disks


def run():

    report = {
        "Sistema": get_system(),
        "CPU": get_cpu(),
        "RAM": get_ram(),
        "Discos": get_disks()
    }

    print(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        )
    )