import requests, re

def grab(line):
    if not line.strip() or line.startswith('#'):
        return
    if ',' not in line:
        return
    name, url = line.split(',', 1)
    name = name.strip()
    url = url.strip()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        text = r.text

        # Tenta VÁRIOS padrões de busca
        match = None
        
        # Padrão 1: hlsManifestUrl
        match = re.search(r'"hlsManifestUrl":"([^"]+)"', text)
        if not match:
            match = re.search(r'"hlsManifestUrl"\s*:\s*"([^"]+)"', text)
        
        # Padrão 2: qualquer .m3u8 na página
        if not match:
            match = re.search(r'(https://[^"\']+\.googlevideo\.com[^"\']+\.m3u8[^"\']*)', text)
        
        # Padrão 3: streamingData
        if not match:
            match = re.search(r'"streamingData"\s*:\s*\{[^}]*"hlsManifestUrl":"([^"]+)"', text)

        if match:
            link = match.group(1).replace('\\u0026', '&').replace('\\u003D', '=')
            with open('youtube.m3u', 'a', encoding='utf-8') as f:
                f.write(f'#EXTINF:-1,{name}\n{link}\n')
            print(f'✅ {name} — OK')
        else:
            print(f'⚠️  {name} — NÃO está ao vivo OU link não encontrado')

    except Exception as e:
        print(f'❌ {name}: {str(e)[:50]}')


# Limpa e recria o arquivo
with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')

# Processa cada canal
with open('youtube_channel_info.txt', 'r', encoding='utf-8') as f:
    for line in f:
        grab(line)

print('\nConcluído!')
