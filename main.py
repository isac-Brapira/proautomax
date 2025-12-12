from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pygetwindow as gw
from function.aceitar_alertas import aceitar_alertas

ie_options = webdriver.IeOptions()

ie_options.attach_to_edge_chrome = True
ie_options.edge_executable_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ie_options.ignore_zoom_level = True
ie_options.require_window_focus = True
ie_options.ensure_clean_session = True
ie_options.ignore_protected_mode_settings = True
ie_options.initial_browser_url = "https://brapira.promaxcloud.com.br"

service = webdriver.IeService(executable_path=r'.\drivers\IEDriverServer.exe')
driver = webdriver.Ie(service=service, options=ie_options)

# Foco na janela
window_title = "PromaxWEB"
for window in gw.getAllTitles():
    if window_title in window:
        gw.getWindowsWithTitle(window)[0].activate()
        break

wait = WebDriverWait(driver, 20)

print(driver.page_source)

driver.switch_to.frame("top")

user_box = wait.until(
    EC.presence_of_element_located((By.NAME, "Usuario"))
)
pw_box = wait.until(
    EC.presence_of_element_located((By.NAME, "Senha"))
)

user_box.clear()
driver.execute_script("arguments[0].value = arguments[1];", user_box, "Macros")

pw_box.clear()
driver.execute_script("arguments[0].value = arguments[1];", pw_box, "M@cros@251")

btn = wait.until(EC.presence_of_element_located((By.ID, "BtnConfirm")))
btn.click()

btn = wait.until(EC.presence_of_element_located((By.NAME, "cmdConfirma")))
btn.click()

aceitar_alertas(driver)
# driver.quit()
