# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 23:40:20 2021

@author: Nazia
"""

import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import arcpy


# File and folder paths
arcpy.env.workspace= r"C:\Users\Nazia\research_ntl"
dirpath = r"C:\Users\Nazia\research_ntl\Mosaiced data\tiff_mar"
out_fp = os.path.join(dirpath, "VNP46A2.A2021001.h08v05.001.2021103041035.tif")

# Make a search criteria to select the DEM files
search_criteria = "*A2021001*.tif"
q = os.path.join(dirpath, search_criteria)
print(q)

# glob function can be used to list files from a directory with specific criteria
ntl_fps = glob.glob(q)

# Files that were found:
ntl_fps

# List for the source files
src_files_to_mosaic = []

# Iterate over raster files and add them to source -list in 'read mode'
for fp in ntl_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

src_files_to_mosaic

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4))
show(src_files_to_mosaic[0], ax=ax1)
show(src_files_to_mosaic[1], ax=ax2)

# Merge function returns a single mosaic array and the transformation info
mosaic, out_trans = merge(src_files_to_mosaic)

# Plot the result
show(mosaic, cmap='terrain')

# Copy the metadata
out_meta = src.meta.copy()  

# Update the metadata
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "crs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
                 }
                )
# Write the mosaic raster to disk
with rasterio.open(out_fp, "w", **out_meta) as dest:
    dest.write(mosaic)


