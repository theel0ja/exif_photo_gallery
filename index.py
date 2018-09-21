from func.index import get_exif_data_for_folder
import os

# Run it
image_dir = os.getcwd() + "/images" # TODO: probably a better way

print(get_exif_data_for_folder(image_dir))