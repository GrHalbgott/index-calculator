# index_calculator

Calculate different indices of Sentinel-2 raster images and, if desired, cut them to a specific region of interest (roi, recommended for they are cut beforehand and can therefor minimize execution times!). <br/>
Following indices are available so far (write an <a href="https://github.com/GrHalbgott/index-calculator/issues">issue</a> if you want some special index to be implemented):
- Normalized Difference Vegetation Index (NDVI)
- Normalized Difference Moisture Index (NDMI)
- Red-Edge Inflection Point (REIP)
- RGB-Composite (not an index and not true color so far)

## Data


Exemplary multispectral raster data can be found <a href="https://heibox.uni-heidelberg.de/d/5a5c773e48cf410a9ed6/">here</a> and should be put into `./data/raster/`. It should be in the same CRS as the raster images and <br/>
The region of interest must be manually added as shapefile into `./data/shapes/`.

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
9.  Hover over the entry and click on the eye icon ("View product details") which appears along with other icons on the lower right side of the entry
10. Check in the quick look window if the data seems suitable
<br/><br/>
    > If the images you are looking for are offline, take a look at <a href="https://github.com/GrHalbgott/Plants-vs-CO2/wiki/Troubleshooting">troubleshooting - Sentinel-2 data offline</a> for some help on that problem.
11. In the Inspector, navigate to `GRANULE/*Name of data*/IMG_DATA/` and download the folders/files you would need for the calculation of the according index (e.g. R10m/*B04.jp2 and R10m/*B08.jpg for the NDVI)
12. When downloaded, put the files in the `./data/raster/` folder
</details>
<br/>

## Usage

Open terminal and navigate to cloned/downloaded folder "index-calculator". Call the program with:

```
$ pip install -r ./requirements.txt -> use if you don't have the required packages installed in your environment yet

$ python src/main.py [shape_input_file_name] [index_name {ndmi, ndvi, reip, rgb}]
```
Example:
```
$ python src/main.py roi.shp ndvi
```

If you have any questions, wishes or ideas, feel free to ask me in the <a href="https://github.com/GrHalbgott/index-calculator/issues">issues section</a>, I'm looking forward to it. Have fun!
