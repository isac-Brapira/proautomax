"""
Rotina: 04.21
Descrição: Baixa um CSV com relatório de registro de inventário.
Autor: Carol
"""

import logging
import pyautogui
from function.abrir_rotinas import abrir_rotinas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function.funcoes_rotina import aguardar_tela_carregar
from function.ai_vision import ESTADOS, aguardar_estado_ia, clicar_elemento_ia, focar_janela_promax
from function.acoes import AGUARDAR_SALVAR_BOTAO_PAGINA, CLICAR_SALVAR_BOTAO_PAGINA
from function.troca_janela import trocar_para_nova_janela

CODIGO_ROTINA = "0421"


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

    logging.info("⚙️ Configurando parâmetros da rotina 04.21...")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))

    # Opção de custo = Preço médio de reposição (3)
    combo = driver.find_element("name", "opcaoCusto")
    driver.execute_script("""
        var select = arguments[0];
        select.value = "3";
        if (select.onchange) { select.onchange(); }
    """, combo)
    logging.info("⚙️ Selecionando opção de preço médio de reposição...")

    # Remove flag Vasilhame
    checkbox_vasilhame = driver.find_element("name", "checkVasilhame")
    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_vasilhame)
    logging.info("⚙️ Removendo flag de Vasilhame...")

    # Remove flag Garrafeira
    checkbox_garrafeira = driver.find_element("name", "checkGarrafeira")
    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_garrafeira)
    logging.info("⚙️ Removendo flag de Garrafeira...")

    # Remove flag Material
    checkbox_material = driver.find_element("name", "checkMaterial")
    driver.execute_script("""
        var cb = arguments[0];
        cb.checked = false;
        if (cb.onclick) cb.onclick();
        if (cb.onchange) cb.onchange();
    """, checkbox_material)
    logging.info("⚙️ Removendo flag de Material...")

    # Depósito 01 Central
    driver.execute_script("""
        document.getElementsByName('cdDeposito')[0].value = '01';
        AdicionaDeposito();
    """)
    logging.info("⚙️ Selecionando Depósito opção 01 Central...")

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

    # Essa rotina não tem botão CSV — tem botão Salvar dentro da própria página
    try:
        analise = aguardar_estado_ia(
            **AGUARDAR_SALVAR_BOTAO_PAGINA,
            contexto=f"Rotina {CODIGO_ROTINA} — aguardando relatório de inventário",
            descricao_adicional=(
                "Esta rotina não usa o botão CSV do toolbar. "
                "Após processar, aparece um botão 'Salvar' dentro do corpo da página. "
                "NÃO é a barra de download do Edge."
            )
        )
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando relatório na rotina {CODIGO_ROTINA}")
        return "skip"

    if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
        logging.warning(f"⏭️ {analise.get('mensagem')} — pulando")
        return "skip"

    logging.info("✅ Relatório gerado! Clicando em Salvar...")
    if not clicar_elemento_ia(**CLICAR_SALVAR_BOTAO_PAGINA):
        logging.error("❌ Falha ao clicar no botão Salvar")
        return "skip"

    logging.info("⏳ Aguardando download...")
