import math
import os
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv

from app.Controller import C_shared

from app.Model import databaseModel

def debug_print(message):
    if C_shared.DEBUG:
        print(message)

def create_media_folders():
    raw = Path(C_shared.FILEPATH+"raw")
    processed = Path(C_shared.FILEPATH+"processed")
    if not raw.is_dir():
        raw.mkdir(parents=True, exist_ok=True)
    if not processed.is_dir():
        processed.mkdir(parents=True, exist_ok=True)


def setup_api_keys() -> None:
    load_dotenv()
    C_shared.GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    C_shared.ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
    if C_shared.GOOGLE_API_KEY == "":
        raise ValueError("Missing GOOGLE_MAPS_API_KEY in .env or system environment values")
    else:
        debug_print("GOOGLE API key loaded successfully")
    if C_shared.ROBOFLOW_API_KEY == "":
        raise ValueError("Missing ROBOFLOW_API_KEY in .env or system environment values")
    else:
        debug_print("roboflow key loaded successfully")

def get_satellite_image(lat, lon,slug, zoom) -> str:

    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": f"{C_shared.IMAGE_SIZE}x{C_shared.IMAGE_SIZE}",
        "maptype": "satellite",
        "scale": 1,
        "key": C_shared.GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)

    create_media_folders()
    fp = f"{C_shared.FILEPATH}raw/{slug}.png"
    if response.status_code == 200:
        with open(fp, "wb") as f:
            f.write(response.content)
    else:
        debug_print(f"Failed: {lat}, {lon}")
        debug_print(params)
        debug_print(response.status_code)
        debug_print(response.text)

    return fp


def get_map_image(lat_tl,lon_tl,lat_br,lon_br) -> None:
    center_lat = (lat_tl+lat_br) / 2
    center_lon = (lon_tl + lon_br) / 2

    debug_print(f"{lat_tl},{lon_tl}")
    debug_print(f"{lat_br},{lon_br}")
    debug_print(f"{center_lat},{center_lon}")

    width_deg  = abs(lat_br-lat_tl)
    height_deg = abs(lon_br-lon_tl)

    width_m    = width_deg * 111320
    height_m   = height_deg * 111320 * math.cos(math.radians(center_lat))

    if width_m > height_m:
        square_side_size = height_m
    elif width_m < height_m:
        square_side_size = width_m
    else:
        square_side_size = height_m

    mpp = square_side_size / 512

    zoom = math.log2(
        156543.03392 * math.cos(math.radians(center_lat)) / mpp
    )
    zoom = round(zoom)

    slug = f"{center_lat} {center_lon} {zoom} {str(int(datetime.datetime.now().timestamp()))}"

    image_path = get_satellite_image(center_lat, center_lon, slug,zoom)

    searchID = databaseModel.save_search(slug,lat_tl,lon_tl,lat_br,lon_br)






