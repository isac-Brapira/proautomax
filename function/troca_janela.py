from selenium.webdriver.support.ui import WebDriverWait

def trocar_para_nova_janela(driver, timeout=10):
    janela_atual = driver.current_window_handle

    WebDriverWait(driver, timeout).until(
        lambda d: len(d.window_handles) > 1
    )

    for handle in driver.window_handles:
        if handle != janela_atual:
            driver.switch_to.window(handle)
            return handle

    raise Exception("Nenhuma nova janela encontrada")

def voltar_para_janela(driver, handle):
    driver.switch_to.window(handle)

