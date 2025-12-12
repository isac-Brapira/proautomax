import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def aceitar_alertas(driver, tentativas=5, intervalo=1):
    """
    Tenta aceitar todos os alerts que possam estar aparecendo em sequência.
    :param driver: WebDriver
    :param tentativas: quantas vezes repetimos a checagem
    :param intervalo: tempo (s) entre as tentativas
    """
    print("Tentando aceitar possíveis alertas...")
    for _ in range(tentativas):
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            print(f"[aceitar_alertas] Alerta detectado: {alert.text}")
            alert.accept()
            time.sleep(intervalo)  
        except TimeoutException:
            # Se não há alert nessa tentativa, paramos
            print("[aceitar_alertas] Nenhum alert presente nessa checagem.")
            break
    print("[aceitar_alertas] Fim das tentativas.")