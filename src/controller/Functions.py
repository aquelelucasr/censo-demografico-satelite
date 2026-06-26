import math
import os
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv
import cv2
import numpy as np
import json



from model.databaseModel import save_result,save_search
from inference_sdk import InferenceHTTPClient


from controller import C_shared
from model import databaseModel

def debug_print(message):
    if C_shared.DEBUG:
        print("[DEBUG]"+str(message))

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


    if C_shared.GOOGLE_API_KEY == None or C_shared.GOOGLE_API_KEY == "":
        raise ValueError("Missing GOOGLE_MAPS_API_KEY in .env or system environment values")
    else:
        debug_print("GOOGLE API key loaded successfully")
    if C_shared.ROBOFLOW_API_KEY == None or C_shared.ROBOFLOW_API_KEY == "":
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

    id_search = save_search(slug,lat_tl,lon_tl,lat_br,lon_br)
    process_and_save_vision_data(id_search,image_path,square_side_size)

def make_annotated_image(image_path: str, predictions: list) -> None:
    img = cv2.imread(image_path)
    debug_print(f"annotating {image_path}")

    for pred in predictions:
        pts = np.array(
            [[p["x"], p["y"]] for p in pred["points"]],
            dtype=np.int32
        )

        cv2.polylines(
            img,
            [pts],
            isClosed=True,
            color=(0, 255, 0),
            thickness=2
        )

    filename =image_path.removeprefix("./media/raw/").removesuffix(".png")


    fp = f"{C_shared.FILEPATH}processed/{filename}.png"
    debug_print(f"Annotated {fp} successfully")
    cv2.imwrite(fp, img)

def get_population_from_image(image_path: str) -> int:
    """Envia a imagem para a IA, conta os telhados, e retorna a estimativa de população."""
    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=C_shared.ROBOFLOW_API_KEY
    )

    result = client.run_workflow(
        workspace_name="ian-martins-mendes",
        workflow_id="general-segmentation-api-6",
        images={
            "image": image_path  # Path recebido como argumento
        },
        parameters={"classes": "roof"},
        use_cache=True,  # cache workflow definition for 15 minutes
    )
    predictions = result[0]["predictions"]["predictions"]
    total_houses = len(predictions)
    population = total_houses * 3

    make_annotated_image(image_path,predictions)

    debug_print(f"Imagem: {image_path} | Casas: {total_houses} | População: {population}")

    return population


def get_searched_area(width_m: float) -> float:
    """Recebe a largura do mapa em metros e calcula a área total em km²."""
    # converte de metros para km e calcula a area do quadrado
    searched_area = (width_m * 0.001) ** 2

    debug_print(f"Largura do mapa: {width_m}m | Área pesquisada: {searched_area:.6f} km²")

    return searched_area


def get_population_density(population: int, searched_area: float) -> float:
    """Recebe a população estimada e a área (em km²) e cospe densidade populacional."""
    population_density = population / searched_area

    debug_print(f"População: {population} hab | Área: {searched_area:.6f} km² | Densidade: {population_density:.2f} hab/km²")

    return population_density


def process_and_save_vision_data(search_id: int, image_path: str, width_m: float) -> tuple:
    """Consulta a IA, calcula tudo que tem que calcular e salva os resultados no banco de dados."""

    debug_print(f"\nIniciando processamento para o ID {search_id}...")

    population = get_population_from_image(image_path)
    searched_area = get_searched_area(width_m)
    population_density = get_population_density(population, searched_area)

    save_result(search_id, population, population_density)

    debug_print("Fluxo de Visão Computacional e Banco de Dados finalizado com sucesso!\n")

    return population, searched_area, population_density


