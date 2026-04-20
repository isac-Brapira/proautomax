"""
Rotina: 01.20.11
Descrição: Baixa um CSV com relatório de Visitas do vendedor
Autor: Carol
"""

import logging
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.funcoes_rotina import aguardar_tela_carregar
from function.ai_vision import ESTADOS, aguardar_estado_ia, clicar_elemento_ia, focar_janela_promax
from function.acoes import CLICAR_CSV, AGUARDAR_CSV
from function.troca_janela import trocar_para_nova_janela
import pyautogui


# Código da rotina no Promax
CODIGO_ROTINA = "012011"


def executar(driver, **kwargs):
    """
    Função principal da rotina.    
    """

    focar_janela_promax()  # garante que o Promax está em foco antes de interagir
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True
    

    logging.info("⚙️ Configurando parâmetros da rotina 01.20.11...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))

    # Não me pergunte o porque, é o promax...
    driver.execute_script("""
        var sel = document.getElementsByName('grPerfilVenda')[0];
        if (sel) {
            sel.value = '05';
            sel.fireEvent('onchange');
        }
    """)

    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Grupo perfil de vendas configurado para 05 - Segmentada")

    driver.execute_script("""
        var cb = document.getElementsByName('todos')[0];
        if (cb && !cb.checked) {
            cb.checked = true;
            cb.fireEvent('onclick');
        }
    """)

    logging.info(f"ROTINA {CODIGO_ROTINA}:⚙️ Checkbox de situação Todos marcada...")

    # Testando clicar no botão visualizar com JavaScript ==============================================================
    logging.info("📤 Executando Visualizar via JavaScript...")

    try:
        funcao_existe = driver.execute_script("return typeof Visualizar === 'function';")
        if not funcao_existe:
            logging.error("❌ Função Visualizar() não encontrada na página.")
            return "skip"            

        driver.execute_script("return Visualizar();")

    except Exception as e:
        logging.error(f"❌ Erro ao executar Visualizar(): {e}")
        return "skip"        
    # ===========================================================================

    try:
        logging.info("⏳ Aguardando processamento do relatório (até 2 min)...")
        analise = aguardar_estado_ia(
            **AGUARDAR_CSV,
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando processamento do relatório", 
        )

        if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
            logging.warning(f"⏭️  Rotina '{CODIGO_ROTINA}' pulada (IA detectou estado {analise.get('mensagem')})\n")

            return "skip"
    except TimeoutError:
        logging.warning(f"❌ Timeout aguardando download na rotina {CODIGO_ROTINA}")
        return "skip"

    
    logging.info("⏳ Relatório gerado! Iniciando download...")

    # Clica no CSV para baixar
    if not clicar_elemento_ia(**CLICAR_CSV):
        logging.error(f"❌ Falha ao clicar para baixar CSV na rotina {CODIGO_ROTINA}")
        return "skip"
    
    logging.info("⏳ Aguardando download...")