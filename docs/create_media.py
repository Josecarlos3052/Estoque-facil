from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]; docs=root/'docs'; dest=Path('/mnt/data')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fontb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
# Sequência UML funcional da operação de saída.
im=Image.new('RGB',(1750,925),'white'); d=ImageDraw.Draw(im)
d.text((70,42),'Diagrama de sequência — registrar saída',font=ImageFont.truetype(fontb,36),fill='#1b3a46')
heads=['Operador','Interface / app.js','Regras / stock.js','localStorage']
xs=[210,645,1095,1530]
for x,h in zip(xs,heads):
 d.rounded_rectangle((x-150,112,x+150,172),radius=12,fill='#e7f7f2',outline='#5cc1a6',width=3)
 box=d.textbbox((0,0),h,font=ImageFont.truetype(fontb,20)); d.text((x-(box[2]-box[0])/2,131),h,font=ImageFont.truetype(fontb,20),fill='#285463')
 d.line((x,180,x,840),fill='#8fadb3',width=3)
 for y in range(185,840,20):d.line((x,y,x,y+10),fill='white',width=4)
rows=[(218,0,1,'1. Clica em Movimentar'),(296,1,2,'2. moveStock(id, SAÍDA, qtd.)'),(380,2,1,'3. Verifica saldo e atualiza'),(464,1,3,'4. Salva produtos + histórico'),(548,3,1,'5. Confirma gravação'),(632,1,0,'6. Exibe novo saldo / histórico')]
for y,src,dst,label in rows:
 x1,x2=xs[src],xs[dst];d.line((x1,y,x2,y),fill='#1b9e87',width=4)
 if x2>x1: d.polygon([(x2,y),(x2-16,y-9),(x2-16,y+9)],fill='#1b9e87')
 else:d.polygon([(x2,y),(x2+16,y-9),(x2+16,y+9)],fill='#1b9e87')
 bx=min(x1,x2)+10
 d.rounded_rectangle((bx,y-38,bx+min(370,abs(x2-x1)-18),y-8),radius=6,fill='#fff',outline='#dfe9ea',width=1)
 d.text((bx+7,y-33),label,font=ImageFont.truetype(font,15),fill='#2b4855')
d.rounded_rectangle((85,760,1645,825),radius=10,fill='#fff4e4',outline='#f1cf9b',width=2)
d.text((110,781),'Fluxo alternativo: se a quantidade exceder o saldo, a operação é recusada e nada é gravado.',font=ImageFont.truetype(font,18),fill='#885829')
im.save(docs/'sequencia_saida.png')
# Vídeo de prévia montado de estados reais executados no navegador (sem áudio).
slides=[
('tela_01_painel.png','01 · Visão geral','Indicadores de produtos, unidades e estoque baixo',8),
('tela_02_cadastro.png','02 · Cadastrar produto','Cadastro com SKU, categoria, preço e estoque mínimo',8),
('tela_03_produto_cadastrado.png','03 · Cadastro concluído','Novo produto aparece imediatamente na tabela',7),
('tela_04_movimentacao.png','04 · Entrada de estoque','Registro da quantidade a acrescentar ao saldo',8),
('tela_05_movimentado.png','05 · Movimentação salva','Total de unidades atualizado e histórico registrado',8),
('tela_06_estoque_baixo.png','06 · Alerta de reposição','Filtro destaca produtos abaixo do mínimo',8),
('tela_07_busca.png','07 · Busca de produtos','Localização rápida pelo nome do item',8),
]
seq=[]
for idx,(filename,title,subtitle,duration) in enumerate(slides,1):
 screen=Image.open(docs/filename).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
 overlay=Image.new('RGBA',(1280,720)); od=ImageDraw.Draw(overlay)
 od.rectangle((0,595,1280,720),fill=(9,30,45,237))
 od.rounded_rectangle((28,615,34,695),radius=2,fill='#3fd1b1')
 od.text((55,606),title,font=ImageFont.truetype(fontb,27),fill='#fff')
 od.text((55,650),subtitle,font=ImageFont.truetype(font,17),fill='#d0e6e7')
 od.text((1095,660),'ESTOQUEFÁCIL',font=ImageFont.truetype(fontb,13),fill='#71dfc9')
 screen=Image.alpha_composite(screen.convert('RGBA'),overlay).convert('RGB')
 p=dest/f'video_slide_{idx:02d}.png';screen.save(p,optimize=True)
 seq.append((p,duration))
manifest=dest/'demo_segments.txt'
with manifest.open('w') as f:
 for p,duration in seq:f.write(f"file '{p}'\nduration {duration}\n")
 f.write(f"file '{seq[-1][0]}'\n")
output=dest/'Demo_EstoqueFacil_55s.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-vf','fps=15,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','22','-movflags','+faststart','-t','55',str(output)],check=True)
print(output,output.stat().st_size)
