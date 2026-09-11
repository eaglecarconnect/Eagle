from pathlib import Path
from PIL import Image

folder = Path("Assets/images-optimized")
bad = []

for f in folder.glob("*.webp"):
    try:
        with Image.open(f) as im:
            im.verify()
    except Exception:
        bad.append(f)

print("Bad WebP files:", len(bad))

for f in bad:
    print(f)