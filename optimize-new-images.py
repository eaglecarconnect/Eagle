from pathlib import Path
from PIL import Image

source = Path("Assets/images")
output = Path("Assets/images-optimized")

output.mkdir(parents=True, exist_ok=True)

extensions = {".jpg", ".jpeg", ".JPG", ".JPEG"}

for file in source.iterdir():
    if file.suffix not in extensions:
        continue

    webp = output / f"{file.stem}.webp"

    # Don't replace an optimized image that already exists
    if webp.exists():
        print(f"SKIP: {file.name}")
        continue

    try:
        with Image.open(file) as img:
            # Convert to RGB/RGBA as required by WebP
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # Resize only if the image is larger than 1600px wide
            max_width = 1600

            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize(
                    (max_width, new_height),
                    Image.Resampling.LANCZOS
                )

            img.save(
                webp,
                "WEBP",
                quality=82,
                method=6
            )

            print(f"OK:   {file.name} -> {webp.name}")

    except Exception as e:
        print(f"ERROR: {file.name} -> {e}")

print("\nDone.")
