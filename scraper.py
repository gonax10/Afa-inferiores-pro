import requests
from bs4 import BeautifulSoup
import json
import os

def get_table_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        
        data = []
        for row in rows[1:]: # Saltamos el encabezado
            cols = row.find_all('td')
            if len(cols) > 1:
                data.append({
                    "pos": cols[0].text.strip(),
                    "club": cols[1].text.strip(),
                    "pj": cols[2].text.strip(),
                    "g": cols[3].text.strip(),
                    "e": cols[4].text.strip(),
                    "p": cols[5].text.strip(),
                    "gf": cols[6].text.strip(),
                    "gc": cols[7].text.strip(),
                    "dg": cols[8].text.strip(),
                    "pts": cols[9].text.strip()
                })
        return data
    except Exception as e:
        print(f"Error en {url}: {e}")
        return []

# Configuración de categorías y URLs de Sábado Gol
urls = {
    "2013": "https://sabadogol.com.ar/infantiles-a-cat-2013/",
    "2014": "https://sabadogol.com.ar/infantiles-a-cat-2014/",
    "2015": "https://sabadogol.com.ar/infantiles-a-cat-2015/",
    "2016": "https://sabadogol.com.ar/infantiles-a-cat-2016/"
}

final_data = {}
for year, url in urls.items():
    final_data[year] = get_table_data(url)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)
