"""
Rotina: 01.05.07.04.02 - Cliente Plus
Descrição: Baixa um CSV com os clientes cadastrados no Promax.
Autor: Isac
"""

import logging

from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.ai_vision import ESTADOS, aguardar_estado_ia, clicar_elemento_ia, focar_janela_promax
from function.acoes import AGUARDAR_TODOS_0105070402, AGUARDAR_CSV_GERADO_0105070402, CLICAR_TODOS_0105070402, CLICAR_GERAR_CSV_0105070402, CLICAR_AS_0105070402, CLICAR_OK_CSV_GERADO_0105070402, CLICAR_DUPLICADOS_0105070402
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
import time
import pyautogui

    # ======================= Acessando a rotina e focando a janela ======================== #


# Código da rotina no Promax
CODIGO_ROTINA = "0105070402"


def executar(driver, **kwargs):

    focar_janela_promax()
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)
    aguardar_tela_carregar(wait)

    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    # Aguarda o formulário com os checkboxes aparecer
    try:
        analise = aguardar_estado_ia(
            **AGUARDAR_TODOS_0105070402,
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando formulário de filtros",
        )
        if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
            return "skip"
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando formulário na rotina {CODIGO_ROTINA}")
        return "skip"

    # Clica nos checkboxes e no botão em sequência
    logging.info("🔘 Interagindo com o formulário de filtros...")
    logging.info(" Clicando no checkbox 'Todos'")
    if not clicar_elemento_ia(**CLICAR_TODOS_0105070402):
        logging.warning("⚠️ Não consegui clicar em 'Todos'")
        return "skip"

    logging.info(" Clicando no checkbox 'Duplicados'")
    if not clicar_elemento_ia(**CLICAR_DUPLICADOS_0105070402):
        logging.warning("⚠️ Não consegui clicar em 'Duplicados'")
        return "skip"

    logging.info(" Clicando no checkbox 'AS'")
    if not clicar_elemento_ia(**CLICAR_AS_0105070402):
        logging.warning("⚠️ Não consegui clicar em 'AS'")
        return "skip"

    logging.info(" Clicando no botão 'Gerar CSV'")
    if not clicar_elemento_ia(**CLICAR_GERAR_CSV_0105070402):
        logging.warning("⚠️ Não consegui clicar em 'Gerar CSV'")
        return "skip"

    # Aguarda o popup "CSV gerado com Sucesso!"
    try:
        analise = aguardar_estado_ia(
            **AGUARDAR_CSV_GERADO_0105070402,
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando popup de confirmação",
        )
        if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
            return "skip"
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando popup de confirmação na rotina {CODIGO_ROTINA}")
        return "skip"

    # Clica em OK no popup
    if not clicar_elemento_ia(**CLICAR_OK_CSV_GERADO_0105070402):
        logging.warning("⚠️ Não consegui clicar em OK")
        return "skip"

    logging.info("⏳ Aguardando barra de download...")
    # executor.py chama salvar_arquivo() após o retorno