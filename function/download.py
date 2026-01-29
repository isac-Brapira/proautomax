"""
Sistema de download híbrido - combina o melhor das duas abordagens.
Monitora Downloads padrão + PyWinAuto pra confirmar.
"""

import os
import time
import shutil
from pathlib import Path
from pywinauto.keyboard import send_keys
import pyautogui
from dotenv import load_dotenv

load_dotenv()
# Pasta Downloads padrão do Windows
PASTA_DOWNLOADS =  os.getenv("PATH_USER") #str(Path.home() / "Downloads")


def confirmar_download():
    """
    Confirma o download usando Tab 3x + Enter.
    Esse é o fluxo que você já testou e funciona.
    """
    """ print("🔽 Confirmando download...")
    
    time.sleep(2)  # Espera a barra de download aparecer
    
    # Tab 3x (navega até o botão Salvar)
    print("   Tab 3x...")
    send_keys("{TAB 3}")
    time.sleep(0.5)
    
    # Enter (clica em Salvar)
    print("   Enter...")
    send_keys("{ENTER}")
    time.sleep(1)
    
    print("✓ Download confirmado")

    """
    time.sleep(2)

    print("⏳ Procurando botão Salvar...")

    while True:
        try:
            pos = pyautogui.locateOnScreen(os.getenv("PATH_IMAGE_SAVE"), confidence= 0.8)
            if pos:
                print("✅ Botão encontrado!")
                print(pos)
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                pyautogui.click(pyautogui.center(pos))
                # Clica bem no começo da imagem para conseguir dar o tab
                # pyautogui.click(pos.left + 2, pos.top + 2)
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    time.sleep(0.5)

    print("🎯 Continuando execução...")

    time.sleep(2)



    # TAB > TAB > TAB
    # send_keys("{TAB}")
    # time.sleep(0.2)

    # send_keys("{TAB}")
    # time.sleep(0.2)

    # send_keys("{TAB}")
    # time.sleep(0.2)

    # print(" Apertou TAB 3x")

    # ↓ > ↓
    # send_keys("{DOWN}")
    # time.sleep(0.2)

    # send_keys("{DOWN}")
    # time.sleep(0.2)

    # print(" Apertou SETA PARA BAIXO 2x")

    # ENTER (executa salvar como)
    send_keys("{ENTER}")
    time.sleep(0.5)

    print(" Apertou ENTER")

    print("💾 Opção 'Salvar como' acionada!")

def aguardar_novo_arquivo(timeout=120):
    print(f"⏳ Aguardando arquivo INF...")
    print(f"📂 Monitorando: {PASTA_DOWNLOADS}")

    inicio = time.time()
    ultimo_log = 0

    while time.time() - inicio < timeout:
        try:
            arquivos = [
                f for f in os.listdir(PASTA_DOWNLOADS)
                if f.lower().endswith(".inf")
                and not f.endswith((".crdownload", ".tmp", ".partial"))
                and os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
            ]

            if arquivos:
                # pega o mais recente
                arquivo_mais_recente = max(
                    arquivos,
                    key=lambda f: os.path.getmtime(os.path.join(PASTA_DOWNLOADS, f))
                )

                caminho = os.path.join(PASTA_DOWNLOADS, arquivo_mais_recente)

                if _arquivo_esta_pronto(caminho):
                    print(f"✓ Arquivo detectado e pronto: {arquivo_mais_recente}")
                    return arquivo_mais_recente

            # log a cada 5s
            tempo = time.time() - inicio
            if tempo - ultimo_log >= 5:
                print(f"   ⏱️ {int(tempo)}s - Aguardando arquivo...")
                ultimo_log = tempo

        except Exception as e:
            print(f"   ⚠️ Erro ao monitorar: {e}")

        time.sleep(1)

    raise TimeoutError(f"Nenhum arquivo INF apareceu após {timeout}s")



def _arquivo_esta_pronto(caminho, tempo_estabilidade=2.0):
    """
    Verifica se o arquivo terminou de ser baixado monitorando a estabilidade do tamanho
    e se o arquivo está acessível para escrita.
    
    Args:
        caminho: Caminho completo do arquivo
        tempo_estabilidade: Tempo (segundos) que o tamanho deve permanecer inalterado
    
    Returns:
        True se o arquivo está pronto, False caso contrário
    """
    start_stable = None
    last_size = -1
    
    # Tenta monitorar por no máximo 15 segundos (timeout interno de segurança)
    max_check_time = 15 
    check_start = time.time()

    while (time.time() - check_start) < max_check_time:
        try:
            if not os.path.exists(caminho):
                return False
                
            current_size = os.path.getsize(caminho)
            
            if current_size == last_size and current_size > 0:
                if start_stable is None:
                    start_stable = time.time()
                elif (time.time() - start_stable) >= tempo_estabilidade:
                    # Tamanho estável pelo tempo necessário. Tenta abrir.
                    try:
                        with open(caminho, 'r+b') as f:
                            return True
                    except (OSError, PermissionError):
                        # Arquivo bloqueado, reseta estabilidade
                        start_stable = None 
            else:
                # Tamanho mudou ou é 0, reseta contagem
                last_size = current_size
                start_stable = None
                
            time.sleep(0.5)
            
        except Exception:
            # Erro ao acessar arquivo (talvez sumiu momentaneamente)
            return False

    return False


def mover_arquivo_com_retry(origem, destino, max_tentativas=5):
    """
    Move o arquivo com retry em caso de erro de permissão.
    
    Args:
        origem: Caminho do arquivo de origem
        destino: Caminho do arquivo de destino
        max_tentativas: Número máximo de tentativas
    
    Returns:
        True se conseguiu mover, False caso contrário
    """
    for tentativa in range(max_tentativas):
        try:
            if tentativa > 0:
                print(f"   🔄 Tentativa {tentativa + 1}/{max_tentativas}")
                time.sleep(2)
            
            shutil.move(origem, destino)
            return True
            
        except PermissionError as e:
            if tentativa == max_tentativas - 1:
                # Última tentativa: copia em vez de mover
                print(f"   💡 Erro de permissão, tentando copiar...")
                try:
                    shutil.copy2(origem, destino)
                    os.remove(origem)
                    return True
                except:
                    print(f"   ⚠️ Arquivo mantido em: {origem}")
                    return False
        
        except Exception as e:
            print(f"   ❌ Erro ao mover: {e}")
            if tentativa == max_tentativas - 1:
                return False
    
    return False


def salvar_arquivo(destino, nome_arquivo):
    """
    Fluxo completo de salvamento.
    
    Args:
        destino: Pasta de destino final
        nome_arquivo: Nome final do arquivo (ex: "0111.csv")
    
    Returns:
        Caminho completo do arquivo salvo
    
    Raises:
        Exception: Se não conseguir salvar o arquivo
    """
    print("💾 Iniciando salvamento...")
    
    # 1. Confirma o download (Tab 3x + Enter)
    confirmar_download()
    
    # 2. Aguarda o arquivo aparecer
    try:
        arquivo_baixado = aguardar_novo_arquivo(timeout=120)
    except TimeoutError as e:
        print(f"❌ {e}")
        raise Exception("Timeout: arquivo não foi baixado")
    
    # 3. Move para o destino final
    origem = os.path.join(PASTA_DOWNLOADS, arquivo_baixado)
    
    # Garante que a pasta de destino existe
    os.makedirs(destino, exist_ok=True)
    
    # Caminho final
    caminho_final = os.path.join(destino, nome_arquivo)
    
    print(f"📦 Movendo arquivo...")
    print(f"   De: {origem}")
    print(f"   Para: {caminho_final}")
    
    # Remove arquivo antigo se existir
    if os.path.exists(caminho_final):
        try:
            os.remove(caminho_final)
            print(f"   🗑️ Arquivo antigo removido")
        except Exception as e:
            print(f"   ⚠️ Não foi possível remover arquivo antigo: {e}")
    
    # Move o arquivo
    if mover_arquivo_com_retry(origem, caminho_final):
        print(f"✓ Arquivo salvo com sucesso!")
        return caminho_final
    else:
        raise Exception("Não foi possível mover o arquivo para o destino")


def limpar_pasta_temp():
    """
    Função de compatibilidade - não necessária nessa abordagem.
    """
    pass


def confirmar_download_com_retry(tentativas=3):
    """
    Função de compatibilidade - chama confirmar_download().
    """
    confirmar_download()


def mover_arquivo(destino, nome_arquivo):
    """
    Função de compatibilidade com o executor.py.
    Apenas chama salvar_arquivo().
    """
    return salvar_arquivo(destino, nome_arquivo)


# Inicialização
print(f"✓ Sistema de download carregado")
print(f"📂 Pasta de downloads: {PASTA_DOWNLOADS}")