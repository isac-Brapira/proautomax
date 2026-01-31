import time
import pyautogui
import os

# Variaveis de imagens
CSV_BTN = os.getenv("PATH_IMAGE_CSV")
CSV_BTN_2 = os.getenv("PATH_IMAGE_CSV_2")
SALVAR_BTN = os.getenv("PATH_IMAGE_SAVE")
VISUALIZAR_BTN = os.getenv("PATH_IMAGE_VISUALIZAR")

# Só procura a imagem e retorna a posição se encontrar. Timeout em segundos.
def encontrar_imagem(caminhoImagem, timeout=None):
    inicio = time.time()
    while True:
        try:
            pos = pyautogui.locateOnScreen(caminhoImagem, confidence=0.8)
            if pos:
                print("✅ Botão encontrado!")
                return pos
        except:
            pass
            
        if timeout and (time.time() - inicio > timeout):
            raise TimeoutError(f"❌ Imagem não encontrada após {timeout} segundos.")
            
        time.sleep(0.5)

# Encontra a imagem e clica
def clicar_imagem(caminhoImagem, timeout=60):
    try:
        pos = encontrar_imagem(caminhoImagem, timeout=timeout)
        if pos:
            print("Clicando no botão...")
            time.sleep(1)
            pyautogui.click(pyautogui.center(pos))
            print("Botão clicado!")
    except TimeoutError:
        print(f"❌ Não foi possível encontrar/clicar na imagem: {caminhoImagem}")
    