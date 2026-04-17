"""
Rotina: 01.11 - Produtos
Descrição: Baixa um CSV com os produtos cadastrados no Promax.
Autor: Isac
Migrado para ai_vision em: [data]

O QUE MUDOU NESSA MIGRAÇÃO:
    - Removido: from function.img_func import encontrar_imagem, clicar_imagem, CSV_BTN_2, SALVAR_BTN
    - Removido: import time  (não precisamos mais de sleeps fixos)
    - Adicionado: from function.ai_vision import aguardar_estado_ia, ESTADOS
    - Adicionado: from function.acoes import AGUARDAR_DOWNLOAD_SALVAR
    - time.sleep(5) após aguardar_tela_carregar → REMOVIDO
      (aguardar_tela_carregar já usa WebDriverWait, o sleep era redundante)
    - time.sleep(2) antes do GerarCsv() → REMOVIDO
      (não havia motivo técnico, era só margem de segurança desnecessária)
    - encontrar_imagem(SALVAR_BTN, timeout=120) + bloco de retry → SUBSTITUÍDO
      por aguardar_estado_ia(**AGUARDAR_DOWNLOAD_SALVAR)
      A IA faz a mesma coisa (detecta o botão Salvar) mas sem precisar
      de imagem de template e com retry embutido no próprio loop.
    - time.sleep(5) no final → REMOVIDO
      (não precisamos mais: a IA já confirmou que o botão apareceu)
    - Todo o bloco de código comentado → REMOVIDO
      (o Git guarda o histórico, código morto polui a leitura)
"""

import logging

import pyautogui
from function.abrir_rotinas import abrir_rotinas
from function.acoes import AGUARDAR_DOWNLOAD_SALVAR
from function.ai_vision import ESTADOS, aguardar_estado_ia
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Código da rotina no Promax
CODIGO_ROTINA = "0111"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    Tudo começa por aqui.
    """
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)
    # ✂️ REMOVIDO: time.sleep(5) — aguardar_tela_carregar já usa WebDriverWait

    # Centraliza o mouse (mantém tela viva no VNC)
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    logging.info("⚙️ Configurando parâmetros da rotina 01.11...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    # ✂️ REMOVIDO: time.sleep(2) — não havia motivo técnico

    logging.info("📤 Executando GerarCsv() via JavaScript...")

    try:
        funcao_existe = driver.execute_script("return typeof GerarCsv === 'function';")
        if not funcao_existe:
            logging.error("❌ Função GerarCsv não encontrada na página.")
            return "skip"

        driver.execute_script("return GerarCsv();")

    except Exception as e:
        logging.error(f"❌ Erro ao executar GerarCsv(): {e}")
        return "skip"

    # ✅ NOVO: IA aguarda o botão Salvar aparecer na barra de download do Edge
    #
    # ANTES (frágil):
    #   encontrar_imagem(SALVAR_BTN, timeout=120)          ← depende de template PNG
    #   except TimeoutError:
    #       driver.execute_script("return GerarCsv();")    ← retry manual
    #       encontrar_imagem(SALVAR_BTN, timeout=180)      ← outro template
    #       except TimeoutError: return "skip"
    #
    # AGORA (robusto):
    #   aguardar_estado_ia() tira screenshots em loop e consulta a IA.
    #   Se aparecer "sem_dados" ou "erro", retorna skip automaticamente.
    #   O retry está embutido — enquanto o timeout não estourar, continua tentando.
    logging.info("⏳ Aguardando barra de download aparecer...")
    try:
        analise = aguardar_estado_ia(
            **AGUARDAR_DOWNLOAD_SALVAR,
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando download do CSV de Produtos",
        )
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando download na rotina {CODIGO_ROTINA}")
        return "skip"

    # Se a IA detectou erro ou sem dados, pula
    if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
        logging.warning(f"⏭️ {analise.get('mensagem')} — pulando")
        return "skip"

    logging.info("✅ Barra de download detectada — executor.py vai salvar o arquivo")
    # ✂️ REMOVIDO: time.sleep(5) — não precisamos mais, a IA já confirmou que está pronto
    # O executor.py chama salvar_arquivo() após o retorno desta função