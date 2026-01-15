"""
Rotina: 03.02.37 - Rel. Notas Fiscais Plus
Descrição: Relatório com quebra por Operação e Vendedor.
Autor: Isac
"""

from function.abrir_rotinas import abrir_rotinas
from function.troca_janela import trocar_para_nova_janela
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pyautogui


# Código da rotina no Promax
CODIGO_ROTINA = "030237"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    """

    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 30)
    _aguardar_tela_carregar(wait)

    print("⚙️ Configurando parâmetros da rotina 030237...")

    # -------------------------
    # Quebra 1 = Operação (14)
    # -------------------------
    quebra1 = Select(wait.until(
        EC.presence_of_element_located((By.NAME, "quebra1"))
    ))
    quebra1.select_by_value("14")
    time.sleep(1)

    # -------------------------
    # Quebra 2 = Vendedor (06)
    # -------------------------
    quebra2 = Select(wait.until(
        EC.presence_of_element_located((By.NAME, "quebra2"))
    ))
    quebra2.select_by_value("06")
    time.sleep(1)

    # -------------------------
    # Itens = Sim
    # -------------------------
    itens_sim = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='itens' and @value='S']"))
    )
    driver.execute_script("arguments[0].click();", itens_sim)

    # -------------------------
    # Data inicial = primeiro dia do mês atual
    # Data final = hoje
    # -------------------------
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1)

    data_ini = primeiro_dia.strftime("%d/%m/%Y")
    data_fim = hoje.strftime("%d/%m/%Y")

    campo_data_ini = wait.until(
        EC.presence_of_element_located((By.NAME, "dataInicial"))
    )
    campo_data_fim = wait.until(
        EC.presence_of_element_located((By.NAME, "dataFinal"))
    )

    campo_data_ini.clear()
    campo_data_ini.send_keys(data_ini)

    campo_data_fim.clear()
    campo_data_fim.send_keys(data_fim)

    time.sleep(1)

    print("📤 Exportando CSV...")
    atalho_alt("v")

    print("⏳ Aguardando download...")


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
