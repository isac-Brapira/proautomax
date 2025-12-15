from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchFrameException
import time

def abrir_rotinas(driver, codigo_rotina, timeout=20):
    try:
        # Garante que estamos no contexto principal
        driver.switch_to.default_content()
        
        # Tenta mudar para o frame "top", depois "iFrameMenu"
        driver.switch_to.frame("top")
        driver.switch_to.frame(driver.find_element(By.ID, "iFrameMenu"))

        # Cria o WebDriverWait
        wait = WebDriverWait(driver, timeout)

        # Aguarda o campo 'atalho'
        atalho_field = wait.until(EC.presence_of_element_located((By.ID, "atalho")))
        
        # Preenche o campo e chama o JS que abre a rotina
        driver.execute_script("arguments[0].value = arguments[1];", atalho_field, codigo_rotina)
        time.sleep(1)  # Pequeno delay antes de chamar a função

        driver.execute_script("AtalhoMenu();")
        print(f"[navegar_para_rotina] Navegação para o relatório '{codigo_rotina}' bem-sucedida.")
        
        # (Não voltamos pro default_content aqui pois o main.py
        #  chamará a função mudar_janela() em seguida.)

    except (TimeoutException, NoSuchElementException, NoSuchFrameException) as e:
        print(f"[navegar_para_rotina] Erro ao navegar para o relatório {codigo_rotina}: {e}")
    except Exception as e:
        print(f"[navegar_para_rotina] Erro inesperado ao navegar para {codigo_rotina}: {e}")