gis-convertor
=============

#### Why?

My father need a tool to pull gis data from pics, convert it (from wgs84 to itm) and save all in a csv file. I did not write all the code, Parts of the code is from https://gist.github.com/erans/983821.



#### How to convert from WGS84 to ____

1. Find the projection number you need at http://spatialreference.org/ref/ (itm = 2039, wgs84 = 4326).
2. Go to line 83 (prj_itm = Proj(init=epsg:2039) and change the number.

##### Notes

1. look at the requirements.txt
2. I upload a pic for checking the tool.


For more info check pyproj docs at: https://code.google.com/p/pyproj/
  
