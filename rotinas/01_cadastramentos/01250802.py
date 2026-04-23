"""
Rotina: 01.25.08.02 - Faixa de Preços
Descrição: Relatório de faixa de preços
Autor: Carol
"""

import logging

from function.abrir_rotinas import abrir_rotinas
from function.funcoes_rotina import aguardar_tela_carregar, atalho_alt
from function.troca_janela import trocar_para_nova_janela
from function.img_func import SALVAR_BTN, clicar_imagem, encontrar_imagem, CSV_BTN, VISUALIZAR_BTN
from function.ai_vision import ESTADOS, clicar_elemento_ia, aguardar_estado_ia, focar_janela_promax
from function.acoes import AGUARDAR_DOWNLOAD_SALVAR, CLICAR_DOWNLOAD_SALVAR, CLICAR_CSV, AGUARDAR_CSV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

# Código da rotina no Promax
CODIGO_ROTINA = "01250802"

def executar(driver, **kwargs):
    """
    Função principal da rotina.
    """
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    focar_janela_promax
    driver.maximize_window()
    
    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)
    time.sleep(5)
    
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    
    logging.info("⚙️ Configurando parâmetros da rotina 01.25.08.02...")
    
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
 
    time.sleep(2)
    
    # Testando clicar no botão visualizar com JavaScript
    logging.info("📤 Executando GeraPlanilha(); via JavaScript...")

    try:
        funcao_existe = driver.execute_script("return typeof GeraPlanilha === 'function';")
        if not funcao_existe:
            logging.error("❌ Função GeraPlanilha não encontrada na página.")
            return "skip"            

        driver.execute_script("return GeraPlanilha();")

    except Exception as e:
        logging.error(f"❌ Erro ao executar GeraPlanilha(): {e}")
        logging.info("Solicitando IA para clicar no botão CSV...")

        if not clicar_elemento_ia(**CLICAR_CSV):
            logging.error("❌ Falha ao clicar no botão CSV via IA.")
            return "skip"  

        logging.info("⏳ Aguardando relatório ser gerado após clique no CSV...")
    

    if not clicar_elemento_ia(**CLICAR_DOWNLOAD_SALVAR):
        logging.error("❌ Falha ao clicar no botão Salvar do download via IA.")
        return "skip"

    logging.info("⏳ Aguardando download...")
    time.sleep(5)