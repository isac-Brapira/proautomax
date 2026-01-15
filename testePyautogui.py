import pyautogui
import time

print("⏳ Procurando botão Salvar...")

while True:
    try:
        pos = pyautogui.locateOnScreen('./images/download_bar.png')
        if pos:
            print("✅ Botão encontrado!")
            break
    except pyautogui.ImageNotFoundException:
        pass  # imagem ainda não apareceu

    time.sleep(0.5)

print("🎯 Continuando execução...")
