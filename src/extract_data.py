import requests 
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# extrair dados de clima de uma API e salvar em um arquivo JSON
def extract_weather_data(url:str) -> list:
    # faz uma requisição GET e transforma em JSON
    response = requests.get(url)
    data = response.json()
    
    # verifica se a requisição foi bem sucedida e se há dados retornados
    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []
    
    # verifica se há dados retornados
    if not data:
        logging.warn("Nenhum dado retornado")
        return []
    
    # defini o caminho do arquivo de saída e cria o diretório se não existir
    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # salva os dados em um arquivo JSON
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    # loga a mensagem de sucesso
    logging.info(f"Arquivo salvo em {output_path}")  
    return data
