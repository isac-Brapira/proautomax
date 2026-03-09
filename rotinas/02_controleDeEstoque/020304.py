"""
Rotina: 02.03.04
Descrição: Baixa um CSV com relatório de saldo da grade.
Autor: Carol
"""

import logging
import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.aceitar_alertas import aceitar_alertas
from function.data_func import data_ontem
from function.funcoes_rotina import aguardar_tela_carregar, atalho_alt
from function.img_func import CSV_BTN, VISUALIZAR_BTN, clicar_imagem, encontrar_imagem
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui


# Código da rotina no Promax
CODIGO_ROTINA = "020304"


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
    

    logging.info("⚙️ Configurando parâmetros da rotina 02.03.04 ...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    logging.info(f"Janelas abertas: {driver.window_handles}")
    logging.info(f"Janela atual: {driver.current_window_handle}")

    data = wait.until(EC.presence_of_element_located((By.NAME, "data")))

    driver.execute_script(f"arguments[0].value = '{data_ontem()}';", data)
    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Data inicial configurada para {data_ontem()}")
    
    time.sleep(2)

    # Exporta o CSV
    logging.info("📤 Exportando para CSV...")
    atalho_alt('v')  # Abre o menu Exportar / gera CSV

    time.sleep(15)

    if aceitar_alertas(driver):
        return "skip"
# Verifica se o botão do CSV aparece (sucesso do Alt+V)
    # Se não aparecer em 300s (5 min), assume falha e tenta clicar no visualizar manualmente
    try:
        # Tenta encontrar o botão CSV que indica que o relatório carregou
        logging.info("⏳ Aguardando processamento do relatório (Até 2 min)...")
        encontrar_imagem(CSV_BTN, timeout=120) 
    except TimeoutError:
        logging.error("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
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