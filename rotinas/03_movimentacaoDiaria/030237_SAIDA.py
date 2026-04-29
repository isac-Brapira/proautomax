"""
Rotina: 03.02.37 - Rel. Notas Fiscais Plus
Descrição: Relatório de notas fiscais de SAIDA com quebra por Operação e Vendedor.
Autor: Carol e Isac
"""

import logging
from function.abrir_rotinas import abrir_rotinas
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
from function.ai_vision import ESTADOS, focar_janela_promax, clicar_elemento_ia, aguardar_estado_ia
from function.acoes import AGUARDAR_CSV, CLICAR_CSV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from function.data_func import primeiro_dia_mes

# Código da rotina no Promax
CODIGO_ROTINA = "030237_SAIDA"


def executar(driver, **kwargs):
    """
    Função principal da rotina.
    """

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

    logging.info("⚙️ Configurando parâmetros da rotina 03.02.37 de saída...")

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))

    # Quebra 1 = Operação (14)
    select_quebra1 = wait.until(EC.presence_of_element_located((By.NAME, "quebra1")))
    driver.execute_script("arguments[0].value = '14'; arguments[0].onchange();", select_quebra1)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Quebra 1 configurada para Operação (14)")

    # Quebra 2 = Vendedor (06)
    select_quebra2 = wait.until(EC.presence_of_element_located((By.NAME, "quebra2")))
    driver.execute_script("arguments[0].value = '06'; arguments[0].onchange();", select_quebra2)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Quebra 2 configurada para Vendedor (06)")

    # Itens = Sim
    radio_itens = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][name='itens'][value='S']"))
    )
    if not radio_itens.is_selected():
        radio_itens.click()
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Itens configurados para Sim")

    # Data inicial = primeiro dia do mês atual
    data_inicial = wait.until(EC.presence_of_element_located((By.NAME, "dataInicial")))
    driver.execute_script(f"arguments[0].value = '{primeiro_dia_mes()}';", data_inicial)
    logging.info(f"ROTINA {CODIGO_ROTINA}: ⚙️ Data inicial configurada para {primeiro_dia_mes()}")

    # Executa o Visualizar
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

    # IA aguarda o CSV — alertas durante o processamento são fechados automaticamente
    # pelo loop interno do aguardar_estado_ia, sem interromper a espera
    logging.info("⏳ Aguardando processamento do relatório (até 10 min)...")
    try:
        analise = aguardar_estado_ia(
            estados_esperados=["csv_disponivel", "sem_dados", "erro"],
            timeout=600,
            intervalo=15,
            pergunta=AGUARDAR_CSV["pergunta"],
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando processamento do relatório",
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

    # Clica no CSV
    logging.info("✅ Relatório gerado! Clicando no CSV...")
    if not clicar_elemento_ia(**CLICAR_CSV):
        logging.error("❌ Falha ao clicar no botão CSV")
        return "skip"

    logging.info("⏳ Aguardando download...")
    # executor.py chama salvar_arquivo() após o retorno