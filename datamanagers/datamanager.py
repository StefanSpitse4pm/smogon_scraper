import pandas as pd
from database import DatabaseConnection
from models import Pokemon
from sqlalchemy import select

db_conn = DatabaseConnection()
db_output = pd.DataFrame(db_conn._create_session(select(Pokemon)))

filterd_pokemon = db_output.loc[(db_output["gen"] == "ss") & (db_output["format"] == "OU")]

filterd_pokemon