gis-convertor
=============

convert wgs84 data from imgs to ITM

#### How to convert from WGS84 to ____

If you want to convert to another projection (not ITM) go to http://spatialreference.org/ref/ and for your projction. 
After you found it change the line:
 prj_itm = Proj(init=epsg:2039)
Change the number after the epsg (2039 = Israel). 
For more info check pyproj docs at: https://code.google.com/p/pyproj/
  
