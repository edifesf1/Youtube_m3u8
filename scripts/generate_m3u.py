import subprocess, sys, re

def get_live_video_url(channel_url):
    """Converte @canal/live → link do vídeo ativo watch?v=..."""
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(channel_url, headers=headers, timeout=15)
        # Procura link do vídeo ativo
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', r.text)
        if match:
            return f"https://www.youtube.com/watch?v={match.group(1)}"
    except:
        pass
    return None

def get_m3u8_url(video_url):
    """Usa yt-dlp no link DIRETO do vídeo"""
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-check-certificates", video_url],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if '.m3u8' in line:
                    return line.strip()
        return None
    except Exception as e:
        print(f"  Erro yt-dlp: {str(e)[:60]}")
        return None

# Iniciar arquivo
with open("youtube.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

# Processar canais
with open("youtube_channel_info.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "," not in line:
            continue
        
        name, url = line.split(",", 1)
        name = name.strip()
        url = url.strip()
        
        print(f"\nBuscando: {name}")
        
        # Passo 1: Descobrir vídeo ativo
        if "/live" in url or "/streams" in url:
            video_url = get_live_video_url(url)
            if not video_url:
                print(f"  ⚠️ Nenhuma transmissão ativa no momento")
                continue
            print(f"  Vídeo encontrado: {video_url}")
        else:
            video_url = url
        
        # Passo 2: Extrair link M3U8
        stream_url = get_m3u8_url(video_url)
        if stream_url:
            with open("youtube.m3u", "a", encoding="utf-8") as f:
                f.write(f"#EXTINF:-1,{name}\n{stream_url}\n")
            print(f"  ✅ Link adicionado!")
        else:
            print(f"  ❌ Não foi possível extrair o link")

print("\n=== Concluído ===")
