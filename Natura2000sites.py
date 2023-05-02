# import required modules
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
from shapely.geometry import Point, Polygon, LineString
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import openpyxl
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
xin = 533835.919 #float(input()) commented out for testing
#    if xin != float or int:
 #       print('Coordinates must be entered in a number format such as 123456.78')
  #      continue
   # else:
    #    break

#while True:
print ("Please enter ITM Y coordinate (northing) of search point.\nCoordinates must be entered in a number format such as 123456.78")
yin = 680764.228 #float(input()) commented out for testing float(input())
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

print ('Please enter the search distance (km)')
ZoI = 15 #commented out for testing float(input())
userbuffer = userinput.buffer((ZoI * 1000), resolution=50) # Buffer around the search point to select Natura 2000 Sites.

#-------------------------------------Fuctions to help mapping---------------------------------------------------------
# Function to generate matplotlib handles for each feature.
# Used to create a legend of the input map features.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20 km in the lower right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
# code modified further to adjust scalebar size based scale of userbuffer.
def scale_bar(ax, location=(0.92, 0.05)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    if ZoI >= 10:
        ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
        ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
        ax.plot([sbx- 10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

        ax.text(sbx, sby-1000, '20 km', transform=ax.projection, fontsize=8)
        ax.text(sbx-10000, sby-1000, '10 km', transform=ax.projection, fontsize=8)
        ax.text(sbx-20500, sby-1000, '0 km', transform=ax.projection, fontsize=8)

    elif ZoI >= 5:
        ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
        ax.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
        ax.plot([sbx - 5000, sbx - 10000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

        ax.text(sbx, sby - 500, '10 km', transform=ax.projection, fontsize=8)
        ax.text(sbx - 5000, sby - 500, '5 km', transform=ax.projection, fontsize=8)
        ax.text(sbx - 10250, sby - 500, '0 km', transform=ax.projection, fontsize=8)

    else:
        ax.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
        ax.plot([sbx, sbx - 2500], [sby, sby], color='k', linewidth=6, transform=ax.projection)
        ax.plot([sbx - 2500, sbx - 5000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

        ax.text(sbx, sby - 250, '5 km', transform=ax.projection, fontsize=8)
        ax.text(sbx - 2500, sby - 250, '2.5 km', transform=ax.projection, fontsize=8)
        ax.text(sbx - 5125, sby - 250, '0 km', transform=ax.projection, fontsize=8)
#_______________________________Creating map________________________________________________________________________
# create figure of size 10x10
myFig = plt.figure(figsize=(10, 10))

# create a coordinate reference system.
myCRS = ccrs.epsg(2157)  # Irish Transverse Mercator (ITM) is used in RoI.
# 2157 is the epsg code for ITM so passed to ccrs.epsg()

# create an axis object in the figure, using myCRS where data is plotted.
ax = plt.axes(projection=myCRS)

# add the outline of RoI using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='grey', facecolor='w')
ax.add_feature(outline_feature)

# using the boundary of the userbuffer, zoom the map to our area of interest
xmin, ymin, xmax, ymax = userbuffer.bounds
# xmin, xmax, ymin, ymax, coordinates are reordered here and defined depends on userbuffer scale
if ZoI >= 10:
    ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=myCRS)
elif ZoI >= 5:
    ax.set_extent([xmin-1000, xmax+1000, ymin-1000, ymax+1000], crs=myCRS)
else:
    ax.set_extent([xmin - 500, xmax + 500, ymin - 500, ymax + 500], crs=myCRS)

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

# add the scale bar to the axis
scale_bar(ax)

# export figure as map
myFig.savefig('Natura2000map.png', bbox_inches='tight', dpi=300)

#-------------------------------Selecting Natura 2000 sites with user buffer---------------------------#

sac_in = sac.loc[sac.intersects(userbuffer)] # new variable containing sacs within userbuffer geometry
print ('Natura 2000 Sites within Search Area -')
print ('Number of Special Areas of Conservation: {}' .format(len(sac_in.index)))
spa_in = spa.loc[spa.intersects(userbuffer)] # new variable containing spas within userbuffer geometry
print ('Number of Special Protection Areas: {}' .format(len(spa_in.index)))

#-------------------------------Exporting results table to file---------------------------------------#

#creating file pathways for excel exports
sac_expath = 'C:/MSc_Remote_Sensing_&_GIS/EGM722_Programming_for_GIS_and_RS/git/EGM722_Assessment/SAC_within.xlsx'
spa_expath = 'C:/MSc_Remote_Sensing_&_GIS/EGM722_Programming_for_GIS_and_RS/git/EGM722_Assessment/SPA_within.xlsx'

#export results to excel
sac_in.to_excel(sac_expath)
spa_in.to_excel(spa_expath)

print('Results and mapping exported to folder')