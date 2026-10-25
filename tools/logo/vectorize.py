import sys
import numpy as np
from PIL import Image, ImageFilter
import potrace

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(int)
red = (a[..., 0] > 180) & (a[..., 1] < 140) & (a[..., 2] < 140)
ys, xs = np.where(red)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
print('bbox', x0, y0, x1, y1, 'size', x1 - x0, y1 - y0)
crop = im.crop((x0, y0, x1, y1))
E = 3  # prolonge les bords pour que les traits sortent proprement du carré
ext = Image.fromarray(np.pad(np.asarray(crop), ((E, E), (E, E), (0, 0)), mode='edge'))
S = 24
big = ext.resize((ext.width * S, ext.height * S), Image.BICUBIC).filter(ImageFilter.GaussianBlur(S * 0.6))
g = np.asarray(big.convert('RGB')).astype(int)[..., 1]   # canal vert : blanc ~255, rouge ~64
mask = g > 160   # potracer trace les zones False -> on obtient les zones rouges
# Pad pour fermer les formes qui touchent le bord du carré
pad = np.pad(mask, 2, constant_values=False)
bmp = potrace.Bitmap(pad)
path = bmp.trace(turdsize=200, alphamax=1.3, opticurve=True, opttolerance=0.6)
W, H = crop.width, crop.height
k = 1.0 / S
def P(pt):
    return f"{(pt.x - 2) * k - E:.3f} {(pt.y - 2) * k - E:.3f}"
d = []
for curve in path:
    d.append('M' + P(curve.start_point))
    for seg in curve.segments:
        if seg.is_corner:
            d.append('L' + P(seg.c) + 'L' + P(seg.end_point))
        else:
            d.append('C' + P(seg.c1) + ' ' + P(seg.c2) + ' ' + P(seg.end_point))
    d.append('Z')
col = '#EF4035'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*10}" height="{H*10}">
  <defs><clipPath id="sq"><rect width="{W}" height="{H}"/></clipPath></defs>
  <rect width="{W}" height="{H}" fill="#fff"/>
  <path clip-path="url(#sq)" fill="{col}" fill-rule="evenodd" d="{''.join(d)}"/>
</svg>
'''
open(out, 'w').write(svg)
print('paths', len(path), 'chars', len(svg))
