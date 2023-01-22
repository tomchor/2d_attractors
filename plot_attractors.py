import numpy as np, pandas as pd
import xarray as xr
from natsort import natsorted
import datashader as ds
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis
from datashader.utils import export_image
from colorcet import palette
palette["viridis"]=viridis
palette["inferno"]=inferno
cmap=palette["fire"][::-1]

import glob
import yaml
import os
directory = 'data'

pixelsize = 2000

def dsplot(df, cmap=viridis, label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    lab = os.path.basename(df.name) if label else None
    cvs = ds.Canvas(plot_width = pixelsize, plot_height = pixelsize)
    agg = cvs.points(df, 'x', 'y')
    img = tf.shade(agg, cmap=cmap, name=lab)
    return img



fpath = os.path.join(directory, "*.nc")
filelist = sorted(glob.glob(fpath))[6:]
attractors = yaml.load(open("strange_attractors.yml","r"), Loader=yaml.FullLoader)
for i, file in enumerate(natsorted(filelist)):
    print(file)

    df = xr.open_dataset(file).to_dataframe()
    df.name = os.path.basename(file)
    img = dsplot(df, cmap=inferno)

    export_image(img=img, filename=f"figures/{df.name}", fmt=".png",  export_path=".",
                 background="black")
                 #background="#FFF4CA")



pause
for i, attractor in enumerate(attractors):
    funcname, cmap, options = attractor[0], attractor[1], attractor[2:]
    func = eval(funcname)
    print(attractor, func)
    img = dsplot(func, options, cmap=palette[cmap][::-1])

    line_number = i+1
    export_image(img=img, filename=f'{line_number}_{funcname}', fmt=".png",  export_path=".",
                 background="#FFF4CA")

