import platform

OS = platform.system()

if OS == "Windows":
    from windows import run

elif OS == "Linux":
    from linux import run

elif OS == "Darwin":
    from mac import run

else:
    raise Exception("Sistema no soportado")

run()