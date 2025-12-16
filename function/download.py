import os
import time
import shutil

DOWNLOAD_PADRAO = r"E:\Code\proautomax\downloads\_temp"


def configurar_download(timeout=60):
    inicio = time.time()

    while time.time() - inicio < timeout:
        arquivos = [
            f for f in os.listdir(DOWNLOAD_PADRAO)
            if f.endswith(".csv")
        ]
        if arquivos:
            return arquivos[0]
        time.sleep(1)

    raise TimeoutError("Download não apareceu")


def mover_arquivo(nome_base, destino):
    os.makedirs(destino, exist_ok=True)

    arquivo = esperar_download()
    origem = os.path.join(DOWNLOAD_PADRAO, arquivo)

    novo = f"{nome_base}.csv"
    shutil.move(origem, os.path.join(destino, novo))
