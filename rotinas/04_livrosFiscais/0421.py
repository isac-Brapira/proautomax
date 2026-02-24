"""
Rotina: 04.21
Descrição: Baixa um CSV com relatório de registro de inventário.
Autor: Carol
"""
import os
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.img_func import CSV_BTN, SALVAR_BTN_2, VISUALIZAR_BTN, clicar_imagem, encontrar_imagem
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui

# Código da rotina no Promax
CODIGO_ROTINA = "0421"


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

    print("⚙️ Configurando parâmetros da rotina 04.21...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    print("Janelas abertas:", driver.window_handles)
    print("Janela atual:", driver.current_window_handle)

    combo = driver.find_element("name", "opcaoCusto")

    driver.execute_script("""
        var select = arguments[0];
        select.value = "3";
        if (select.onchange) {
            select.onchange();
        }
    """, combo)
    print("⚙️ Selecionando opção de custo ...")

    checkbox_vasilhame = driver.find_element("name", "checkVasilhame")

    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_vasilhame)

    checkbox_garrafeira = driver.find_element("name", "checkGarrafeira")

    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_garrafeira)

    checkbox_material = driver.find_element("name", "checkMaterial")

    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_material)

    driver.execute_script("""
        document.getElementsByName('cdDeposito')[0].value = '01';
        AdicionaDeposito();
    """)

    print("📤 Tentando usar o atalho Alt+V para visualizar...")
    atalho_alt("v")

    # Verifica se o botão do CSV aparece (sucesso do Alt+V)
    # Se não aparecer em 300s (5 min), assume falha e tenta clicar no visualizar manualmente
    try:
        # Tenta encontrar o botão CSV que indica que o relatório carregou
        print("⏳ Aguardando processamento do relatório (Até 2 min)...")
        encontrar_imagem(SALVAR_BTN_2, timeout=120) 
    except TimeoutError:
        print("❌ Atalho Alt+V falhou ou demorou demais. Tentando clicar em Visualizar manualmente...")
        clicar_imagem(VISUALIZAR_BTN, timeout=10) # Tenta clicar no botão visualizar
        
        # Espera novamente pelo resultado
        print("⏳ Aguardando processamento (2ª tentativa)...")
        try:
            encontrar_imagem(SALVAR_BTN_2, timeout=300)
        except TimeoutError:
            print("❌ Falha crítica: Relatório não carregou.")
            return

    print("⏳ Relatório gerado! Iniciando download...")
    
    # Clica no botão salvar para baixar
    clicar_imagem(SALVAR_BTN_2)

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