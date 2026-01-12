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

# Pasta Downloads padrão do Windows
PASTA_DOWNLOADS =  "E:\\Users\\Isac\\Downloads" #str(Path.home() / "Downloads")


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
    time.sleep(5)

    print("⏳ Procurando botão Salvar...")

    while True:
        try:
            pos = pyautogui.locateOnScreen('./images/download_bar.png')
            if pos:
                print("✅ Botão encontrado!")
                # Clica na imagem para garantir o foco na janela antes de enviar teclas
                pyautogui.click(pyautogui.center(pos))
                break
        except pyautogui.ImageNotFoundException:
            pass  # imagem ainda não apareceu

    time.sleep(0.5)

    print("🎯 Continuando execução...")

    time.sleep(2)



    # TAB > TAB > TAB
    send_keys("{TAB}")
    time.sleep(0.2)

    send_keys("{TAB}")
    time.sleep(0.2)

    send_keys("{TAB}")
    time.sleep(0.2)

    print(" Apertou TAB 3x")

    # ↓ > ↓
    send_keys("{DOWN}")
    time.sleep(0.2)

    send_keys("{DOWN}")
    time.sleep(0.2)

    print(" Apertou SETA PARA BAIXO 2x")

    # ENTER (executa salvar como)
    send_keys("{ENTER}")
    time.sleep(0.5)

    print(" Apertou ENTER")

    print("💾 Opção 'Salvar como' acionada!")
def aguardar_novo_arquivo(timeout=120):
    """
    Aguarda até que um novo arquivo CSV apareça na pasta Downloads.
    Ignora arquivos parciais (.crdownload, .tmp, .partial).
    
    Returns:
        Nome do arquivo CSV completo que apareceu
    
    Raises:
        TimeoutError: Se nenhum arquivo aparecer no tempo limite
    """
    print(f"⏳ Aguardando arquivo CSV...")
    print(f"📂 Monitorando: {PASTA_DOWNLOADS}")
    
    inicio = time.time()
    ultimo_log = 0
    
    # Captura o estado inicial (arquivos que JÁ existem)
    try:
        arquivos_iniciais = set(
            f for f in os.listdir(PASTA_DOWNLOADS)
            if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
        )
        print(f"   📋 {len(arquivos_iniciais)} arquivo(s) já existente(s)")
    except Exception as e:
        print(f"   ⚠️ Erro ao listar arquivos iniciais: {e}")
        arquivos_iniciais = set()
    
    while time.time() - inicio < timeout:
        try:
            # Lista arquivos atuais
            arquivos_atuais = set(
                f for f in os.listdir(PASTA_DOWNLOADS)
                if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
            )
            
            # Detecta arquivos NOVOS (que não estavam antes)
            arquivos_novos = arquivos_atuais - arquivos_iniciais
            
            # Filtra só CSVs completos (ignora parciais)
            csvs_completos = [
                f for f in arquivos_novos
                if f.lower().endswith('.csv')
                and not f.endswith('.crdownload')
                and not f.endswith('.tmp')
                and not f.endswith('.partial')
                and not f.endswith('.inf')
            ]
            
            # Log periódico
            tempo_decorrido = time.time() - inicio
            if tempo_decorrido - ultimo_log >= 5:
                if arquivos_novos:
                    print(f"   ⏱️ {int(tempo_decorrido)}s - {len(arquivos_novos)} arquivo(s) novo(s) detectado(s)")
                else:
                    print(f"   ⏱️ {int(tempo_decorrido)}s - Aguardando...")
                ultimo_log = tempo_decorrido
            
            # Se encontrou CSV completo, verifica se está pronto
            for csv in csvs_completos:
                caminho = os.path.join(PASTA_DOWNLOADS, csv)
                
                if _arquivo_esta_pronto(caminho):
                    print(f"✓ Arquivo detectado e pronto: {csv}")
                    return csv
                else:
                    print(f"   📝 Arquivo ainda sendo escrito: {csv}")
        
        except Exception as e:
            print(f"   ⚠️ Erro ao monitorar: {e}")
        
        time.sleep(1)
    
    raise TimeoutError(f"Nenhum arquivo CSV apareceu após {timeout}s")


def _arquivo_esta_pronto(caminho, verificacoes=3):
    """
    Verifica se o arquivo terminou de ser baixado.
    Faz múltiplas verificações pra garantir.
    
    Args:
        caminho: Caminho completo do arquivo
        verificacoes: Número de verificações a fazer
    
    Returns:
        True se o arquivo está pronto, False caso contrário
    """
    for _ in range(verificacoes):
        try:
            # Verifica se o tamanho é estável
            tamanho1 = os.path.getsize(caminho)
            time.sleep(0.5)
            tamanho2 = os.path.getsize(caminho)
            
            # Se tá crescendo, não tá pronto
            if tamanho1 != tamanho2:
                return False
            
            # Tenta abrir pra leitura/escrita
            with open(caminho, 'r+b') as f:
                pass
            
            # Se chegou aqui e tamanho > 0, tá pronto
            if tamanho2 > 0:
                return True
                
        except (OSError, PermissionError):
            # Se não consegue abrir, ainda tá em uso
            return False
        
        time.sleep(0.5)
    
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