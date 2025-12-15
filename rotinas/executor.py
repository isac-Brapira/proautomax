import json


def executar_rotinas(driver, rotinas_registradas, caminho_json):
    with open(caminho_json, encoding="utf-8") as f:
        config = json.load(f)

    for item in config["execucao"]:
        codigo = item["codigo"]
        params = item.get("params", {})

        if codigo not in rotinas_registradas:
            raise Exception(f"Rotina {codigo} não registrada")

        print(f"▶ Executando rotina {codigo}")
        rotinas_registradas[codigo](driver, **params)
        
