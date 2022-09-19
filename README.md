# index_calculator

Calculate different indices of Sentinel-2 raster images and, if desired, cut them to a specific region of interest (roi, recommended since they are clipped beforehand and can therefore minimize execution times!). <br/>
Following indices are available so far (write an <a href="https://github.com/GrHalbgott/index-calculator/issues">issue</a> if you want some special index to be implemented):
- Atmospherically Resistant Vegetation Index (ARVI)
- Green Chlorophyll Vegetation Index (GCI)
- Green Normalized Difference Vegetation Index (GNDVI)
- Normalized Difference Build-up Index (NDBI)
- Normalized Difference Moisture Index (NDMI)
- Normalized Difference Red-Edge Vegetation Index (NDRE)
- Normalized Difference Snow Index (NDSI)
- Normalized Difference Vegetation Index (NDVI)
- Normalized Difference Water Index (NDWI)
- Red-Edge Inflection Point (REIP)
- Soil-Adjusted Vegetation Index (SAVI)
- Structure Intensive Pigment Vegetation Index (SIPI)

### Output options

The following outputs can be automatically generated and aved to `./results/`:
- Plot the resulting array with the default ranges (as found in literature)
- Save the plot as figure
- Save the resulting array as txt-file
- Export the resulting array as GIS-ready tif-file (raster)
- Generate a histogram and include descriptive statistics (min, max, mean, std.dev)

As before, if there is a type of output which you would want to get, please write an <a href="https://github.com/GrHalbgott/index-calculator/issues">issue</a>.

## Data

Exemplary multispectral raster data can be found <a href="https://heibox.uni-heidelberg.de/d/5a5c773e48cf410a9ed6/">here</a> and should be put into `./data/raster/`.<br/>
The region of interest must be manually added as a shapefile into `./data/shapes/`. <br/>
An example roi to test the program can be found in the HeiBOX folder mentioned above as well.

<details>
   <summary><b>How to acquire raster (Sentinel-2) data</b></summary>
<br/>

1. Navigate to <a href="https://scihub.copernicus.eu/dhus/#/self-registration">Copernicus Open Access Hub by ESA registration form</a> and set up an account
2. Log in on <a href="https://scihub.copernicus.eu/dhus/#/home">Copernicus Open Access Hub</a>. Without logging in you cannot download the required data
3. Specify the search area in the map with right-click (move map with left-click and zoom in with mouse wheel)
4. Click on the three stripes left of the search box to open the advanced search (upper left corner of screen)
5. Select Sentinel-2 and put following statement in the box for the cloud cover: `[0 TO 2]`
6. If you want to search for data in a specific time period, put the required dates in "sensing period"
7. Click on the search button (upper right of search box) and wait until the results are displayed
8. Search for an image with full extent (no black parts) and minimal cloud cover
9. Hover over the entry and click on the eye icon ("View product details") which appears along with other icons on the lower right side of the entry
10. Check in the quick look window if the data seems suitable
<br/><br/>
    > If the images you are looking for are offline, take a look at <a href="https://github.com/GrHalbgott/Plants-vs-CO2/wiki/Troubleshooting">troubleshooting - Sentinel-2 data offline</a> for some help on that problem.
11. In the Inspector, click on the download-arrow in the lower right corner to download the complete ZIP-file
12. When downloaded, extract the ZIP-file and put the new folder in the `./data/raster/` folder
</details>
<br/>

## Getting Started

To run the program every machine having at least Python 3.9 installed is suitable. Your Python environment should additionally include following libraries:
- numpy
- matplotlib
- fiona
- rasterio

The rest should be included in the python installation. If you are using Linux or Mac, you should check the relative paths beforehand.

### Installing

Create your virtual python environment and clone the repository. Open the terminal and navigate to the cloned/downloaded folder `index-calculator`. If you don't have the required packages installed already, call this first:
```
$ pip install -r ./requirements.txt
```
You should then be ready to execute the program.

### Usage

If ready, call the program without any arguments to access the help within the terminal with information on how to use the arguments:
```
$ python src/main.py

usage: main.py [-h] -i Index name [-c Clip] [-r Resolution] [-ov Optional value] [-tif Save raster] [-gp Generate plot] [-sp Save plot] [-txt Save as txt] [-stat Statistics]

Calculate an index with Sentinel-2 satellite imagery. You can use the following options to adapt the calculation to your needs. Have fun!

required arguments:
  -i Index name       String | Choose which index gets calculated. Check the README for a list of possible indices.

optional arguments:
  -c Clip             String | Clip raster to shapefile with shapefile. Use the name and file-type only (like roi.shp). Default value: None
  -r Resolution       Integer | The indices can be calculated with different resolutions (10, 20, 60 (meters)). Default value: highest resolution possible
  -ov Optional value  Integer | Some indices need additional values like the L-value in SAVI. Default value: as in literature
  -tif Save raster    Boolean | Do you want to export the results/ndarray as tif-file locally to ./results/? Use true/false. Default: false
  -gp Generate plot   Boolean | Do you want to generate a plot? Use true/false. Default: true
  -sp Save plot       Boolean | Do you want to save the plot locally to ./results/? Use true/false. Default: false
  -txt Save as txt    Boolean | Do you want to save the results/ndarray as txt-file locally to ./results/? Use true/false. Default: false
  -stat Statistics    Boolean | Do you want to generate statistics (histogram & descriptive) for the results and save them locally to ./results/? Use true/false. Default: false

Exiting program, call again to run. Use -h or --help to show the help dialog.

```

## Cleaning up

If finished with multiple analyses, you can empty `./results/` and delete temporary used files from `./data/.` <br/>
**Make sure to save any results you want to keep to another location BEFORE executing the following command!** <br/>

To do a cleanup, call:
```
$ python src/cleanup.py
```

---

### *Footnote:*

If you have any questions, wishes or ideas, feel free to ask me in the <a href="https://github.com/GrHalbgott/index-calculator/issues">issues section</a>, I'm looking forward to it. Have fun!
