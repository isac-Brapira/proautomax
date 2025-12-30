import subprocess
import time
from pywinauto import Desktop
from pywinauto.keyboard import send_keys


def salvar_arquivo():
    print("⌨ Navegando até a opção de Salvar...")

    time.sleep(10)  # Espera a janela abrir
    # TAB > TAB > TAB
    send_keys("{TAB}")
    time.sleep(0.2)

    send_keys("{TAB}")
    time.sleep(0.2)

    send_keys("{TAB}")
    time.sleep(0.2)

    # ↓ > ↓
    send_keys("{DOWN}")
    time.sleep(0.2)

    send_keys("{DOWN}")
    time.sleep(0.2)

    # ENTER (executa salvar como)
    send_keys("{ENTER}")
    time.sleep(0.5)

    print("💾 Opção 'Salvar como' acionada!")

    time.sleep(10)  # Espera a janela abrir