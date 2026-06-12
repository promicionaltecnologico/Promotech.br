import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

html_path = '/home/ubuntu/browser_html/affili-buddy-kit_lovable_app_page_1781247218600.html'
base_url = 'https://affili-buddy-kit.lovable.app/'

with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Criar diretório para assets
os.makedirs('/home/ubuntu/site_assets', exist_ok=True)

def download_asset(url, folder):
    if not url:
        return None
    full_url = urljoin(base_url, url)
    parsed_url = urlparse(full_url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        return None
    
    filepath = os.path.join(folder, filename)
    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"Erro ao baixar {full_url}: {e}")
    return None

# Extrair links de CSS e JS
css_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
js_links = [script.get('src') for script in soup.find_all('script') if script.get('src')]
img_links = [img.get('src') for img in soup.find_all('img')]

print(f"CSS encontrados: {css_links}")
print(f"JS encontrados: {js_links}")
print(f"Imagens encontradas: {img_links}")

# Salvar as listas para referência
with open('/home/ubuntu/asset_list.txt', 'w') as f:
    f.write(f"CSS: {css_links}\n")
    f.write(f"JS: {js_links}\n")
    f.write(f"Imagens: {img_links}\n")
