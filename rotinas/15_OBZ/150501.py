"""
Rotina: 15.05.01 - Lançamentos detalhados OBZ
Descrição: Relatório de lançamentos do OBZ
Autor: Carol
"""

from function.abrir_rotinas import abrir_rotinas
from function.troca_janela import trocar_para_nova_janela
from function.img_func import clicar_imagem, encontrar_imagem, CSV_BTN, SALVAR_BTN, VISUALIZAR_BTN
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pyautogui
from function.data_func import ano_vigente, data_hoje, data_ontem, primeiro_dia_mes

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
    _aguardar_tela_carregar(wait)
    time.sleep(5)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    print("⚙️ Configurando parâmetros da rotina 150501...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    # -------------------------
    # Quebra 1 = Período (A)
    # -------------------------
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "idPeriodo")))

    driver.execute_script("arguments[0].value = 'A'; arguments[0].onchange();", select_quebra1)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para Período Anual (A)")

    # -------------------------
    # Data = Ano vigente
    # -------------------------   

    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dtAno")))

    driver.execute_script(f"arguments[0].value = '{ano_vigente()}';", data_inicial)
    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Ano configurado para {ano_vigente()}")

    # CLICAR NO BOTÃO DE NBZ
    while True:
        try:
            pos = pyautogui.locateOnScreen("images/nbz.png", confidence= 0.8)
            if pos:
                print("✅ Clicando no botão de NBZ...")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pos.left + pos.width - 10, pos.top + pos.height // 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    # CLICAR NO BOTÃO DE DEPTO
    while True:
        try:
            pos = pyautogui.locateOnScreen("images/depto.png", confidence= 0.8)
            if pos:
                print("✅ Clicando no botão de DEPTO...")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pos.left + pos.width - 10, pos.top + pos.height // 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    # CLICAR NO BOTÃO DE PACOTE
    while True:
        try:
            pos = pyautogui.locateOnScreen("images/pacote.png", confidence= 0.8)
            if pos:
                print("✅ Clicando no botão de PACOTE...")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pos.left + pos.width - 10, pos.top + pos.height // 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    # CLICAR NO BOTÃO DE VBZ
    while True:
        try:
            pos = pyautogui.locateOnScreen("images/vbz.png", confidence= 0.8)
            if pos:
                print("✅ Clicando no botão de VBZ...")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pos.left + pos.width - 10, pos.top + pos.height // 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    # CLICAR NO BOTÃO DE CONTA
    while True:
        try:
            pos = pyautogui.locateOnScreen("images/conta.png", confidence= 0.8)
            if pos:
                print("✅ Clicando no botão de CONTA...")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pos.left + pos.width - 10, pos.top + pos.height // 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    time.sleep(1)

    print("📤 Tentando usar o atalho Alt+V para visualizar...")
    atalho_alt("v")

    # Verifica se o botão do CSV aparece (sucesso do Alt+V)
    # Se não aparecer em 300s (5 min), assume falha e tenta clicar no visualizar manualmente
    try:
        # Tenta encontrar o botão CSV que indica que o relatório carregou
        print("⏳ Aguardando processamento do relatório (Até 2 min)...")
        encontrar_imagem(CSV_BTN, timeout=120) 
    except TimeoutError:
        print("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
        clicar_imagem(VISUALIZAR_BTN, timeout=10) # Tenta clicar no botão visualizar
        
        # Espera novamente pelo resultado
        print("⏳ Aguardando processamento (2ª tentativa)...")
        try:
            encontrar_imagem(CSV_BTN, timeout=300)
        except TimeoutError:
            print("❌ Falha crítica: Relatório não carregou.")
            return

    print("⏳ Relatório gerado! Iniciando download...")

    # Clica no CSV para baixar
    clicar_imagem(CSV_BTN)
    

    print("⏳ Aguardando download...")

    time.sleep(2)

# ========================
# Funções auxiliares
# ========================

def _aguardar_tela_carregar(wait):
    """
    Aguarda o loading da rotina desaparecer.
    """
    wait.until(EC.invisibility_of_element_located((By.ID, "imgWait")))


def atalho_alt(tecla):
    """
    Helper para atalhos Alt+Tecla
    """
    time.sleep(0.5)
    pyautogui.keyDown("alt")
    pyautogui.press(tecla.lower())
    pyautogui.keyUp("alt")