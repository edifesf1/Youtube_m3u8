
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "youtube.txt"
OUTPUT_FILE = BASE_DIR / "youtube.m3u"


def generate_m3u():
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text("", encoding="utf-8")

    links = [
        line.strip()
        for line in INPUT_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    lines = ["#EXTM3U"]

    for index, url in enumerate(links, start=1):
        if not url.startswith(("https://", "http://")):
            print(f"Link ignorado: {url}")
            continue

        lines.append(f"#EXTINF:-1,YouTube {index}")
        lines.append(url)

    OUTPUT_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8"
    )

    print(f"Playlist criada: {OUTPUT_FILE}")
    print(f"Links processados: {len(lines[1:]) // 2}")


if __name__ == "__main__":
    generate_m3u()
