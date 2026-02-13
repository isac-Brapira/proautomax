
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def desmarcar_item(tipoInput, wait, driver, name, value, descricao, CODIGO_ROTINA):
    item = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input[type='{tipoInput}'][name='{name}'][value='{value}']")
        )
    )

    if item.is_selected():
        driver.execute_script("arguments[0].click();", item)
        print(f"ROTINA {CODIGO_ROTINA}:⚙️ {tipoInput} de {descricao} desmarcado...")

def marcar_item(tipoInput, wait, driver, name, value, descricao, CODIGO_ROTINA):
    item = wait.until(
        EC.presence_of_element_located(
             (By.CSS_SELECTOR, f"input[type='{tipoInput}'][name='{name}'][value='{value}']")
        )
    )

    if not item.is_selected():
        driver.execute_script("arguments[0].click();", item)
        print(f"ROTINA {CODIGO_ROTINA}:⚙️ {tipoInput} de {descricao} marcado...")