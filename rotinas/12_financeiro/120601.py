"""
Rotina: 12.06.01 - Títulos Pendentes
Descrição: Baixa um CSV com os títulos em atraso do Promax.
Autor: Carol e Isac
"""

from datetime import datetime, timedelta
import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.img_func import encontrar_imagem, clicar_imagem, CSV_BTN, VISUALIZAR_BTN
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui
from function.data_func import data_ontem

# Código da rotina no Promax
CODIGO_ROTINA = "120601"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    Tudo começa por aqui.
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
    

    print("⚙️ Configurando parâmetros da rotina 120601...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    #TODO
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "opcaoRel")))

    driver.execute_script("arguments[0].value = '01'; arguments[0].onchange();", select_quebra1)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para classificação numérica")

    vencimento_final = wait.until(EC.presence_of_element_located((By.NAME, "fimVencimento")))

    driver.execute_script(f"arguments[0].value = '{data_ontem()}';", vencimento_final)
    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Data inicial configurada para {data_ontem()}")

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
    time.sleep(2)
    clicar_imagem(CSV_BTN)



    time.sleep(2)

    # Aqui o executor.py vai chamar confirmar_download_com_retry()
    # que usa o sistema de estratégias automaticamente


# ========================
# Funções auxiliares
# ========================

def _aguardar_tela_carregar(wait):
    """
    Garante que a tela da rotina abriu.
    Ajuste o elemento para cada rotina.
    """
    wait.until(EC.invisibility_of_element_located((By.ID, "imgWait")))


def atalho_alt(tecla):
    """Helper para atalhos Alt+Tecla"""
    time.sleep(0.5)
    pyautogui.keyDown('alt')
    pyautogui.press(tecla.lower())
    pyautogui.keyUp('alt')