"""
Rotina: 01.11 - Produtos
Descrição: Baixa um CSV com os produtos cadastrados no Promax.
Autor: Isac
"""

from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Código da rotina no Promax
CODIGO_ROTINA = "0111"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    Tudo começa por aqui.
    """

    abrir_rotinas(driver, CODIGO_ROTINA)

    wait = WebDriverWait(driver, 20)

    _aguardar_tela_carregar(wait)

    # --- AÇÕES DA ROTINA ---
    # exemplo:
    # _preencher_campos(driver, wait, kwargs)
    # _confirmar(driver, wait)


# ========================
# Funções auxiliares
# ========================

def _aguardar_tela_carregar(wait):
    """
    Garante que a tela da rotina abriu.
    Ajuste o elemento para cada rotina.
    """
    wait.until(
        EC.presence_of_element_located((By.ID, "FormPrincipal"))
    )


def _preencher_campos(driver, wait, data):
    pass


def _confirmar(driver, wait):
    pass
