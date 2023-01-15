import numpy as np, pandas as pd, datashader as ds
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis
from datashader.utils import export_image
from numba import jit
from math import sin, cos, sqrt, fabs

@jit(nopython=True)
def Clifford(x, y, a, b, c, d, *o):
    return sin(a * y) + c * cos(a * x), \
           sin(b * x) + d * cos(b * y)

@jit(nopython=True)
def Chor1(x, y, a, b, c, d, *o):
    return sin(a * y)**2 + c * cos(a * x), \
           sin(b * x) + d * cos(b * y)**2

@jit(nopython=True)
def Chor2(x, y, a, b, c, d, *o):
    return sin(a * y) + c * cos(a * x), \
           d * cos(b * x) + sin(b * y)

@jit(nopython=True)
def De_Jong(x, y, a, b, c, d, *o):
    return sin(a * y) - cos(b * x), \
           sin(c * x) - cos(d * y)

@jit(nopython=True)
def Svensson(x, y, a, b, c, d, *o):
    return d * sin(a * x) - sin(b * y), \
           c * cos(a * x) + cos(b * y)

@jit(nopython=True)
def Bedhead(x, y, a, b, *o):
    return sin(x*y/b)*y + cos(a*x-y), \
           x + sin(y)/b

@jit(nopython=True)
def Fractal_Dream(x, y, a, b, c, d, *o):
    return sin(y*b)+c*sin(x*b), \
           sin(x*a)+d*sin(y*a)

@jit(nopython=True)
def Hopalong1(x, y, a, b, c, *o):
    return y - sqrt(fabs(b * x - c)) * np.sign(x), \
           a - x

@jit(nopython=True)
def G(x, mu):
    return mu * x + 2 * (1 - mu) * x**2 / (1.0 + x**2)

@jit(nopython=True)
def Gumowski_Mira(x, y, a, b, mu, *o):
    xn = y + a*(1 - b*y**2)*y  +  G(x, mu)
    yn = -x + G(xn, mu)
    return xn, yn

@jit(nopython=True)
def Symmetric_Icon(x, y, a, b, g, om, l, d, *o):
    zzbar = x*x + y*y
    p = a*zzbar + l
    zreal, zimag = x, y
    
    for i in range(1, d-1):
        za, zb = zreal * x - zimag * y, zimag * x + zreal * y
        zreal, zimag = za, zb
    
    zn = x*zreal - y*zimag
    p += b*zn
    
    return p*x + g*zreal - om*y, \
           p*y - g*zimag + om*x



n=int(1e8)

@jit(nopython=True)
def trajectory_coords(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = np.zeros(n), np.zeros(n)
    x[0], y[0] = x0, y0
    for i in np.arange(n-1):
        x[i+1], y[i+1] = fn(x[i], y[i], a, b, c, d, e, f)
    return x,y

def trajectory(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = trajectory_coords(fn, x0, y0, a, b, c, d, e, f, n)
    return pd.DataFrame(dict(x=x,y=y))


def dsplot(fn, attractors, n=n, cmap=viridis, label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    lab = ("{}, "*(len(attractors)-1)+" {}").format(*attractors) if label else None
    df  = trajectory(fn, *attractors, n=n)
    cvs = ds.Canvas(plot_width = 1600, plot_height = 1600)
    agg = cvs.points(df, 'x', 'y')
    img = tf.shade(agg, cmap=cmap, name=lab)
    return img

from colorcet import palette
palette["viridis"]=viridis
palette["inferno"]=inferno

import yaml
attractors = yaml.load(open("strange_attractors.yml","r"), Loader=yaml.FullLoader)

for i, attractor in enumerate(attractors):
    funcname, cmap, options = attractor[0], attractor[1], attractor[2:]
    func = eval(funcname)
    print(attractor, func)
    img = dsplot(func, options, cmap=palette[cmap][::-1])

    line_number = i+1
    export_image(img=img, filename=f'{line_number}_{funcname}', fmt=".png",  export_path=".",
                 background="#FFF4CA")

