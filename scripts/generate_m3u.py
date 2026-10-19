import subprocess, os

def get_stream_url(url):
    try:
        # Passa os cookies para o yt-dlp
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--cookies", "cookies.txt", url],
            capture_output=True,
            text=True,
            timeout=90
        )
        if result.returncode == 0:
            for linha in result.stdout.strip().split('\n'):
                if '.m3u8' in linha:
                    return linha.strip()
        # Tenta também com --live-from-start
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--cookies", "cookies.txt", "--live-from-start", url],
            capture_output=True,
            text=True,
            timeout=90
        )
        if result.returncode == 0:
            for linha in result.stdout.strip().split('\n'):
                if '.m3u8' in linha:
                    return linha.strip()
        # Mostra o ERRO real para sabermos por quê falhou
        if result.stderr:
            print(f"  ⚠️ yt-dlp diz: {result.stderr[:200]}")
        return None
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return None

# Iniciar
with open("youtube.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

# Ler canais
with open("youtube_channel_info.txt", "r", encoding="utf-8") as f:
    for linha in f:
        linha = linha.strip()
        if not linha or linha.startswith("#") or "," not in linha:
            continue
        
        nome, url = linha.split(",", 1)
        nome = nome.strip()
        url = url.strip()
        
        print(f"\n=== {nome} ===")
        link = get_stream_url(url)
        
        if link:
            with open("youtube.m3u", "a", encoding="utf-8") as f:
                f.write(f"#EXTINF:-1,{nome}\n{link}\n")
            print(f"✅ ADICIONADO!")
        else:
            print(f"❌ SEM LINK")

print("\n=== FIM ===")
