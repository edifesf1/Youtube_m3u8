
from pathlib import Path

BASE = Path(__file__).resolve().parent
ARQUIVO_ENTRADA = BASE / "youtube.txt"
ARQUIVO_SAIDA = BASE / "youtube.m3u"


def gerar_playlist():
    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError("Crie o arquivo youtube.txt primeiro.")

    linhas = ["#EXTM3U"]
    total = 0

    for linha in ARQUIVO_ENTRADA.read_text(
        encoding="utf-8"
    ).splitlines():
        linha = linha.strip()

        if not linha or linha.startswith("#"):
            continue

        if "|" in linha:
            nome, url = linha.split("|", 1)
            nome, url = nome.strip(), url.strip()
        else:
            nome, url = f"YouTube {total + 1}", linha

        if not url.startswith("https://"):
            print(f"Link ignorado: {url}")
            continue

        linhas.append(f"#EXTINF:-1,{nome}")
        linhas.append(url)
        total += 1

    ARQUIVO_SAIDA.write_text(
        "\n".join(linhas) + "\n",
        encoding="utf-8"
    )

    print(f"Playlist criada: {ARQUIVO_SAIDA}")
    print(f"Entradas: {total}")


if __name__ == "__main__":
    gerar_playlist()
