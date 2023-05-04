# Natura2000Sites
Natura2000Sites.py an interactive program developed to automate the process of identifying Natura 2000 sites within a user defined distance (i.e. ‘ Zone of Influence’) of a project location within the Republic of Ireland. In simple terms this program takes a set of coordinates and a search distance provided by the user and produces the following outputs,
*	A text output stating how many SACs and SPAs occur within (even partly) within the search area,
*	Excel tables containing details of each Natura 2000 site, including a link to the relevant website for more information. 
*	A map showing where Natura 2000 sites occur in relation to the search area / project.
##  Setup and Installation
The script uses three external shapefiles to run the program. These can be found in the ‘data_files’ folder in the repository and are detailed the table below. All files are licenced under open creative commons licencing. External files are used in the program without modification from the source and so no alterations are required prior to running the script. 
| Name        | Description           | Source  |
| ------------- |:-------------:| -----:|
| Counties___Ungen_2019    | County Boundary files  | Tailte Éireann – National Mapping Division,   https://data-osi.opendata.arcgis.com/  |
| SAC_ITM_2023_02     | Special Areas of Conservation boundary files      |   National Parks and Wildlife Service,  https://www.npws.ie/maps-and-data |
| SPA_ITM_2021_10 | Special Protection Areas boundary files      |    National Parks and Wildlife Service,  https://www.npws.ie/maps-and-data |

The shapefiles used for the Natura 2000 Sites (‘SAC_ITM_2023_02’ and ‘SPA_ITM_2021_10’) are the most recent versions at the time of writing (May 2023). As the boundaries of these site can change over time the source for each should be checked prior to carrying out the program for the first time and newer versions used if required. The process for doing this is detailed in section 3.1 below.
The repository includes an environment file (‘environment.yml’) that can be used by your package management software to create an environment to run the programs code. The main dependencies used by the python script to run are:
  * python
  * geopandas
  * cartopy>=0.21
  * notebook
  * rasterio
  * pyepsg
  * folium

For the purposes of this guide, it is assumed that the user already has package manager and environment management system such as Conda, and an integrated development environment (IDE) such as PyCharm  already installed. It is also assumed that Git system software is also installed.  It is advised that GitHub  account is created and GitHub Desktop  installed to aid in the setup and installation stage.  

1. The first step of the setup is to fork the main branch of the repository to your GitHub account. This can be done through the repository link (https://github.com/O-2me/EGM722_Assessment) and selecting the fork tab and creating a new fork. 
2. Once the repository is forked it can then be cloned to your computer at a specific file pathway.  Open GitHub Desktop. Select ‘file’ and ‘Clone a repository’, the forked repository should be visible under ‘Your Repositories’. Select a local path where you want the repository saved to and click ‘Clone’. 
3. It is advised to use a graphical user interface (GUI) package management system, such as Anaconda Navigator , to launch applications and import modules set by the environment. Once installed open the Environments tab in Anaconda Navigator and select ‘Import’. Navigate to the cloned repository on your local system and select ‘environment.yml’. The name field will be automatically populated to ‘natura2000sites’. Click import and the environment will start setting up. Once complete return to the ‘Home’ tab and select the ‘natura2000sites’ environment in the dropdown box next to ‘Channels’ at the top of the screen.
4. To run the program, launch open your IDE (this example uses PyCharm). Select ‘file’ and ‘open’ and navigate to the location of the cloned repository.  Change the interpreter by selecting ‘Python 3.10’ in the lower right-hand corner of the screen. Select ‘Add New Interpreter’ and ‘Add Local Interpreter’. Then select ‘Conda Environment’ and ‘Use existing environment’ and select ‘natura2000sites’ from the drop down before pressing ‘OK’.
5. Once the setup is complete the interactive program is ready to run. Once initiated If the input files are projected to the wrong coordinate reference system (CRS), the user will first be informed of this and prompted to select the EPSG code to reproject the data to (program is designed to be carried out with EPSG 2175 – Irish Transverse Mercator (ITM)). The user will then be prompted to input a number of commands relating to the coordinates of your search point (i.e., project location) and search area (i.e. Zone of Influence) before producing the outputs
## Troubleshooting
### Incorrect external shapefile pathway
In the event that the external shapefiles area not saved to the locations specified in section 1, or if their files names have been altered the following error code will be presented;

_fiona.errors.DriverError: ‘your filepathway’: No such file or directory’_

Should this occur check that the files are in the correct location and named as specified in the program and re-run the script.
### Incorrect CRS Input
If the input shapefiles not all share a consistent CRS the user will be prompted to enter a new CRS to reproject the shapefiles to. The program will only accept integers as input and will re-prompt the user to enter a new CRS if any type other than an integer is added. However, if the user enters an integer that is not a recognised EPSG code the program will crash, and the following error code presented -

_pyproj.exceptions.CRSError: Invalid projection: EPSG:3: (Internal Proj Error: proj_create: crs not found)_

Should this occur, the user should check that the input they are using is a recognised EPSG code, for example 2157 (Irish Transverse Mercator, which this program was designed to use) and rerun the program with the correct EPSG input. 
### Incorrect CRS used for Search Point
When prompted for X and Y coordinates for the search point the user is limited to using float types. If the user enters the incorrect CRS coordinated (i.e. WGS84) the program will continue to run until all inputs are received and then crash producing the following error code;

_ValueError: Axis limits cannot be NaN or Inf_

Should this occur make sure the input coordinates are set to ITM and rerun the program.
### Other Issues
If you have any other issues running the program not listed above, please create an issue post in the GitHub repository
