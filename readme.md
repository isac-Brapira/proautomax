# ProAutoMax

Framework de automação do sistema Promax (IE Mode / Edge)  
Desenvolvido para executar rotinas automaticamente via Selenium.

## 🎯 Objetivo
Permitir a execução automatizada de rotinas do Promax de forma:
- modular
- escalável
- configurável via JSON
- independente de quem desenvolveu a rotina

## 🧠 Arquitetura

- `main.py` → ponto de entrada
- `rotinas/` → rotinas do sistema
- `rotinas/base.py` → navegação e infra comum
- `rotinas/loader.py` → descoberta automática de rotinas
- `rotinas/executor.py` → execução baseada em JSON
- `rotinas.json` → definição das rotinas a serem executadas

## 🚀 Como executar

```bash
python main.py
