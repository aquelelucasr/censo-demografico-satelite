from app.Controller.Functions import *
from app.Model.databaseModel import setup_db


setup_db()
setup_api_keys()

get_map_image(-28.9486767,-49.4689805,-28.9513217,-49.4638693)
