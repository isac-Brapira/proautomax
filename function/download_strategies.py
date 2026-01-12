"""
Sistema de estratégias para confirmar downloads do Promax.
Cada rotina pode especificar qual estratégia usar ou tentar todas.
"""

import time
import os
import pyautogui
import pygetwindow as gw
from abc import ABC, abstractmethod


class DownloadStrategy(ABC):
    """Classe base para estratégias de download"""
    
    @abstractmethod
    def executar(self, timeout=5):
        """
        Tenta confirmar o download.
        Retorna True se conseguiu, False caso contrário.
        """
        pass
    
    def focar_janela_edge(self):
        """Tenta focar na janela do Edge/Promax"""
        for w in gw.getAllTitles():
            if "Edge" in w or "Promax" in w:
                try:
                    gw.getWindowsWithTitle(w)[0].activate()
                    time.sleep(0.5)
                    return True
                except:
                    pass
        return False


class TabEnterStrategy(DownloadStrategy):
    """Estratégia: Tab + Enter"""
    
    def executar(self, timeout=5):
        print("   → Tentando: Tab + Enter")
        self.focar_janela_edge()
        
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(timeout)
        return True


class MultiTabEnterStrategy(DownloadStrategy):
    """Estratégia: Múltiplos Tabs + Enter (caso o foco não esteja no botão)"""
    
    def __init__(self, num_tabs=3):
        self.num_tabs = num_tabs
    
    def executar(self, timeout=5):
        print(f"   → Tentando: {self.num_tabs}x Tab + Enter")
        self.focar_janela_edge()
        
        for _ in range(self.num_tabs):
            pyautogui.press('tab')
            time.sleep(0.2)
        
        pyautogui.press('enter')
        time.sleep(timeout)
        return True


class ClickPosicaoStrategy(DownloadStrategy):
    """Estratégia: Clica em uma posição específica da tela"""
    
    def __init__(self, x_percent=0.42, y_percent=0.95):
        """
        x_percent: porcentagem da largura da tela (0.0 a 1.0)
        y_percent: porcentagem da altura da tela (0.0 a 1.0)
        """
        self.x_percent = x_percent
        self.y_percent = y_percent
    
    def executar(self, timeout=5):
        print(f"   → Tentando: Click na posição ({self.x_percent}, {self.y_percent})")
        self.focar_janela_edge()
        
        screen_width, screen_height = pyautogui.size()
        x = int(screen_width * self.x_percent)
        y = int(screen_height * self.y_percent)
        
        pyautogui.click(x, y)
        time.sleep(timeout)
        return True


class EscEnterStrategy(DownloadStrategy):
    """Estratégia: ESC (fecha outros popups) + Tab + Enter"""
    
    def executar(self, timeout=5):
        print("   → Tentando: ESC + Tab + Enter")
        self.focar_janela_edge()
        
        pyautogui.press('esc')
        time.sleep(0.3)
        pyautogui.press('tab')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(timeout)
        return True


class DownloadManager:
    """Gerenciador de estratégias de download"""
    
    # Estratégias padrão (ordenadas por probabilidade de sucesso)
    ESTRATEGIAS_PADRAO = [
     #   TabEnterStrategy(),
     #   MultiTabEnterStrategy(num_tabs=2),
        MultiTabEnterStrategy(num_tabs=3),
     #   EscEnterStrategy(),
     #   ClickPosicaoStrategy(x_percent=0.42, y_percent=0.95),
     #   ClickPosicaoStrategy(x_percent=0.38, y_percent=0.93),  # posição alternativa
    ]
    
    def __init__(self, pasta_temp):
        self.pasta_temp = pasta_temp
    
    def confirmar_download(self, estrategias=None, timeout_por_estrategia=5, max_tentativas=3):
        """
        Tenta confirmar o download usando várias estratégias.
        
        Args:
            estrategias: Lista de estratégias a tentar (None = usa padrão)
            timeout_por_estrategia: Tempo de espera após cada tentativa
            max_tentativas: Máximo de tentativas com todas as estratégias
        
        Returns:
            True se conseguiu confirmar, False caso contrário
        """
        if estrategias is None:
            estrategias = self.ESTRATEGIAS_PADRAO
        
        print("🔽 Iniciando confirmação de download...")
        
        for tentativa in range(max_tentativas):
            print(f"\n📍 Tentativa {tentativa + 1}/{max_tentativas}")
            
            for estrategia in estrategias:
                # Verifica se já baixou antes de tentar
                if self._arquivo_ja_baixado():
                    print("✓ Arquivo já foi baixado!")
                    return True
                
                # Tenta a estratégia
                try:
                    estrategia.executar(timeout=timeout_por_estrategia)
                    
                    # Verifica se funcionou
                    if self._arquivo_ja_baixado():
                        print(f"✓ Sucesso com: {estrategia.__class__.__name__}")
                        return True
                    
                except Exception as e:
                    print(f"   ✗ Erro: {e}")
            
            if tentativa < max_tentativas - 1:
                print("⏳ Aguardando antes da próxima rodada...")
                time.sleep(2)
        
        print("⚠ Não foi possível confirmar o download automaticamente")
        return False
    
    def _arquivo_ja_baixado(self):
        """Verifica se já tem arquivo CSV na pasta de download"""
        try:
            arquivos = [
                f for f in os.listdir(self.pasta_temp)
                if f.lower().endswith('.csv') and not self._arquivo_em_uso(
                    os.path.join(self.pasta_temp, f)
                )
            ]
            return len(arquivos) > 0
        except:
            return False
    
    def _arquivo_em_uso(self, caminho):
        """Verifica se o arquivo ainda está sendo escrito"""
        try:
            with open(caminho, 'rb'):
                return False
        except OSError:
            return True


# ============================================
# Funções de conveniência (compatibilidade)
# ============================================

DOWNLOAD_TEMP = r"E:\Code\proautomax\downloads\_temp"
_manager = DownloadManager(DOWNLOAD_TEMP)


def confirmar_download_com_retry(tentativas=3):
    """
    Função de compatibilidade com o código existente.
    Usa o sistema de estratégias automaticamente.
    """
    return _manager.confirmar_download(max_tentativas=tentativas)


def confirmar_download_personalizado(estrategias, tentativas=3):
    """
    Permite que rotinas específicas usem estratégias customizadas.
    
    Exemplo:
        estrategias = [
            TabEnterStrategy(),
            ClickPosicaoStrategy(x_percent=0.5, y_percent=0.92)
        ]
        confirmar_download_personalizado(estrategias)
    """
    return _manager.confirmar_download(
        estrategias=estrategias,
        max_tentativas=tentativas
    )