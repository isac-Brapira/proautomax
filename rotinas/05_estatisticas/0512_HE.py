"""
Rotina: 05.12
Descrição: Baixa um CSV com relatório de vendas no ano em hectolitro com quebra de setor/cliente do Promax.
Autor: Carol
"""

import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    _aguardar_tela_carregar(wait)
    time.sleep(5)
    # Reseta a posição do mouse para o centro da tela para evitar FailSafe
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    print("⚙️ Configurando parâmetros da rotina 0512 em hectolitro ...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)
    
    #Selecionando selected box
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "opcaoRel")))

    driver.execute_script("arguments[0].value = '01'; arguments[0].onchange();", select_quebra1)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para Setor/Cliente (06)")

    #Selecionando checkbox
    checkbox = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[type='checkbox'][name='idConverteHecto'][value='S']")
        )
    )

    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Checkbox selecionada")

    # Exporta o CSV
    print("📤 Clicando em visualizar...")
    atalho_alt('v')  # Abre o menu Exportar / gera CSV
    
    time.sleep(1)

    # Espera a barra de download aparecer
    print("⏳ Aguardando download...")
    
    while True:
        try:
            pos = pyautogui.locateOnScreen(os.getenv("PATH_IMAGE_CSV"), confidence= 0.8)
            if pos:
                print("✅ Botão encontrado!")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(2)
                pyautogui.click(pyautogui.center(pos))

                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

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