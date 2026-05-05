"""
Rotina: 03.02.37 - Rel. Notas Fiscais Plus
Descrição: Relatório de notas fiscais de ENTRADA com quebra por Operação e código fiscal.
Autor: Carol e Isac
"""

import logging
import pyautogui
from function.abrir_rotinas import abrir_rotinas
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
from function.ai_vision import ESTADOS, focar_janela_promax, clicar_elemento_ia, aguardar_estado_ia
from function.acoes import AGUARDAR_CSV, CLICAR_CSV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.data_func import primeiro_dia_mes

CODIGO_ROTINA = "030237_ENTRADA"


def executar(driver, **kwargs):

    focar_janela_promax()
    abrir_rotinas(driver, '030237')
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    logging.info("⚙️ Configurando parâmetros da rotina 03.02.37 de entrada...")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))

    # Quebra 1 = Operação (14)
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "quebra1")))
    driver.execute_script("arguments[0].value = '14'; arguments[0].onchange();", select_quebra1)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Quebra 1 configurada para Operação (14)")

    # Quebra 2 = Código Fiscal (29)
    select_quebra2 = wait.until(EC.presence_of_element_located((By.NAME, "quebra2")))
    driver.execute_script("arguments[0].value = '29'; arguments[0].onchange();", select_quebra2)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Quebra 2 configurada para Código Fiscal (29)")

    # Itens = Sim
    radio_itens = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][name='itens'][value='S']"))
    )
    if not radio_itens.is_selected():
        radio_itens.click()
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Itens configurados para Sim")

    # Notas = Entrada
    radio_entrada = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][name='notas'][value='NE']"))
    )
    if not radio_entrada.is_selected():
        radio_entrada.click()
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Notas configuradas para Entrada")

    # Checkbox Lista NFs de Compra
    checkbox = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'][name='listaNotaCompra'][value='S']"))
    )
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Checkbox de Lista NFs de Compra flagada")

    # Data inicial = primeiro dia do mês
    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dataInicial")))
    driver.execute_script(f"arguments[0].value = '{primeiro_dia_mes()}';", data_inicial)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Data inicial configurada para {primeiro_dia_mes()}")

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

    logging.info("⏳ Aguardando processamento do relatório (até 10 min)...")
    try:
        analise = aguardar_estado_ia(
            estados_esperados=["csv_disponivel", "sem_dados", "erro"],
            timeout=600,
            intervalo=15,
            pergunta=AGUARDAR_CSV["pergunta"],
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando relatório de notas fiscais de entrada",
            descricao_adicional=(
                "O relatório foi disparado e pode aparecer um dialog de 'Processando...' "
                "durante a geração — isso é normal e NÃO é um erro, apenas aguarde. "
                "Só retorne csv_disponivel quando o botão CSV aparecer na toolbar."
            )
        )
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando relatório na rotina {CODIGO_ROTINA}")
        return "skip"

    if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
        logging.warning(f"⏭️ {analise.get('mensagem')} — pulando")
        return "skip"

    logging.info("✅ Relatório gerado! Clicando no CSV...")
    if not clicar_elemento_ia(**CLICAR_CSV):
        logging.error("❌ Falha ao clicar no CSV")
        return "skip"

    logging.info("⏳ Aguardando download...")
