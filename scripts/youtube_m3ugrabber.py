import requests, re

def grab(line):
    if not line.strip() or line.startswith('#'):
        return
    name, url = line.split(',', 1)
    name = name.strip()
    url = url.strip()
    
    try:
        r = requests.get(url, timeout=15)
        match = re.search(r'"hlsManifestUrl":"([^"]+)"', r.text)
        if match:
            link = match.group(1).replace('\\u0026', '&')
            with open('youtube.m3u', 'a', encoding='utf-8') as f:
                f.write(f'#EXTINF:-1,{name}\n{link}\n')
            print(f'✅ {name}')
    except Exception as e:
        print(f'❌ {name}: {e}')

with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')

with open('youtube_channel_info.txt', 'r', encoding='utf-8') as f:
    for line in f:
        grab(line)

print('Pronto!')
