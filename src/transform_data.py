import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

# criar dataframe 
def create_dataframe(path_name:str) -> pd.DataFrame:

    logging.info("→ Criando DataFrame do arquivo JSON...")
    path = path_name
    
    # se o arquivo não existir, lança um erro
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    # lê o arquivo JSON e cria um DataFrame
    with open(path) as f:
        data = json.load(f)
        
    # normaliza os dados JSON em um DataFrame do Pandas
    df = pd.json_normalize(data)
    logging.info(f"\n✓ DataFrame criado com {len(df)} linha(s)")
    return df

# normalizar a coluna 'weather' e criar novas colunas
def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    # coluna 'weather' é uma lista de dicionários, então precisamos normalizar essa coluna para criar novas colunas no DataFrame
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))
    
    # renomear as colunas do DataFrame df_weather para evitar conflitos de nomes com o DataFrame original
    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })
    
    # log que a coluna 'weather' foi normalizada e quantas colunas foram criadas
    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"\n✓ Coluna 'weather' normalizada - {len(df.columns)} colunas")
    return df

# remover colunas 
def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n→ Removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    logging.info(f"✓ Colunas removidas - {len(df.columns)} colunas restantes")
    return df 

# renomeando colunas
def rename_columns(df: pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    logging.info(f"\n→ Renomeando {len(columns_names)} colunas...")
    df = df.rename(columns=columns_names)
    logging.info("✓ Colunas renomeadas")
    return df 
    
# normalizar colunas de data e hora
def normalize_datetime_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n→ Convertendo colunas para datetime: {columns_names}")
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
    logging.info("✓ Colunas convertidas para datetime\n")    
    return df

# carregando transformações
def data_transformations():
    print("\n Iniciando transformações")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info("✓ Transformações concluídas\n")
    return df
    