import logging
import time
import traceback
import pyautogui
import os

# Variaveis de imagens
CSV_BTN = os.getenv("PATH_IMAGE_CSV")
CSV_BTN_2 = os.getenv("PATH_IMAGE_CSV_2")
SALVAR_BTN = os.getenv("PATH_IMAGE_SAVE")
SALVAR_BTN_2 = os.getenv("PATH_IMAGE_SAVE_2")
VISUALIZAR_BTN = os.getenv("PATH_IMAGE_VISUALIZAR")

def encontrar_imagem(caminhoImagem, timeout=None, confidence=0.6):
    inicio = time.time()
    tentativas = 0

    while True:
        try:
            pos = pyautogui.locateOnScreen(caminhoImagem, confidence=confidence)

            if pos:
                logging.info(f"✅ Imagem encontrada: {caminhoImagem}")
                return pos

        except pyautogui.ImageNotFoundException:
            pass

        tentativas += 1

        # Log a cada X tentativas (evita spam)
        if tentativas % 10 == 0:
            logging.info(f"🔍 Procurando imagem... ({tentativas} tentativas)")

        # Timeout
        if timeout and (time.time() - inicio > timeout):
            screenshot_nome = f"erro_{int(time.time())}.png"
            pyautogui.screenshot(screenshot_nome)

            logging.error(f"❌ Imagem não encontrada após {timeout}s: {caminhoImagem}")
            logging.error(f"📸 Screenshot salvo: {screenshot_nome}")

            raise TimeoutError(f"Imagem não encontrada: {caminhoImagem}")

        # 🔥 mantém tela “viva” (importantíssimo no VNC)
        try:
            pyautogui.moveRel(1, 0)
            pyautogui.moveRel(-1, 0)
        except:
            pass

        time.sleep(0.5)
# Só procura a imagem e retorna a posição se encontrar. Timeout em segundos.
# def encontrar_imagem(caminhoImagem, timeout=None):
#     inicio = time.time()
#     while True:
#         try:
#             pos = pyautogui.locateOnScreen(caminhoImagem, confidence=0.8)
#             if pos:
#                 logging.info("✅ Botão encontrado!")
#                 return pos
#         except:
#             pass
            
#         if timeout and (time.time() - inicio > timeout):
#             logging.error(f"❌ Imagem não encontrada após {timeout} segundos.")
#             raise TimeoutError(f"❌ Imagem não encontrada após {timeout} segundos.")
            
#         time.sleep(0.5)

# Encontra a imagem e clica
def clicar_imagem(caminhoImagem, timeout=120):
    try:
        pos = encontrar_imagem(caminhoImagem, timeout=timeout)
        if pos:
            logging.info("Clicando no botão...")
            time.sleep(1)
            pyautogui.click(pyautogui.center(pos))
            logging.info("Botão clicado!")
    except TimeoutError:
        logging.error(f"❌ Não foi possível encontrar/clicar na imagem: {caminhoImagem}")
    