import os
import time
from pywinauto import Desktop
from pywinauto.keyboard import send_keys


def abrir_salvar_como():

    print("⌨️ Navegando até 'Salvar como'...")
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
    time.sleep(10)  # Espera a janela abrir"

def preencher_dialogo_salvar(caminho_completo, timeout=30):
    """
    Preenche o diálogo 'Salvar Como' do Windows com o caminho do arquivo.
    
    Args:
        caminho_completo: Caminho completo incluindo nome do arquivo
        timeout: Tempo máximo para encontrar o diálogo
    
    Returns:
        True se conseguiu salvar, False caso contrário
    """
    print(f"💾 Salvando em: {caminho_completo}")
    
    inicio = time.time()
    dialogo_encontrado = False
    
    # Tenta encontrar o diálogo "Salvar Como"
    while time.time() - inicio < timeout:
        try:
            # Tenta conectar no diálogo (vários títulos possíveis)
            # O título pode variar: "Salvar como", "Salvar Como", "Save As"
            desktop = Desktop(backend="uia")
            
            # Procura por qualquer janela com "Salvar" no título
            dialogo = None
            for janela in desktop.windows():
                titulo = janela.window_text().lower()
                if "salvar" in titulo or "save" in titulo:
                    dialogo = janela
                    dialogo_encontrado = True
                    print(f"✓ Diálogo encontrado: {janela.window_text()}")
                    break
            
            if dialogo_encontrado:
                break
                
        except Exception as e:
            pass
        
        time.sleep(0.5)
    
    if not dialogo_encontrado:
        print("❌ Não foi possível encontrar o diálogo 'Salvar Como'")
        return False
    
    try:
        # Método 1: Tenta encontrar o campo "Nome do arquivo" diretamente
        print("📝 Preenchendo campo de nome...")
        
        try:
            # Procura pelo campo de edição (geralmente é o primeiro Edit visível)
            campo_nome = dialogo.child_window(class_name="Edit", found_index=0)
            campo_nome.wait('visible', timeout=5)
            
            # Limpa o campo e preenche com o caminho completo
            campo_nome.set_focus()
            time.sleep(0.2)
            
            # Seleciona tudo e substitui
            send_keys("^a")  # Ctrl+A
            time.sleep(0.2)
            
            # Digita o caminho
            campo_nome.type_keys(caminho_completo, with_spaces=True)
            time.sleep(0.5)
            
            print("✓ Caminho preenchido")
            
        except Exception as e:
            print(f"⚠️ Método 1 falhou: {e}")
            print("💡 Tentando método alternativo...")
            
            # Método 2: Usa keyboard pra preencher
            send_keys("^a")  # Ctrl+A
            time.sleep(0.2)
            send_keys(caminho_completo, with_spaces=True)
            time.sleep(0.5)
        
        # Procura e clica no botão "Salvar"
        print("🔘 Clicando em 'Salvar'...")
        
        try:
            # Tenta encontrar o botão Salvar (pode ter vários nomes)
            botao_salvar = None
            
            # Procura por diferentes variações do botão
            for nome_botao in ["Salvar", "Save", "&Salvar", "OK"]:
                try:
                    botao_salvar = dialogo.child_window(title=nome_botao, control_type="Button")
                    if botao_salvar.exists(timeout=1):
                        break
                except:
                    pass
            
            if botao_salvar and botao_salvar.exists():
                botao_salvar.click()
                time.sleep(1)
                print("✓ Botão 'Salvar' clicado")
            else:
                # Fallback: aperta Enter
                print("⚠️ Botão não encontrado, usando Enter...")
                send_keys("{ENTER}")
                time.sleep(1)
        
        except Exception as e:
            print(f"⚠️ Erro ao clicar no botão: {e}")
            print("💡 Usando Enter como fallback...")
            send_keys("{ENTER}")
            time.sleep(1)
        
        # Se pedir confirmação de substituição, aceita
        time.sleep(1)
        try:
            desktop = Desktop(backend="uia")
            for janela in desktop.windows():
                titulo = janela.window_text().lower()
                if "substituir" in titulo or "replace" in titulo or "confirmar" in titulo:
                    print("⚠️ Confirmando substituição...")
                    send_keys("{ENTER}")
                    time.sleep(1)
                    break
        except:
            pass
        
        print("✓ Salvamento concluído")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher diálogo: {e}")
        import traceback
        traceback.print_exc()
        return False


def salvar_arquivo(destino, nome_arquivo):
    """
    Fluxo completo: abre o diálogo e salva o arquivo.
    
    Args:
        destino: Caminho da pasta de destino
        nome_arquivo: Nome do arquivo (ex: "0111.csv")
    
    Returns:
        Caminho completo do arquivo salvo
    """
    print("💾 Iniciando salvamento com PyWinAuto...")
    
    # Monta o caminho completo
    caminho_completo = os.path.join(destino, nome_arquivo)
    print(f"📂 Caminho: {caminho_completo}")
    
    # 1. Abre o diálogo "Salvar Como"
    abrir_salvar_como()
    
    # 2. Preenche e confirma
    sucesso = preencher_dialogo_salvar(caminho_completo)
    
    if not sucesso:
        raise Exception("Não foi possível salvar o arquivo")
    
    # 3. Verifica se o arquivo foi salvo
    if _verificar_arquivo_salvo(caminho_completo, timeout=30):
        print(f"✓ Arquivo salvo com sucesso!")
        return caminho_completo
    else:
        raise Exception(f"Arquivo não foi encontrado em: {caminho_completo}")


def _verificar_arquivo_salvo(caminho, timeout=30):
    """
    Verifica se o arquivo foi salvo e está pronto.
    """
    print(f"⏳ Verificando arquivo (timeout: {timeout}s)...")
    inicio = time.time()
    
    while time.time() - inicio < timeout:
        if os.path.exists(caminho):
            try:
                # Verifica se está pronto
                with open(caminho, 'r+b'):
                    pass
                
                tamanho = os.path.getsize(caminho)
                if tamanho > 0:
                    print(f"   ✓ Arquivo encontrado ({tamanho} bytes)")
                    return True
            except (OSError, PermissionError):
                print(f"   ⏳ Arquivo ainda sendo escrito...")
        else:
            tempo_decorrido = int(time.time() - inicio)
            if tempo_decorrido % 5 == 0 and tempo_decorrido > 0:
                print(f"   ⏱️ {tempo_decorrido}s - Aguardando...")
        
        time.sleep(1)
    
    print(f"   ❌ Timeout: arquivo não foi encontrado")
    return False


# Funções de compatibilidade
def limpar_pasta_temp():
    """Não necessário no modo Salvar Como"""
    pass


def confirmar_download_com_retry(tentativas=3):
    """Não necessário no modo Salvar Como"""
    pass


def mover_arquivo(destino, nome_arquivo):
    """Wrapper para compatibilidade com executor.py"""
    return salvar_arquivo(destino, nome_arquivo)