
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "youtube.txt"
OUTPUT = BASE / "youtube.m3u"


def generate():
    entries = ["#EXTM3U"]

    if not INPUT.exists():
        raise FileNotFoundError("Arquivo youtube.txt não encontrado")

    for line in INPUT.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "|" not in line:
            print(f"Linha ignorada: {line}")
            continue

        name, url = (part.strip() for part in line.split("|", 1))

        if not name or not url.startswith("https://"):
            print(f"Entrada inválida: {line}")
            continue

        if ".m3u8" not in url.split("?", 1)[0].lower():
            print(f"Aviso: URL sem extensão .m3u8: {name}")

        entries.extend([
            f"#EXTINF:-1,{name}",
            url
        ])

    OUTPUT.write_text(
        "\n".join(entries) + "\n",
        encoding="utf-8"
    )

    print(f"Playlist criada: {OUTPUT}")


if __name__ == "__main__":
    generate()
