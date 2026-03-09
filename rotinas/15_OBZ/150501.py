"""
Rotina: 15.05.01 - Lançamentos detalhados OBZ
Descrição: Relatório de lançamentos do OBZ
Autor: Carol
"""

import logging

from function.abrir_rotinas import abrir_rotinas
from function.funcoes_rotina import aguardar_tela_carregar, atalho_alt
from function.troca_janela import trocar_para_nova_janela
from function.img_func import clicar_imagem, encontrar_imagem, CSV_BTN, VISUALIZAR_BTN
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
from function.data_func import ano_vigente

# Código da rotina no Promax
CODIGO_ROTINA = "150501"

def executar(driver, **kwargs):
    """
    Função principal da rotina.
    """

    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)
    time.sleep(5)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    logging.info("⚙️ Configurando parâmetros da rotina 15.05.01...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    logging.info(f"Janelas abertas: {driver.window_handles}")
    logging.info(f"Janela atual: {driver.current_window_handle}")

    # -------------------------
    # Quebra 1 = Período (A)
    # -------------------------
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "idPeriodo")))

    driver.execute_script("arguments[0].value = 'A'; arguments[0].onchange();", select_quebra1)

    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para Período Anual (A)")

    # -------------------------
    # Data = Ano vigente
    # -------------------------   

    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dtAno")))

    driver.execute_script(f"arguments[0].value = '{ano_vigente()}';", data_inicial)
    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Ano configurado para {ano_vigente()}")

    # CLICAR NO BOTÃO DE NBZ
    clicar_botao_imagem("images/nbz.png","NBZ",30)

    # CLICAR NO BOTÃO DE DEPTO
    clicar_botao_imagem("images/depto.png","DEPTO",30)

    # CLICAR NO BOTÃO DE PACOTE
    clicar_botao_imagem("images/pacote.png","PACOTE",30)

    # CLICAR NO BOTÃO DE VBZ
    clicar_botao_imagem("images/vbz.png","VBZ",30)

    # CLICAR NO BOTÃO DE CONTA
    clicar_botao_imagem("images/conta.png","CONTA",30)

    time.sleep(2)

    logging.info("📤 Tentando usar o atalho Alt+V para visualizar...")
    atalho_alt("v")

    # Verifica se o botão do CSV aparece (sucesso do Alt+V)
    # Se não aparecer em 300s (5 min), assume falha e tenta clicar no visualizar manualmente
    try:
        # Tenta encontrar o botão CSV que indica que o relatório carregou
        logging.info("⏳ Aguardando processamento do relatório (Até 2 min)...")
        encontrar_imagem(CSV_BTN, timeout=120) 
    except TimeoutError:
        logging.warning("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
        clicar_imagem(VISUALIZAR_BTN, timeout=10) # Tenta clicar no botão visualizar
        
        # Espera novamente pelo resultado
        logging.info("⏳ Aguardando processamento (2ª tentativa)...")
        try:
            encontrar_imagem(CSV_BTN, timeout=300)
        except TimeoutError:
            logging.error("❌ Falha crítica: Relatório não carregou.")
            return

    logging.info("⏳ Relatório gerado! Iniciando download...")

    # Clica no CSV para baixar
    time.sleep(2)
    clicar_imagem(CSV_BTN)
    
    logging.info("⏳ Aguardando download...")


def clicar_botao_imagem(caminho, nome, timeout=30):
    inicio = time.time()

    while time.time() - inicio < timeout:

        pos = pyautogui.locateOnScreen(caminho, confidence=0.8)

        if pos:
            logging.info(f"✅ Clicando no botão de {nome}...")

            x = pos.left + pos.width - 10
            y = pos.top + pos.height // 2

            time.sleep(1)
            pyautogui.click(x, y)
            return

        time.sleep(0.5)
    msg = f"❌ Botão {nome} não encontrado."
    logging.error(msg)
    raise TimeoutError(msg)