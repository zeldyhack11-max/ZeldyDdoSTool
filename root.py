import os
import platform
import subprocess

print("📱 Telefon Bilgi Aracı")
print("-" * 30)

print("Sistem:", platform.system())
print("Mimari:", platform.machine())
print("Python:", platform.python_version())

def komut(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return "Alınamadı"

print("\n🔋 Batarya:")
print(komut("termux-battery-status"))

print("\n💾 Depolama:")
print(komut("df -h /data"))

print("\n🧠 RAM:")
print(komut("cat /proc/meminfo | head"))

print("\n⚙️ CPU:")
print(komut("cat /proc/cpuinfo | grep 'Hardware' | head"))

print("\n🔐 Root kontrolü:")
if os.path.exists("/system/xbin/su") or os.path.exists("/system/bin/su"):
    print("Root olabilir ✅")
else:
    print("Root bulunamadı ❌")
