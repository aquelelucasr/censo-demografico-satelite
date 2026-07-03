GOOGLE_API_KEY = ""
ROBOFLOW_API_KEY = ""
IMAGE_SIZE = 512
IMG_FILEPATH = "./media/"

DB_FILEPATH = "./database/"
DEBUG = True

def debug_print(message):
    if DEBUG:
        print("[DEBUG]"+str(message))

def get_center(lat_tl,lon_tl,lat_br,lon_br) -> tuple[float,float]:
    center_lat = (float(lat_tl) + float(lat_br)) / 2
    center_lon = (float(lon_tl) + float(lon_br)) / 2
    return center_lat,center_lon