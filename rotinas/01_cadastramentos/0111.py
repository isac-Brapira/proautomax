"""
Rotina: 01.11 - Produtos
Descrição: Baixa um CSV com os produtos cadastrados no Promax.
Autor: Isac
"""

from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    trocar_para_nova_janela(driver)

    print("Janela depois da troca:", driver.current_window_handle)

    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    _aguardar_tela_carregar(wait)

    time.sleep(2)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    # Exporta o CSV
    print("📤 Exportando para CSV...")
    atalho_alt('v')  # Abre o menu Exportar / gera CSV

    # Espera a barra de download aparecer
    print("⏳ Aguardando barra de download...")
    time.sleep(5)  # Tempo para a barra aparecer

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