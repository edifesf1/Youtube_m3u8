import subprocess

def get_m3u8_url(channel_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", channel_url],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            if url and '.m3u8' in url:
                return url
        return None
    except Exception as e:
        print(f"  Erro: {e}")
        return None

# Iniciar arquivo
with open("youtube.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

# Processar canais
with open("youtube_channel_info.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," not in line:
            continue
        
        name, url = line.split(",", 1)
        name = name.strip()
        url = url.strip()
        
        print(f"Buscando: {name}...")
        stream_url = get_m3u8_url(url)
        
        if stream_url:
            with open("youtube.m3u", "a", encoding="utf-8") as f:
                f.write(f"#EXTINF:-1,{name}\n{stream_url}\n")
            print(f"  ✅ Adicionado!")
        else:
            print(f"  ⚠️ Sem transmissão ao vivo")

print("\nConcluído!")
