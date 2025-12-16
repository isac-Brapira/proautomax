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

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print("iframes encontrados:", len(iframes))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    trocar_para_nova_janela(driver)

    print("Janela depois da troca:", driver.current_window_handle)


    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    _aguardar_tela_carregar(wait)

    time.sleep(2)

    atalho_alt('v')  # Abre o menu Exportar




# ========================
# Funções auxiliares
# ========================

def scroll_ate_elemento(driver, elemento):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        elemento
    )

def _aguardar_tela_carregar(wait):
    """
    Garante que a tela da rotina abriu.
    Ajuste o elemento para cada rotina.
    """
    wait.until(EC.invisibility_of_element_located((By.ID, "imgWait")))


def atalho_alt(tecla):
    time.sleep(0.5)
    pyautogui.keyDown('alt')
    pyautogui.press(tecla.lower())
    pyautogui.keyUp('alt')


