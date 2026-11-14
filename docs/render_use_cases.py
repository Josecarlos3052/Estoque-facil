"""Aplica a fronteira do sistema ao diagrama de casos de uso renderizado pelo Graphviz."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parent
source = DOCS / "casos_de_uso_base.png"
target = DOCS / "casos_de_uso.png"
if not source.exists():
    raise FileNotFoundError(source)

image = Image.open(source).convert("RGB")
draw = ImageDraw.Draw(image)
width, height = image.size
left, top = int(width * 0.234), int(height * 0.252)
right, bottom = int(width * 0.984), int(height * 0.960)
draw.rounded_rectangle((left, top, right, bottom), radius=18, outline=(183, 218, 207), width=3)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 15)
label = "Sistema EstoqueFácil"
bounds = draw.textbbox((0, 0), label, font=font)
label_width = bounds[2] - bounds[0]
draw.rectangle((left + 15, top - 14, left + label_width + 32, top + 9), fill="white")
draw.text((left + 23, top - 13), label, font=font, fill=(24, 68, 86))
image.save(target)
source.unlink()
print("DIAGRAMA_CASOS_DE_USO_OK", target, image.size)
