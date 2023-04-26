# import required modules
import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# Function to generate matplotlib handles for each feature of interest.
# This is used to create a legend of the input map features.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

#Scalebar may need to be modified once scalled to 15km
# create a scale bar of length 20 km in the upper right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
def scale_bar(ax, location=(0.92, 0.05)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby-10000, '20 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-12500, sby-10000, '10 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-24500, sby-10000, '0 km', transform=ax.projection, fontsize=8)

# import external datasets
# load the Republic of Ireland boundary as an outline
outline = gpd.read_file(os.path.abspath('data_files/Counties___Ungen_2019.shp'))

# load Natura 2000 Site boundaries
sac = gpd.read_file(os.path.abspath('data_files/SAC_ITM_2023_02.shp'))
spa = gpd.read_file(os.path.abspath('data_files/SPA_ITM_2021_10.shp'))

#_______________________________Creating map________________________________________________________________________
# create figure of size 10x10
myFig = plt.figure(figsize=(10, 10))

# create a Universal Transverse Mercator reference system to transform data.
myCRS = ccrs.UTM(29)  # RoI is in UTM Zone 29, so we pass 29 to ccrs.UTM()

# create an axis object in the figure, using myCRS where data is plotted.
ax = plt.axes(projection=myCRS)

# add the outline of RoI using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')


ax.add_feature(outline_feature)  # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
xmin, ymin, xmax, ymax = outline.total_bounds
# because total_bounds gives output as xmin, ymin, xmax, ymax, but set_extent takes xmin,
# xmax, ymin, ymax, coordinates are reordered here.
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=myCRS)

# Setting the symbologies for the features of interest
sac_feat = ShapelyFeature(sac['geometry'],  # first argument is the geometry
                            myCRS,          # second argument is the CRS
                            edgecolor='g',  # set the edgecolor to be green
                            facecolor='g',  # set the facecolor to be green
                            linewidth=1,    # set the outline width to be 1 pt
                            alpha= 0.5)    # Transparency set to 50%
ax.add_feature(sac_feat)  # add the  feature to the map

spa_feat = ShapelyFeature(spa['geometry'],  # first argument is the geometry
                            myCRS,          # second argument is the CRS
                            edgecolor='b',  # set the edgecolor to be blue
                            facecolor='b',  # set the facecolor to be blue
                            linewidth=1,    # set the outline width to be 1 pt
                            alpha= 0.5)    # Transparency set to 50%
ax.add_feature(spa_feat)  # add the feature to the map

# Symbologies for handles in legend
sac_handle = generate_handles(['SAC'], ['g'])
spa_handle = generate_handles(['SPA'], ['b'])

# ax.legend() takes list of handles and list of labels corresponding to the features of interest
# and adds them to  the legend
handles = sac_handle + spa_handle
labels = ['SAC', 'SPA']
leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                fontsize=10, loc='upper left', frameon=True, framealpha=1)

# Gridlines - I'll probably remove
gridlines = ax.gridlines(draw_labels=True,  # draw  labels for the grid lines
                         xlocs=[-9.5, -9, -8.5, -8, -7.5, -7],  # add longitude lines at 0.5 deg intervals
                         ylocs=[54, 54.5, 55, 55.5])  # add latitude lines at 0.5 deg intervals
gridlines.left_labels = False  # turn off the left-side labels
gridlines.bottom_labels = False  # turn off the bottom labels

# add the scale bar to the axis
scale_bar(ax)

# save the figure as map.png, cropped to the axis (bbox_inches='tight'), and a dpi of 300
myFig.savefig('map.png', bbox_inches='tight', dpi=300)
