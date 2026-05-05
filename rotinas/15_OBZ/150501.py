"""
Rotina: 15.05.01 - Lançamentos detalhados OBZ
Descrição: Relatório de lançamentos do OBZ.
Autor: Carol
"""

import logging
import pyautogui
from function.abrir_rotinas import abrir_rotinas
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
from function.ai_vision import ESTADOS, aguardar_estado_ia, clicar_elemento_ia, focar_janela_promax
from function.acoes import AGUARDAR_CSV, CLICAR_CSV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from function.data_func import ano_vigente

CODIGO_ROTINA = "150501"


def executar(driver, **kwargs):

    focar_janela_promax()
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    logging.info("⚙️ Configurando parâmetros da rotina 15.05.01...")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))

    # Período = Anual (A)
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "idPeriodo")))
    driver.execute_script("arguments[0].value = 'A'; arguments[0].onchange();", select_quebra1)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Período configurado para Anual (A)")

    # Ano vigente
    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dtAno")))
    driver.execute_script(f"arguments[0].value = '{ano_vigente()}';", data_inicial)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Ano configurado para {ano_vigente()}")

    # NBZ = 99 - Todos
    select_nbz = Select(wait.until(EC.presence_of_element_located((By.NAME, "cdNbz"))))
    select_nbz.select_by_value("99")
    driver.execute_script("AdicionaNbz();")
    lista = driver.find_element(By.NAME, "cdNbzLista")
    if lista.find_elements(By.TAG_NAME, "option"):
        logging.info("NBZ adicionada com sucesso")
    time.sleep(1)

    # Depto = 9999 - Todos
    select_depto = Select(wait.until(EC.presence_of_element_located((By.NAME, "cdDepto"))))
    select_depto.select_by_value("9999")
    driver.execute_script("AdicionaDepto();")
    lista = driver.find_element(By.NAME, "cdDeptoLista")
    if lista.find_elements(By.TAG_NAME, "option"):
        logging.info("Depto adicionada com sucesso")
    time.sleep(1)

    # Pacote = 9999 - Todos
    select_pacote = Select(wait.until(EC.presence_of_element_located((By.NAME, "cdPacote"))))
    select_pacote.select_by_value("9999")
    driver.execute_script("AdicionaPacote();")
    lista = driver.find_element(By.NAME, "cdPacoteLista")
    if lista.find_elements(By.TAG_NAME, "option"):
        logging.info("Pacote adicionado com sucesso")
    else:
        logging.warning("Pacote não foi adicionado")
    time.sleep(1)

    # VBZ = 9999 - Todos
    select_vbz = Select(wait.until(EC.presence_of_element_located((By.NAME, "cdVbz"))))
    select_vbz.select_by_value("9999")
    driver.execute_script("AdicionaVbz();")
    lista = driver.find_element(By.NAME, "cdVbzLista")
    if lista.find_elements(By.TAG_NAME, "option"):
        logging.info("VBZ adicionada com sucesso")
    else:
        logging.warning("VBZ não foi adicionada")
    time.sleep(1)

    # Conta = 9999999999 - Todos
    select_conta = Select(wait.until(EC.presence_of_element_located((By.NAME, "cdConta"))))
    select_conta.select_by_value("9999999999")
    driver.execute_script("AdicionaConta();")
    lista = driver.find_element(By.NAME, "cdContaLista")
    if lista.find_elements(By.TAG_NAME, "option"):
        logging.info("Conta adicionada com sucesso")
    else:
        logging.warning("Conta não foi adicionada")
    time.sleep(1)

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

    try:
        analise = aguardar_estado_ia(
            estados_esperados=["csv_disponivel", "sem_dados", "erro"],
            timeout=300,
            intervalo=4,
            pergunta=AGUARDAR_CSV["pergunta"],
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando relatório de lançamentos OBZ",
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
