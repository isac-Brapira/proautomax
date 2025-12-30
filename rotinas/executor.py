import json
from time import time
from function.download import salvar_arquivo


def executar_rotinas(driver, rotinas_registradas, caminho_json):
    """
    Executa as rotinas definidas no arquivo JSON.
    
    Args:
        driver: WebDriver do Selenium
        rotinas_registradas: Dicionário com as rotinas carregadas
        caminho_json: Caminho do arquivo rotinas.json
    """
    with open(caminho_json, encoding="utf-8") as f:
        config = json.load(f)

    total = len(config["execucao"])
    print(f"📋 {total} rotina(s) para executar\n")

    for idx, item in enumerate(config["execucao"], 1):
        codigo = item["codigo"]
        destino = item["destino"]
        descricao = item.get("descricao", codigo)
        params = item.get("params", {})

        if codigo not in rotinas_registradas:
            print(f"❌ Erro: Rotina {codigo} não registrada")
            continue

        print("="*60)
        print(f"▶ [{idx}/{total}] {descricao} (Código: {codigo})")
        print("="*60)

        try:
            # Executa a rotina (ela vai gerar o CSV e deixar pronto pra salvar)
            print("📤 Executando rotina...")
            rotinas_registradas[codigo](driver, **params)
              # Pequena pausa antes de salvar

            # Agora usa "Salvar Como" pra salvar direto no destino
            arquivo_final = salvar_arquivo()

            

            print(f"✓ Concluído: {arquivo_final}\n")

        except Exception as e:
            print(f"❌ Erro ao executar rotina {codigo}: {e}\n")
            # Continua com as próximas rotinas mesmo se uma falhar
            continue

    print("="*60)
    print("✓ EXECUÇÃO FINALIZADA")
    print("="*60)