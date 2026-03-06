import json
import os
import pyautogui
# Importa a função completa de salvar, não apenas a que abre a janela
# Se o arquivo download.py estiver numa pasta "function", mude para: from function.download import salvar_arquivo
from function.download import salvar_arquivo 
from function.data_func import ano_vigente, gerar_nome_mes_vigente


def executar_rotinas(driver, rotinas_registradas, caminho_json):
    """
    Executa as rotinas definidas no arquivo JSON.
    
    Args:
        driver: WebDriver do Selenium
        rotinas_registradas: Dicionário com as rotinas carregadas
        caminho_json: Caminho do arquivo rotinas.json
    """
    # Verifica se o arquivo existe antes de tentar abrir

    promaxPrimeiraJanela = driver.current_window_handle

    if not os.path.exists(caminho_json):
        print(f"❌ Erro: Arquivo de configuração não encontrado: {caminho_json}")
        return

    try:
        with open(caminho_json, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return

    total = len(config["execucao"])
    print(f"📋 {total} rotina(s) para executar\n")

    for idx, item in enumerate(config["execucao"], 1):

        codigo = item["codigo"]
        
        if not item.get("ativo", True): # Default to True if missing for backward compatibility
            print(f"⏭️ Rotina {codigo} ignorada (ativo=False)")
            continue
        # CORREÇÃO: Removidas as vírgulas que transformavam strings em tuplas
        destino = item["destino"]
        
        params = item.get("params", {})

        if params.get("nomeMes") == "MES_ATUAL":
            nome_mes_vigente = gerar_nome_mes_vigente()
            nome = f"{nome_mes_vigente}.csv"

        elif params.get("anoVigente") == "ANO_VIGENTE":
            nome = f"{codigo}_{ano_vigente()}.csv"

        else:
            nome = item.get("nome", f"{codigo}.csv")
        
        descricao = item.get("descricao", codigo)
        
        print(f"'{codigo}'")
        for r in rotinas_registradas:
                print(f"'{r}'")

        if codigo not in rotinas_registradas:
            print(f"❌ Erro: Rotina {codigo} não registrada")
            continue
        
        
        print("="*60)
        print(f"▶ [{idx}/{total}] {descricao} (Código: {codigo})")
        print(f"📄 Arquivo: {nome}")
        print(f"📂 Destino: {destino}")
        print("="*60)

        try:
            # 1. Executa a rotina (gera o relatório no navegador)
            print("📤 Executando rotina...")
            resultado = rotinas_registradas[codigo](driver, **params)
            # Adicionado retorno caso apareça caixa de diálogo "sem informações para listar"
            if resultado == "skip":
                print('⏭️ Pulando rotina... \n')
                continue
            # 2. Salva o arquivo usando a função completa do download.py
            # Ela cuida de abrir o diálogo, digitar o caminho e validar o arquivo
            arquivo_final = salvar_arquivo(destino, nome)

            print(f"✓ Concluído: {arquivo_final}\n")

            pyautogui.moveTo(0, 0)


            driver.close()

            driver.switch_to.window(promaxPrimeiraJanela)

        except Exception as e:
            print(f"❌ Erro ao executar rotina {codigo}: {e}\n")
            # Importante: traceback ajuda muito a debugar
            import traceback
            traceback.print_exc()
            continue

    
    driver.quit()
    print("="*60)
    print("✓ EXECUÇÃO FINALIZADA")
    print("="*60)