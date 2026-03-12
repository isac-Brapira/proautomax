"""
Rotina: 05.12
Descrição: Baixa um CSV com relatório de vendas no ano em hectolitro com quebra de setor/cliente do Promax.
Autor: Carol
"""

import logging
import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.funcoes_rotina import aguardar_tela_carregar, atalho_alt
from function.img_func import encontrar_imagem, clicar_imagem, CSV_BTN, VISUALIZAR_BTN
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui


# Código da rotina no Promax
CODIGO_ROTINA = "0512"


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
    # Reseta a posição do mouse para o centro da tela para evitar FailSafe
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    logging.info("⚙️ Configurando parâmetros da rotina 05.12 em hectolitro ...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    logging.info(f"Janelas abertas: {driver.window_handles}")
    logging.info(f"Janela atual: {driver.current_window_handle}")
    
    #Selecionando selected box
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "opcaoRel")))

    driver.execute_script("arguments[0].value = '06'; arguments[0].onchange();", select_quebra1)

    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para Setor/Cliente (06)")
    time.sleep(0.5)

    #Selecionando checkbox
    checkbox = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[type='checkbox'][name='idConverteHecto'][value='S']")
        )
    )

    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)

    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Checkbox hectolitro selecionada")
    
    time.sleep(2)

    logging.info("📤 Executando Visualizar via JavaScript...")

    try:
        funcao_existe = driver.execute_script("return typeof Visualizar === 'function';")
        if not funcao_existe:
            logging.error("❌ Função Visualizar() não encontrada na página.")
            return "skip"            

        driver.execute_script("return Visualizar();")

    except Exception as e:
        logging.error(f"❌ Erro ao executar Visualizar(): {e}")
        return       

    try:
        logging.info("⏳ Aguardando processamento do relatório (até 2 min)...")
        encontrar_imagem(CSV_BTN, timeout=120)

    except TimeoutError:
        logging.warning("⚠️ Relatório demorou demais. Tentando novamente...")

        try:
            driver.execute_script("return Visualizar();")
            encontrar_imagem(CSV_BTN, timeout=180)
        except TimeoutError:
            logging.error("❌ Falha crítica: relatório não foi gerado.")
            return "skip"

    # # Exporta o CSV
    # logging.info("📤 Tentando usar o atalho Alt+V para visualizar...")
    # atalho_alt("v")
    # time.sleep(5)

    # try:
    #     # Tenta encontrar o botão CSV que indica que o relatório carregou
    #     logging.info("⏳ Aguardando processamento do relatório (Até 2 min)...")
    #     encontrar_imagem(CSV_BTN, timeout=120) 
    # except TimeoutError:
    #     logging.warning("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
    #     clicar_imagem(VISUALIZAR_BTN, timeout=10) # Tenta clicar no botão visualizar
        
    #     # Espera novamente pelo resultado
    #     logging.info("⏳ Aguardando processamento (2ª tentativa)...")
    #     try:
    #         encontrar_imagem(CSV_BTN, timeout=300)
    #     except TimeoutError:
    #         logging.error("❌ Falha crítica: Relatório não carregou.")
    #         return

    logging.info("⏳ Relatório gerado! Iniciando download...")

    # Clica no CSV para baixar
    time.sleep(2)
    clicar_imagem(CSV_BTN)

    logging.info("⏳ Aguardando download...")