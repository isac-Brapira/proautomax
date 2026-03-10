
import time

import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def desmarcar_item(tipoInput, wait, driver, name, value, descricao, CODIGO_ROTINA):
    item = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input[type='{tipoInput}'][name='{name}'][value='{value}']")
        )
    )

    if item.is_selected():
        driver.execute_script("arguments[0].click();", item)
        print(f"ROTINA {CODIGO_ROTINA}:⚙️ {tipoInput} de {descricao} desmarcado...")

def marcar_item(tipoInput, wait, driver, name, value, descricao, CODIGO_ROTINA):
    item = wait.until(
        EC.presence_of_element_located(
             (By.CSS_SELECTOR, f"input[type='{tipoInput}'][name='{name}'][value='{value}']")
        )
    )

    if not item.is_selected():
        driver.execute_script("arguments[0].click();", item)
        print(f"ROTINA {CODIGO_ROTINA}:⚙️ {tipoInput} de {descricao} marcado...")

def selecionar_selectedbox(wait, driver, name, value, quebra, label, CODIGO_ROTINA):
    select = wait.until(EC.presence_of_element_located((By.NAME, name)))

    driver.execute_script(f"arguments[0].value = '{value}'; arguments[0].onchange();", select)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ A quebra {quebra} foi configurada para {label}")

def aguardar_tela_carregar(wait):
    """
    Garante que a tela da rotina abriu.
    Ajuste o elemento para cada rotina.
    """
    wait.until(EC.invisibility_of_element_located((By.ID, "imgWait")))


def atalho_alt(tecla):
    """Helper para atalhos Alt+Tecla"""
    time.sleep(0.5)
    pyautogui.keyDown('alt')
    time.sleep(0.25)
    pyautogui.press(tecla.lower())
    time.sleep(0.25)
    pyautogui.keyUp('alt')