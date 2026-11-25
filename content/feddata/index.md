{
  "title": "FedData",
  "type": "docs",
  "wordpress_id": 142,
  "lastmod": "2017-12-16T01:36:39Z",
  "toc_hide": true
}

One of the principal tasks of SKOPE is to develop tools to improve access to federated environmental data sources. To that end, we have begun developing <em>FedData</em>, a package for the <em>R</em> statistical environment implementing functions to automate downloading geospatial data available from several federated data sources (mainly sources maintained by the US Federal government).

Currently, the package enables extraction from seven datasets:

- The [National Elevation Dataset (NED)](https://nationalmap.gov/elevation.html) digital elevation models (1 and 1/3 arc-second; USGS)
- The [National Hydrography Dataset (NHD)](http://nhd.usgs.gov/) (USGS)
- The [Soil Survey Geographic (SSURGO) database](<https://websoilsurvey.sc.egov.usda.gov/App/HomePage.htm)>) from the National Cooperative Soil Survey (NCSS), which is led by the Natural Resources Conservation Service (NRCS) under the USDA,
- The [Global Historical Climatology Network (GHCN)](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn), coordinated by National Climatic Data Center at NOAA,
- The [Daymet](https://daymet.ornl.gov/) gridded estimates of daily weather parameters for North America, version 3, available from the Oak Ridge National Laboratory's Distributed Active Archive Center (DAAC)
- The [International Tree Ring Data Bank (ITRDB)](http://www.ncdc.noaa.gov/data-access/paleoclimatology-data/datasets/tree-ring), coordinated by National Climatic Data Center at NOAA.
- The [National Land Cover Database](https://www.mrlc.gov/) (NLCD) from 2011, 2006, and 2001.

This package is designed with the large-scale geographic information system (GIS) use-case in mind: cases where the use of dynamic web-services is impractical due to the scale (spatial and/or temporal) of analysis. It functions primarily as a means of downloading tiled or otherwise spatially-defined datasets; additionally, it can preprocess those datasets by extracting data within an area of interest (AoI), defined spatially. It relies heavily on the [**sp**](https://cran.r-project.org/web/packages/sp/index.html), [**raster**](https://cran.r-project.org/web/packages/raster/index.html), and [**rgdal**](https://cran.r-project.org/web/packages/rgdal/index.html) packages.

More information about FedData can be found [here. ](https://github.com/ropensci/FedData)
