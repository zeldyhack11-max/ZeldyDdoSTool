import os

def oku(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None

# Olası dosya yolları (cihaza göre değişir)
paths = {
    "design_capacity": [
        "/sys/class/power_supply/battery/charge_full_design",
        "/sys/class/power_supply/battery/energy_full_design"
    ],
    "current_capacity": [
        "/sys/class/power_supply/battery/charge_full",
        "/sys/class/power_supply/battery/energy_full"
    ]
}

design = None
current = None

for p in paths["design_capacity"]:
    design = oku(p)
    if design:
        break

for p in paths["current_capacity"]:
    current = oku(p)
    if current:
        break

if design and current:
    design = int(design)
    current = int(current)

    health = (current / design) * 100
    print(f"Pil sağlığı: %{health:.2f}")
else:
    print("Değerler okunamadı (root lazım ya da cihaz desteklemiyor)")
