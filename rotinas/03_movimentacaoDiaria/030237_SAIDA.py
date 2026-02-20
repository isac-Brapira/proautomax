"""
Rotina: 03.02.37 - Rel. Notas Fiscais Plus
Descrição: Relatório de notas fiscais de SAIDA com quebra por Operação e Vendedor.
Autor: Carol e Isac
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
from function.data_func import data_hoje, data_ontem, primeiro_dia_mes



# Código da rotina no Promax
CODIGO_ROTINA = "030237"

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
    

    print("⚙️ Configurando parâmetros da rotina 030237...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    # -------------------------
    # Quebra 1 = Operação (14)
    # -------------------------
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "quebra1")))

    driver.execute_script("arguments[0].value = '14'; arguments[0].onchange();", select_quebra1)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 1 configurada para Operação (14)")

    # -------------------------
    # Quebra 2 = Vendedor (06)
    # -------------------------
    select_quebra2 = wait.until(EC.presence_of_element_located((By.NAME, "quebra2")))

    driver.execute_script("arguments[0].value = '06'; arguments[0].onchange();", select_quebra2)

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Quebra 2 configurada para Vendedor (06)")

    # -------------------------
    # Itens = Sim
    # -------------------------
    radio_itens = wait.until(

      EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][name='itens'][value='S']"))

    )

    if not radio_itens.is_selected():

      radio_itens.click()

    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Itens configurados para Sim")

    # -------------------------
    # Data inicial = primeiro dia do mês atual
    # Data final = hoje
    # -------------------------   

    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dataInicial")))

    driver.execute_script(f"arguments[0].value = '{primeiro_dia_mes()}';", data_inicial)
    print(f"ROTINA {CODIGO_ROTINA}:⚙️ Data inicial configurada para {primeiro_dia_mes()}")

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

    #clicar_imagem("images/csv_carol.png")

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