# import required modules
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
from shapely.geometry import Point, LineString
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

    ax.text(sbx, sby-1000, '20 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-10000, sby-1000, '10 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-20500, sby-1000, '0 km', transform=ax.projection, fontsize=8)

# ---------------------Import external shapefiles as GeoPandas Geodataframes----------------------------------------
outline = gpd.read_file(os.path.abspath('data_files/Counties___Ungen_2019.shp'))
sac = gpd.read_file(os.path.abspath('data_files/SAC_ITM_2023_02.shp'))
spa = gpd.read_file(os.path.abspath('data_files/SPA_ITM_2021_10.shp'))
#---------------------------------Check CRS Consistency--------------------------------------------------------------
#sac = sac.to_crs(epsg=32639) #debug

#Check EPSG codes of the input data and state if projections are consistent
if outline.crs == sac.crs == spa.crs:
    print ('All features are projected to projection {}'.format(outline.crs))

else:
    print ('Input data will be reprojected as 1 or more features have inconsistent projections')
    epsg_code = int((input('Please enter the EPSG code used to reproject input data: '))) #ITM = 2157
    outline = outline.to_crs(epsg=epsg_code)
    sac = sac.to_crs(epsg=epsg_code)
    spa = spa.to_crs(epsg=epsg_code)
    print('Outline projection - {}\nSAC projection - {}\nSPA projection - {}'
          .format(outline.crs, sac.crs, spa.crs))

#------------------------------User input coordinates and search features-------------------------------------------

#while True:
print ("Please enter ITM X coordinate (easting) of search point.\nCoordinates must be entered in a number format such as 123456.78")
xin = 570748.007 #float(input()) commented out for testing
#    if xin != float or int:
 #       print('Coordinates must be entered in a number format such as 123456.78')
  #      continue
   # else:
    #    break

#while True:
print ("Please enter ITM Y coordinate (northing) of search point.\nCoordinates must be entered in a number format such as 123456.78")
yin = 621905.056 # commented out for testing float(input())
#    if yin != float or int:
#        print('Coordinates must be entered in a number format such as 123456.78')
#        continue
#    else:
#        break
#xin = float(xin) #transform input str to float for plotting
#while xin != float or int:
    #print ('Coordinates must be entered in a number format such as 123456.78')

#yin = input('Enter ITM Y coordinate (northing) of search point;')
#while yin != float or int:
    #print ('Coordinates must be entered in a number format such as 123456.78')
userinput = Point(xin, yin)

userbuffer = userinput.buffer(15000, resolution=50) # Buffer of 15 km around the search point to select Natura 2000 Sites.
#userbuffer = userbuffer.to_crs(epsg=2157)

#-------------------------------Selecting intersecting Natura 2000 sites with user buffer---------------------------#
#print(userbuffer.intersects(sac))
#print(userbuffer.intersects(spa))
#_______________________________Creating map________________________________________________________________________
# create figure of size 10x10
myFig = plt.figure(figsize=(10, 10))

# create a coordinate reference system.
myCRS = ccrs.UTM(29)  # Irish Transverse Mercator (ITM) is used in RoI.
# 2157 is the epsg code for ITM so passed to ccrs.epsg()

# create an axis object in the figure, using myCRS where data is plotted.
ax = plt.axes(projection=myCRS)

# add the outline of RoI using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='grey', facecolor='w')
ax.add_feature(outline_feature)

# using the boundary of the shapefile features, zoom the map to our area of interest
xmin, ymin, xmax, ymax = userbuffer.bounds
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

userpoint_handle = ax.plot(xin, yin, 'o', color='r', ms=6,)

#userbuffer_handle = ax.plot(userbuffer, color='none', edgecolor = 'k')

userbuffer_feat = ShapelyFeature(userbuffer,  # first argument is the geometry
                            myCRS,          # second argument is the CRS
                            edgecolor='k',  # set the edgecolor to be black
                            facecolor='none',  # set the facecolor to be white
                            linewidth=1)    # set the outline width to be 1 pt

ax.add_feature(userbuffer_feat)  # add the feature to the map

# Symbologies for handles in legend
sac_handle = generate_handles(['SAC'], ['g'])
spa_handle = generate_handles(['SPA'], ['b'])
userbuffer_handle = generate_handles(['Search Area'], ['w'])

# ax.legend() takes list of handles and list of labels corresponding to the features of interest
# and adds them to  the legend
handles = sac_handle + spa_handle + userpoint_handle + userbuffer_handle
labels = ['SAC', 'SPA', 'Search Point', 'Seach Area']
leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                fontsize=10, loc='upper left', frameon=True, framealpha=1)

# Gridlines - I'll probably remove
#gridlines = ax.gridlines(draw_labels=True,  # draw  labels for the grid lines
#                         xlocs=[-9.5, -9, -8.5, -8, -7.5, -7],  # add longitude lines at 0.5 deg intervals
#                         ylocs=[54, 54.5, 55, 55.5])  # add latitude lines at 0.5 deg intervals
#gridlines.left_labels = False  # turn off the left-side labels
#gridlines.bottom_labels = False  # turn off the bottom labels

# add the scale bar to the axis
scale_bar(ax)

# save the figure as map.png, cropped to the axis (bbox_inches='tight'), and a dpi of 300
myFig.savefig('map.png', bbox_inches='tight', dpi=300)
