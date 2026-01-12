"""
Sistema de download usando "Salvar Como".
Mais direto e confiável que esperar download automático.
"""

import os
import time
import pyautogui
import pygetwindow as gw


def salvar_arquivo(codigo_rotina, destino):
    """
    Usa "Salvar Como" para salvar o arquivo diretamente no destino.
    
    Args:
        codigo_rotina: Código da rotina (será o nome do arquivo)
        destino: Caminho completo onde salvar o arquivo
    
    Returns:
        Caminho completo do arquivo salvo
    """
    print("💾 Iniciando salvamento com 'Salvar Como'...")
    
    # Garante que a pasta existe
    os.makedirs(destino, exist_ok=True)
    
    # Monta o caminho completo do arquivo
    nome_arquivo = f"{codigo_rotina}.csv"
    caminho_completo = os.path.join(destino, nome_arquivo)
    
    print(f"📂 Destino: {caminho_completo}")
    
    # Foca na janela do Edge
    #_focar_edge()
    time.sleep(1)
    
    # Sequência: Tab 3x + Arrow Down 2x + Enter
    print("🎯 Abrindo diálogo 'Salvar Como'...")
    
    # Tab 3x (navega até o dropdown)
    for i in range(3):
        pyautogui.press('tab')
        time.sleep(0.3)
        print(f"   Tab {i+1}/3")
    
    # Arrow Down 2x (seleciona "Salvar como")
    for i in range(2):
        pyautogui.press('down')
        time.sleep(0.3)
        print(f"   Arrow Down {i+1}/2")
    
    # Enter (abre o diálogo)
    print("   Enter (abrindo diálogo)...")
    pyautogui.press('enter')
    time.sleep(3)  # Espera o diálogo abrir
    
    # Agora preenche o campo com o caminho completo
    print("✏️ Preenchendo caminho...")
    
    # Ctrl+A para selecionar tudo que já está no campo
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    
    # Digita o caminho completo (com intervalo entre teclas)
    print(f"   Digitando: {caminho_completo}")
    pyautogui.write(caminho_completo, interval=0.02)
    time.sleep(1)
    
    # Enter para confirmar o salvamento
    print("   Enter (confirmando salvamento)...")
    pyautogui.press('enter')
    time.sleep(2)
    
    # Se o arquivo já existir, o Windows vai perguntar se quer substituir
    # Vamos dar Enter de novo pra confirmar
    print("   Confirmando substituição (se necessário)...")
    pyautogui.press('enter')
    time.sleep(2)
    
    # Verifica se o arquivo foi salvo
    if _verificar_arquivo_salvo(caminho_completo, timeout=30):
        print(f"✓ Arquivo salvo com sucesso!")
        return caminho_completo
    else:
        raise Exception(f"Arquivo não foi encontrado em: {caminho_completo}")


def _focar_edge():
    """Foca na janela do Edge/Promax"""
    print("🔍 Focando janela do Edge...")
    for w in gw.getAllTitles():
        if "Edge" in w or "Promax" in w:
            try:
                gw.getWindowsWithTitle(w)[0].activate()
                time.sleep(0.5)
                print(f"   ✓ Focado em: {w}")
                return True
            except:
                pass
    print("   ⚠️ Não conseguiu focar")
    return False


def _verificar_arquivo_salvo(caminho, timeout=30):
    """
    Verifica se o arquivo foi salvo e está pronto.
    
    Args:
        caminho: Caminho completo do arquivo
        timeout: Tempo máximo de espera em segundos
    
    Returns:
        True se o arquivo existe e está pronto, False caso contrário
    """
    print(f"⏳ Verificando se arquivo foi salvo (timeout: {timeout}s)...")
    inicio = time.time()
    
    while time.time() - inicio < timeout:
        if os.path.exists(caminho):
            # Arquivo existe, verifica se está pronto
            try:
                # Tenta abrir para garantir que não está em uso
                with open(caminho, 'r+b'):
                    pass
                
                # Verifica se o tamanho é maior que zero
                tamanho = os.path.getsize(caminho)
                if tamanho > 0:
                    print(f"   ✓ Arquivo encontrado ({tamanho} bytes)")
                    return True
                else:
                    print(f"   ⏳ Arquivo vazio, aguardando...")
                    
            except (OSError, PermissionError):
                print(f"   ⏳ Arquivo ainda sendo escrito...")
        else:
            # Mostra progresso a cada 5 segundos
            tempo_decorrido = int(time.time() - inicio)
            if tempo_decorrido % 5 == 0 and tempo_decorrido > 0:
                print(f"   ⏱️ {tempo_decorrido}s - Aguardando...")
        
        time.sleep(1)
    
    print(f"   ❌ Timeout: arquivo não foi encontrado")
    return False


# Mantém compatibilidade com o executor existente
def limpar_pasta_temp():
    """Função de compatibilidade - não faz nada no modo Salvar Como"""
    pass


def confirmar_download_com_retry(tentativas=3):
    """Função de compatibilidade - não é necessária no modo Salvar Como"""
    print("ℹ️ Modo 'Salvar Como' - download será confirmado automaticamente")
    return True


def mover_arquivo(codigo_rotina, destino):
    """
    Função adaptada para o modo Salvar Como.
    Em vez de mover, chama salvar_arquivo que já salva no destino correto.
    """
    return salvar_arquivo(codigo_rotina, destino)