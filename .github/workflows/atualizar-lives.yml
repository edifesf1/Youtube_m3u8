
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARQUIVO_CANAIS = ROOT / "canais.txt"
ARQUIVO_LISTA = ROOT / "youtube.txt"


def carregar_canais():
    canais = []

    for linha in ARQUIVO_CANAIS.read_text(
        encoding="utf-8-sig"
    ).splitlines():
        linha = linha.strip()

        if not linha or linha.startswith("#") or "|" not in linha:
            continue

        nome, url = linha.split("|", 1)
        canais.append((nome.strip(), url.strip()))

    return canais


def obter_live(url):
    comando = [
        "yt-dlp",
        "--dump-single-json",
        "--no-warnings",
        "--no-playlist",
        "--skip-download",
        url,
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if resultado.returncode != 0 or not resultado.stdout.strip():
        raise RuntimeError(
            resultado.stderr.strip() or "Não foi possível consultar o canal"
        )

    dados = json.loads(resultado.stdout)

    # Só aceita uma transmissão identificada como AO VIVO.
    if dados.get("is_live") is not True:
        raise RuntimeError(
            "A consulta não confirmou uma transmissão ao vivo."
        )

    video_id = str(dados.get("id", "")).strip()

    # IDs de vídeos do YouTube normalmente têm 11 caracteres.
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise RuntimeError("ID de transmissão inválido.")

    return video_id


def atualizar():
    if not ARQUIVO_CANAIS.exists():
        raise FileNotFoundError("Arquivo canais.txt não encontrado.")

    if not ARQUIVO_LISTA.exists():
        raise FileNotFoundError("Arquivo youtube.txt não encontrado.")

    linhas = ARQUIVO_LISTA.read_text(
        encoding="utf-8-sig"
    ).splitlines()

    alteracoes = 0

    for nome, url in carregar_canais():
        print(f"\nConsultando: {nome}")

        try:
            video_id = obter_live(url)
            nova_url = f"https://www.youtube.com/live/{video_id}"
        except Exception as erro:
            print(f"Sem atualização para {nome}: {erro}")
            continue

        encontrados = 0

        for i, linha in enumerate(linhas):
            if not linha.strip() or linha.lstrip().startswith("#"):
                continue

            partes = linha.split("|")

            if len(partes) < 2:
                continue

            nome_na_lista = partes[-2].strip()

            if nome_na_lista.casefold() != nome.casefold():
                continue

            encontrados += 1

            if partes[-1].strip() != nova_url:
                partes[-1] = nova_url
                linhas[i] = "|".join(partes)
                alteracoes += 1
                print(f"Atualizado: {nome} -> {video_id}")
            else:
                print(f"Já está atualizado: {nome}")

        if encontrados == 0:
            print(
                f"ATENÇÃO: não encontrei uma linha com o nome "
                f"'{nome}' no youtube.txt. Nenhuma linha foi criada."
            )

    if alteracoes:
        ARQUIVO_LISTA.write_text(
            "\n".join(linhas) + "\n",
            encoding="utf-8",
        )
        print(f"\nTotal de URLs alteradas: {alteracoes}")
    else:
        print("\nNenhuma alteração necessária.")


if __name__ == "__main__":
    atualizar()
