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

cmaps = dict(bgyw = palette["bgyw"],
             inferno = palette["inferno"],
             fire = palette["fire"][::-1],
             fire2 = palette["fire"],
             bmy = palette["bmy"],
             kbc = palette["kbc"],
             )


import glob
import yaml
import os
directory = 'data'

pixelsize = 1000

def dsplot(df, cmap=inferno, label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    lab = os.path.basename(df.name) if label else None
    cvs = ds.Canvas(plot_width = pixelsize, plot_height = pixelsize)
    agg = cvs.points(df, 'x', 'y')
    img = tf.shade(agg, cmap=cmap, name=lab)
    return img



fpath = os.path.join(directory, "*.nc")
filelist = sorted(glob.glob(fpath))
attractors = yaml.load(open("strange_attractors.yml","r"), Loader=yaml.FullLoader)

for attractor, file in zip(attractors, natsorted(filelist)):
    print(file)

    df = xr.open_dataset(file).to_dataframe()
    df.name = os.path.basename(file)
    aname = df.name.replace('.nc', '')

    for cname, background in attractor["pairs"]:
        print(aname, cname, background)
        img = dsplot(df, cmap=cmaps[cname])

        export_image(img=img, filename=f"figures/{aname}_{cname}_{background}", fmt=".png",  export_path=".",
                     background=background)


