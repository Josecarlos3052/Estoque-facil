"""Renderiza o diagrama de casos de uso em duas colunas, com ator e fronteira do sistema."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parent
OUT = DOCS / "casos_de_uso.png"
WIDTH, HEIGHT = 1000, 600
BASE_FONT = Path("/usr/share/fonts/truetype/dejavu")
title_font = ImageFont.truetype(str(BASE_FONT / "DejaVuSans-Bold.ttf"), 24)
label_font = ImageFont.truetype(str(BASE_FONT / "DejaVuSans-Bold.ttf"), 18)
text_font = ImageFont.truetype(str(BASE_FONT / "DejaVuSans.ttf"), 16)
actor_font = ImageFont.truetype(str(BASE_FONT / "DejaVuSans-Bold.ttf"), 16)

navy = (24, 68, 86)
teal = (139, 216, 194)
boundary = (183, 218, 207)
edge = (120, 148, 163)

image = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(image)

title = "Diagrama de Casos de Uso | EstoqueFácil 1.1"
title_box = draw.textbbox((0, 0), title, font=title_font)
draw.text(((WIDTH - (title_box[2] - title_box[0])) / 2, 22), title, font=title_font, fill=navy)

# Fronteira do sistema: o ator permanece do lado externo.
draw.rounded_rectangle((285, 112, 970, 560), radius=22, outline=boundary, width=4)
system_label = "Sistema EstoqueFácil"
label_box = draw.textbbox((0, 0), system_label, font=label_font)
draw.rectangle((310, 98, 322 + label_box[2] - label_box[0], 128), fill="white")
draw.text((320, 99), system_label, font=label_font, fill=navy)

left_cases = [
    ("Cadastrar produto", 170),
    ("Editar produto", 250),
    ("Registrar entrada", 330),
    ("Registrar saída", 410),
    ("Buscar produtos", 490),
]
right_cases = [
    ("Filtrar estoque baixo", 170),
    ("Consultar indicadores", 250),
    ("Exportar CSV", 330),
    ("Excluir produto", 410),
    ("Consultar histórico\n(pesquisar e filtrar)", 490),
]

# Ator UML.
draw.ellipse((83, 205, 117, 239), outline=navy, width=3)
draw.line((100, 239, 100, 302), fill=navy, width=3)
draw.line((67, 263, 133, 263), fill=navy, width=3)
draw.line((100, 302, 72, 340), fill=navy, width=3)
draw.line((100, 302, 128, 340), fill=navy, width=3)
draw.multiline_text((43, 352), "OPERADOR\nDA LOJA", font=actor_font, fill=navy, align="center", spacing=2)

# Associações desenhadas antes das elipses para que não atravessem os rótulos.
anchor = (145, 263)
for _, center_y in left_cases:
    draw.line((anchor, (320, center_y)), fill=edge, width=2)
for _, center_y in right_cases:
    draw.line((anchor, (650, center_y)), fill=edge, width=2)

def draw_use_case(label, center_x, center_y):
    x1, x2 = center_x - 130, center_x + 130
    y1, y2 = center_y - 26, center_y + 26
    draw.ellipse((x1, y1, x2, y2), fill="white", outline=teal, width=3)
    lines = label.split("\n")
    measured = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=text_font)
        measured.append((line, box[2] - box[0], box[3] - box[1]))
    total_height = sum(item[2] for item in measured) + (len(measured) - 1) * 2
    y = center_y - total_height / 2
    for line, text_width, text_height in measured:
        draw.text((center_x - text_width / 2, y), line, font=text_font, fill=(25, 43, 62))
        y += text_height + 2

for label, center_y in left_cases:
    draw_use_case(label, 450, center_y)
for label, center_y in right_cases:
    draw_use_case(label, 780, center_y)

image.save(OUT)
print("DIAGRAMA_CASOS_DE_USO_OK", OUT, image.size)
