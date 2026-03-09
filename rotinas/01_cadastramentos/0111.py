"""
Rotina: 01.11 - Produtos
Descrição: Baixa um CSV com os produtos cadastrados no Promax.
Autor: Isac
"""
import logging
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.funcoes_rotina import aguardar_tela_carregar, atalho_alt
from function.img_func import encontrar_imagem, clicar_imagem, CSV_BTN_2, SALVAR_BTN
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui


# Código da rotina no Promax
CODIGO_ROTINA = "0111"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    Tudo começa por aqui.
    """
    abrir_rotinas(driver, CODIGO_ROTINA)

    logging.info(f"Janelas abertas: {driver.window_handles}")
    logging.info(f"Janela atual: {driver.current_window_handle}")

    trocar_para_nova_janela(driver)

    logging.info(f"Janela depois da troca: {driver.current_window_handle}")

    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    aguardar_tela_carregar(wait)

    time.sleep(2)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    time.sleep(2)

    # Tenta usar o atalho Alt+V para abrir o menu Exportar / gera CSV
    atalho_alt('v')
    logging.info("Tentando usar o atalho Alt+V para abrir o menu Exportar / gera CSV...")
 
    
    try:
        # Tenta encontrar o botão CSV que indica que o relatório carregou
        logging.info("⏳ Aguardando processamento do relatório (Até 2 min)...")
        encontrar_imagem(SALVAR_BTN, timeout=120) 
    except TimeoutError:
        logging.error("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
        clicar_imagem(CSV_BTN_2, timeout=10) # Tenta clicar no botão visualizar que neste caso o botão de visualizar chama Csv
        
        # Espera novamente pelo resultado
        logging.warning("⏳ Aguardando processamento (2ª tentativa)...")
        try:
            encontrar_imagem(SALVAR_BTN, timeout=300)
        except TimeoutError:
            logging.error("❌ Falha crítica: Relatório não carregou.")
            return

    logging.info("⏳ Relatório gerado! Iniciando download...")

    # Espera a barra de download aparecer
    logging.info("⏳ Aguardando barra de download...")
    time.sleep(5)  # Tempo para a barra aparecer

    # Aqui o executor.py vai chamar confirmar_download_com_retry()
    # que usa o sistema de estratégias automaticamente