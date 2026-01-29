import time
import pyautogui


def clicar_imagem(caminhoImagem):
    while True:
        try:
            pos = pyautogui.locateOnScreen(caminhoImagem, confidence= 0.8)
            if pos:
                print("✅ Botão encontrado!")
                time.sleep(2)
                pyautogui.click(pyautogui.center(pos))

                break
        except pyautogui.ImageNotFoundException:
            pass