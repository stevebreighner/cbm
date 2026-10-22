from pathlib import Path
from datetime import date

from artwork import (
    CONTENT_DIR,
    IMAGE_DIR,
    THUMB_SIZES,
    slugify,
    yaml_quote,
    save_jpeg,
    save_cropped_jpeg,
    suggest_orientation,
)

PHOTO_DIR = Path.home() / "Desktop" / "cbm_photos"

extensions = {".jpg", ".jpeg", ".png", ".webp"}

photos = sorted(
    p for p in PHOTO_DIR.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
)

if not photos:
    raise SystemExit(f"No photos found in {PHOTO_DIR}")

jobs = []

for source in photos:
    title = source.stem.replace("_", " ").title()
    slug = slugify(title)
    md_file = CONTENT_DIR / f"{slug}.md"
    art_dir = IMAGE_DIR / slug

    if md_file.exists() or art_dir.exists():
        raise SystemExit(
            f"Stopped before importing: '{title}' already has a record "
            f"or image directory.\nChecked: {md_file}\n           {art_dir}"
        )

    jobs.append((source, title, slug, md_file, art_dir))

print("Ready to import:")
for source, title, slug, md_file, art_dir in jobs:
    print(f"  {title}  <-  {source.name}")

answer = input("\nType IMPORT to continue: ")
if answer != "IMPORT":
    raise SystemExit("Cancelled; no artwork imported.")

CONTENT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

for source, title, slug, md_file, art_dir in jobs:
    art_dir.mkdir(parents=True, exist_ok=False)

    main_image = art_dir / "main.jpg"
    save_jpeg(source, main_image)

    orientation = suggest_orientation(main_image)
    if orientation not in THUMB_SIZES:
        orientation = "square"

    for kind, size in THUMB_SIZES.items():
        save_cropped_jpeg(
            main_image,
            art_dir / f"thumb-{kind}.jpg",
            size,
        )

    (art_dir / "thumb.jpg").write_bytes(
        (art_dir / f"thumb-{orientation}.jpg").read_bytes()
    )

    image_root = f"/images/artwork/{slug}"
    record = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date.today().isoformat()}",
        f"orientation: {yaml_quote(orientation)}",
        f'thumb: "{image_root}/thumb-{orientation}.jpg"',
        "thumbs:",
        f'  portrait: "{image_root}/thumb-portrait.jpg"',
        f'  square: "{image_root}/thumb-square.jpg"',
        f'  landscape: "{image_root}/thumb-landscape.jpg"',
        f'image: "{image_root}/main.jpg"',
        'medium: ""',
        'size: ""',
        'year: ""',
        'price: ""',
        'status: "Available"',
        "---",
        "",
        "",
    ]

    md_file.write_text("\n".join(record), encoding="utf-8")
    print(f"Created: {md_file.relative_to(Path.cwd())}")

print(f"\nSuccessfully imported {len(jobs)} artworks.")
print("Original photos were left unchanged.")
print("Review prices, medium, dimensions, year, and status before publishing.")
