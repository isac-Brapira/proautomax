import json
import logging
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
        logging.error(f"❌ Erro: Arquivo de configuração não encontrado: {caminho_json}")
        return

    try:
        with open(caminho_json, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"❌ Erro ao ler JSON: {e}")
        return

    total = len(config["execucao"])
    logging.info(f"📋 {total} rotina(s) para executar\n")

    rotinas_salvas = []
    rotinas_erros = []
    rotinas_ignoradas = []

    for idx, item in enumerate(config["execucao"], 1):

        codigo = item["codigo"]
        
        if not item.get("ativo", True): # Default to True if missing for backward compatibility
            logging.warning(f"⏭️ Rotina {codigo} ignorada (ativo=False)")
            rotinas_ignoradas.append(codigo)
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
        
        logging.info(f"'{codigo}'")
        for r in rotinas_registradas:
                logging.info(f"'{r}'")

        if codigo not in rotinas_registradas:
            logging.error(f"❌ Erro: Rotina {codigo} não registrada")
            continue
        
        
        logging.info("="*60)
        logging.info(f"▶ [{idx}/{total}] {descricao} (Código: {codigo})")
        logging.info(f"📄 Arquivo: {nome}")
        logging.info(f"📂 Destino: {destino}")
        logging.info("="*60)

        try:
            # 1. Executa a rotina (gera o relatório no navegador)
            logging.info("📤 Executando rotina...")
            resultado = rotinas_registradas[codigo](driver, **params)
            # Adicionado retorno caso apareça caixa de diálogo "sem informações para listar"
            if resultado == "skip":
                logging.warning('⏭️ Pulando rotina... \n')
                rotinas_ignoradas.append(codigo)
                if driver.current_window_handle != promaxPrimeiraJanela:
                    driver.close()
                    driver.switch_to.window(promaxPrimeiraJanela)
                continue
            # 2. Salva o arquivo usando a função completa do download.py
            # Ela cuida de abrir o diálogo, digitar o caminho e validar o arquivo
            arquivo_final = salvar_arquivo(destino, nome)

            logging.info(f"✓ Concluído: {arquivo_final}\n")
            rotinas_salvas.append(codigo)

            pyautogui.moveTo(0, 0)


            driver.close()

            driver.switch_to.window(promaxPrimeiraJanela)

        except Exception as e:
            logging.error(f"❌ Erro ao executar rotina {codigo}: {e}")
            rotinas_erros.append(codigo)
            # Importante: traceback ajuda muito a debugar
            import traceback
            traceback.print_exc()
            continue

    logging.info("*=="*25)
    logging.info("📊 RESUMO DA EXECUÇÃO")
    logging.info(f"✅ Foram {len(rotinas_salvas)} rotinas salvas com sucesso. {rotinas_salvas}")
    logging.info(f"❌ Dentre elas {len(rotinas_erros)} resultaram em erro. {rotinas_erros}")
    logging.info(f"⏭️ E {len(rotinas_ignoradas)} foram ignoradas. {rotinas_ignoradas}")
    logging.info("^=="*25)
    
    driver.quit()
    logging.info("="*60)
    logging.info("✓ EXECUÇÃO FINALIZADA 🍻")
    logging.info("="*60)