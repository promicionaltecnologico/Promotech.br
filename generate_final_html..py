import os
from bs4 import BeautifulSoup
import base64

html_path = '/home/ubuntu/browser_html/affili-buddy-kit_lovable_app_page_1781247218600.html'
css_path = '/home/ubuntu/site_assets/styles-Dad8yXsO.css'
logo_path = '/home/ubuntu/site_assets/logo-BZhf5zyy.png'

# Ler CSS
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Ler Logo e converter para base64
with open(logo_path, 'rb') as f:
    logo_base64 = base64.b64encode(f.read()).decode('utf-8')
    logo_data_uri = f"data:image/png;base64,{logo_base64}"

# Ler HTML original
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Remover scripts externos que podem quebrar ou rastrear
for script in soup.find_all('script'):
    script.decompose()

# Remover o badge do Lovable
badge = soup.find(id='lovable-badge')
if badge:
    badge.decompose()

# Substituir links de CSS por estilo embutido
for link in soup.find_all('link', rel='stylesheet'):
    link.decompose()

style_tag = soup.new_tag('style')
style_tag.string = css_content
soup.head.append(style_tag)

# Substituir logos locais por data URI
for img in soup.find_all('img'):
    src = img.get('src', '')
    if '/assets/logo' in src:
        img['src'] = logo_data_uri

# Garantir que o charset e viewport estejam corretos
if not soup.find('meta', charset=True):
    meta_charset = soup.new_tag('meta', charset='utf-8')
    soup.head.insert(0, meta_charset)

# Salvar o resultado
output_path = '/home/ubuntu/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print(f"HTML gerado com sucesso em: {output_path}")
