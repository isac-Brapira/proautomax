"""
Rotina: 01.05.07.04.02 - Cliente Plus
Descrição: Baixa um CSV com os clientes cadastrados no Promax.
Autor: Isac
"""

from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui

    # ======================= Acessando a rotina e focando a janela ======================== #


# Código da rotina no Promax
CODIGO_ROTINA = "0105070402"


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
    
    # =========================== Navegação dentro da rotina =============================== #

    while True:
        try:
            pos = pyautogui.locateOnScreen("images/0105070402_images/Todos.png", confidence= 0.8)
            if pos:
                print("✅ Marcando checkbox TODOS...")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pyautogui.center(pos))
                # Clica bem no começo da imagem para conseguir dar o tab
                # pyautogui.click(pos.left + 2, pos.top + 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    while True:
        try:
            pos = pyautogui.locateOnScreen("images/0105070402_images/Duplicados.png", confidence= 0.8)
            if pos:
                print("✅ Marcando checkbox Duplicados...")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                pyautogui.click(pyautogui.center(pos))
                # Clica bem no começo da imagem para conseguir dar o tab
                # pyautogui.click(pos.left + 2, pos.top + 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu        

    while True:
        try:
            pos = pyautogui.locateOnScreen("images/0105070402_images/AS.png", confidence= 0.8)
            if pos:
                print("✅ Marcando o checkbox AS...")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                # Clica no lado esquerdo da imagem (onde deve estar o checkbox)
                pyautogui.click(pos.left + 10, pos.top + pos.height / 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    while True:
        try:
            pos = pyautogui.locateOnScreen("images/0105070402_images/Gerar_CSV.png", confidence= 0.8)
            if pos:
                print("✅ Gerando CSV...")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(1)
                # Clica no lado esquerdo da imagem (onde deve estar o checkbox)
                pyautogui.click(pos.left + 10, pos.top + pos.height / 2)
                
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    while True:
        try:
            pos = pyautogui.locateOnScreen("images/0105070402_images/CSV_gerado.png", confidence= 0.8)
            if pos:
                print("✅ CSV Gerado!")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                time.sleep(2)
                # Clica no lado esquerdo da imagem (onde deve estar o checkbox)
                pyautogui.keyDown("enter")
                pyautogui.keyUp("enter")
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu   


    time.sleep(2)
    # Garante que a janela principal esteja em foco novamente
    try:
        driver.switch_to.window(driver.current_window_handle)
    except Exception:
        pass
    
    # Clica no centro da tela para garantir o foco no sistema operacional
    screen_w, screen_h = pyautogui.size()
    pyautogui.click(screen_w / 2, screen_h / 2)
    # =========================== Exportando para CSV ===================================== #

   



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