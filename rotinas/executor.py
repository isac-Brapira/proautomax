import json
from function.download import configurar_download, mover_arquivo


def executar_rotinas(driver, rotinas_registradas, caminho_json):
    configurar_download(driver)

    with open(caminho_json, encoding="utf-8") as f:
        config = json.load(f)


    for item in config["execucao"]:
        codigo = item["codigo"]
        destino = item["destino"]
        params = item.get("params", {})

        if codigo not in rotinas_registradas:
            raise Exception(f"Rotina {codigo} não registrada")

        print(f"▶ Executando rotina {codigo}")

        rotinas_registradas[codigo](driver, **params)

        print(f"Aguardando download da rotina {codigo}...")
        arquivo_final = mover_arquivo(codigo, destino)

        print(f"✔ Rotina {codigo} concluída. Arquivo salvo em: {arquivo_final}\n")
        
