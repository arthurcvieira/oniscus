# Generates the original Oniscus wallpaper (CC BY-SA 4.0).
import sys, math
from PIL import Image, ImageDraw, ImageFilter
W,H=1920,1080
img=Image.new('RGB',(W,H))
px=img.load()
def blob(x,y,cx,cy,rx,ry):
    d=((x-cx)/rx)**2+((y-cy)/ry)**2
    return max(0.0,1-d)
for y in range(H):
    t=y/H
    # Charcoal background (#161A1F at the top, #0D0F12 at the bottom)
    base=(22-9*t, 26-11*t, 31-13*t)
    for x in range(W):
        r,g,b=base
        for (cx,cy,rx,ry,col,a) in ((0.25*W,0.7*H,1080,456,(78,53,39),0.55),(0.7*W,0.42*H,984,624,(201,148,18),0.20)):
            w=blob(x,y,cx,cy,rx,ry)*a
            r=r+(col[0]-r)*w; g=g+(col[1]-g)*w; b=b+(col[2]-b)*w
        px[x,y]=(int(r),int(g),int(b))
def curve(off,width,col,blur):
    layer=Image.new('RGBA',(W,H),col[:3]+(0,))
    d=ImageDraw.Draw(layer)
    pts=[]
    for i in range(0,801):
        t=i/800; x=-60+t*(W+120)
        y=0.74*H+off-0.22*H*t+0.10*H*math.sin(t*math.pi*2.2)
        pts.append((x,y))
    d.line(pts,fill=col,width=width)
    return layer.filter(ImageFilter.GaussianBlur(blur))
img=img.convert('RGBA')
for args in ((40,60,(247,201,72,34),14),(0,3,(255,229,143,90),1.2),(80,2,(255,229,143,45),1.0)):
    img=Image.alpha_composite(img,curve(*args))
img=img.convert('RGB')
img.save(sys.argv[1],quality=92)
