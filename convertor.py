from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pyproj import Proj, transform
import glob, csv, os

#------------------------------------------------------------------
# this part from https://gist.github.com/erans/983821


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lon, lat


#------------------------------------------------------------------

def reproject_wgs_to_itm(longitude, latitude):
    if longitude == None or latitude == None:
        return None, None
    else:
        prj_wgs = Proj(init='epsg:4326')
        prj_itm = Proj(init='epsg:2039')
        x, y = transform(prj_wgs, prj_itm, longitude, latitude)
        return x, y


def main_lat_lon():
    ''' take the data from the pic and return a list with the data'''
    lst = []
    for infile in glob.glob("*.jpg"):
        temp_lst = []
        
        # append file names to the list
        file_name, ext = os.path.splitext(infile)
        temp_lst.append(file_name)
        
        # get lat and lon from the image 
        im = Image.open(infile)
        exif_data = get_exif_data(im)
        Wlon, Wlat = get_lat_lon(exif_data)
        prj4 = reproject_wgs_to_itm(Wlon, Wlat)
        for cord in prj4:
            temp_lst.append(cord)
        # convert lat and lon to itm & append to lst
        lst.append(temp_lst)
    return lst

#print main_lat_lon() 

def main():
    ''' write the data in csv file  
        a file without data (None output) will show a blank row  '''

    with open('converted_data.csv', 'wb') as f:
        writer = csv.writer(f)
        lst_lan_lon = main_lat_lon()
        for i in lst_lan_lon:
            writer.writerow(i)

    
main()



    





    


