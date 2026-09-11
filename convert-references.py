from pathlib import Path
import re

files = ["car-single.html", "car.html"]

pattern = re.compile(
    r'Assets/images/([^"\'),]+\.(?:jpg|JPG|jpeg|JPEG))'
)

total = 0
changed = 0
missing = []

for filename in files:
    path = Path(filename)
    text = path.read_text(encoding="utf-8")

    def replace_image(match):
        global total, changed

        total += 1

        original_name = match.group(1)
        webp_name = Path(original_name).with_suffix(".webp")
        optimized = Path("Assets/images-optimized") / webp_name

        if optimized.exists():
            changed += 1
            return "Assets/images-optimized/" + webp_name.name

        missing.append(str(optimized))
        return match.group(0)

    new_text = pattern.sub(replace_image, text)
    path.write_text(new_text, encoding="utf-8")

print("References checked:", total)
print("Changed to WebP:", changed)
print("Missing WebP:", len(missing))

if missing:
    print("\nMissing files:")
    for item in missing:
        print(item)