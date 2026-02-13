"""
Rotina: 03.01.47.01
Descrição: Baixa um CSV com relatório de Apuração de CDP.
Autor: Carol
"""

import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.data_func import primeiro_dia_ano, primeiro_dia_mes
from function.img_func import CSV_BTN, VISUALIZAR_BTN, clicar_imagem, encontrar_imagem
from function.troca_janela import trocar_para_nova_janela
from function.funcoes_rotina import desmarcar_item, marcar_item, selecionar_selectedbox
import time
import pyautogui

# Código da rotina no Promax
CODIGO_ROTINA = "03014701"


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

    print("⚙️ Configurando parâmetros da rotina 03.01.47.01...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    # # parametros: wait, driver, name, value, quebra, label, CODIGO_ROTINA
    selecionar_selectedbox(wait, driver,"quebra1", "01", "Quebra 1", "Geral", CODIGO_ROTINA)

    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dataInicial")))

    driver.execute_script(f"arguments[0].value = '{primeiro_dia_mes()}';", data_inicial)
    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Data inicial configurada para {primeiro_dia_mes()}")

    time.sleep(1)

    print("📤 Tentando usar o atalho Alt+V para visualizar...")
    atalho_alt("V")

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

    time.sleep(2)


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