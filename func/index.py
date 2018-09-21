import exifread
import os

# Return exif data for a file
def get_exif(file_path):
    # Open image file for reading (binary mode)
    f = open(file_path, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    return tags

# List all files in a directory
def list_all_files(directory):
    files = []

    # https://stackoverflow.com/a/41447012/6451184
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for file in f:
            if ".jpg" in file: # fixme: don't hardcode jpg!
                files.append( os.path.join(r, file) )

    return files

# https://gist.github.com/snakeye/fdc372dbf11370fe29eb
def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def get_exif_location(exif_data, file_name, current_dir):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return {
        'file_name': file_name.replace(current_dir + "/", ""),
        'location': {
            'lat': lat,
            'lon': lon
        }
    }




# Glue script made by myself :-)

def get_exif_data_for_folder(directory, current_dir):
    files = list_all_files(directory)

    data_list = []

    for file in files:
        exif_data = get_exif(file)

        data = get_exif_location(exif_data, file, current_dir)

        data_list.append(data)

    return data_list