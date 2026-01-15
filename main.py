from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pygetwindow as gw
from function.aceitar_alertas import aceitar_alertas
from function.abrir_rotinas import abrir_rotinas
from rotinas.loader import carregar_rotinas
from rotinas.executor import executar_rotinas

from dotenv import load_dotenv
import os


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

PROMAX_USER = os.getenv("PROMAX_USER")
PROMAX_PASSWORD = os.getenv("PROMAX_PASSWORD")

# Verifica se as credenciais foram carregadas corretamente
if not PROMAX_USER or not PROMAX_PASSWORD:
    raise ValueError("CREDENCIAIS DE LOGIN NÃO ENCONTRADAS NO .ENV\n")
else:
    print("\nCREDENCIAIS DE LOGIN ENCONTRADAS\n")

# Configurações do Internet Explorer para usar o Edge
ie_options = webdriver.IeOptions()

ie_options.attach_to_edge_chrome = True
ie_options.edge_executable_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ie_options.ignore_zoom_level = True
ie_options.require_window_focus = True
ie_options.ensure_clean_session = True
ie_options.ignore_protected_mode_settings = True
ie_options.initial_browser_url = "https://brapira.promaxcloud.com.br"

# Inicia o driver do Internet Explorer
service = webdriver.IeService(executable_path=r'.\drivers\IEDriverServer.exe')
driver = webdriver.Ie(service=service, options=ie_options)

# Foco na janela
window_title = "PromaxWEB"
for window in gw.getAllTitles():
    if window_title in window:
        gw.getWindowsWithTitle(window)[0].activate()
        break

wait = WebDriverWait(driver, 20)

# Mudar para o frame de login que por alguma motivo chama "top"
driver.switch_to.frame("top")

# Aguarda os elementos de login aparecerem e salva em uma variável
user_box = wait.until(
    EC.presence_of_element_located((By.NAME, "Usuario"))
)
pw_box = wait.until(
    EC.presence_of_element_located((By.NAME, "Senha"))
)

# Preenche os campos de login
user_box.clear()
driver.execute_script("arguments[0].value = arguments[1];", user_box, PROMAX_USER)

pw_box.clear()
driver.execute_script("arguments[0].value = arguments[1];", pw_box, PROMAX_PASSWORD)

# Clica no botão de Confirmar 
btn = wait.until(EC.presence_of_element_located((By.ID, "BtnConfirm")))
btn.click()

WebDriverWait(driver, 20)

# Clica no outro botão de Confirmar que já mudou de nome D:
btn = wait.until(EC.presence_of_element_located((By.NAME, "cmdConfirma")))
btn.click()


aceitar_alertas(driver)
# driver.quit()

rotinas = carregar_rotinas()
executar_rotinas(driver, rotinas, "rotinas.json")