# ProAutoMax — Manual de Referência
### `ai_vision.py` e `acoes.py`

---

## O que importar no topo de cada rotina

```python
from function.ai_vision import aguardar_estado_ia, clicar_elemento_ia, ESTADOS
from function.acoes import (
    # Escolha só o que você precisa — veja a lista completa abaixo
    AGUARDAR_CSV,
    AGUARDAR_CSV_PESADO,
    AGUARDAR_DOWNLOAD_SALVAR,
    AGUARDAR_SALVAR_BOTAO_PAGINA,
    CLICAR_CSV,
    CLICAR_DOWNLOAD_SALVAR,
    CLICAR_SALVAR_BOTAO_PAGINA,
)
```

---

## Funções do `ai_vision.py`

### `aguardar_estado_ia(...)`

Fica em loop tirando screenshots e perguntando para a IA o que está na tela, até um dos estados esperados aparecer ou o tempo acabar. Substitui `encontrar_imagem()` + `time.sleep()` + bloco de retry.

**Como usar:**
```python
analise = aguardar_estado_ia(
    **AGUARDAR_CSV,                        # spread de uma ação do acoes.py
    contexto=f"Rotina {CODIGO_ROTINA}",    # aparece no log, ajuda no debug
)
```

**O que retorna:** um dicionário com o resultado da última análise da IA.
```python
{
    "estado":      "csv_disponivel",
    "confianca":   9,
    "mensagem":    "Botão CSV visível no toolbar",
    "acao":        "clicar_csv",
    "coordenadas": {"x": 1150, "y": 90}
}
```

> ⚠️ **Lança `TimeoutError`** se nenhum estado esperado aparecer no tempo limite. Sempre envolva em `try/except`.

**Exemplo completo:**
```python
try:
    analise = aguardar_estado_ia(**AGUARDAR_CSV, contexto=f"Rotina {CODIGO_ROTINA}")
except TimeoutError:
    logging.error("❌ Timeout")
    return "skip"

if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
    return "skip"
```

---

### `clicar_elemento_ia(...)`

Pede para a IA localizar um elemento na tela por descrição e clica nele. Substitui `clicar_imagem()`.

**Como usar:**
```python
clicou = clicar_elemento_ia(**CLICAR_CSV)
```

**O que retorna:**
- `True` → encontrou e clicou
- `False` → não encontrou no tempo limite

**Exemplo completo:**
```python
if not clicar_elemento_ia(**CLICAR_CSV):
    logging.error("❌ Não foi possível clicar no CSV")
    return "skip"
```

---

### `ESTADOS` — constantes de string

Dicionário com os estados que a IA pode retornar. Use para comparar o resultado de `aguardar_estado_ia()`.

| Chave | Valor | Significado |
|---|---|---|
| `ESTADOS["CSV_DISPONIVEL"]` | `"csv_disponivel"` | Botão CSV visível |
| `ESTADOS["PROCESSANDO"]` | `"processando"` | Tela carregando |
| `ESTADOS["SEM_DADOS"]` | `"sem_dados"` | Popup sem registros |
| `ESTADOS["ERRO"]` | `"erro"` | Mensagem de erro |
| `ESTADOS["ALERTA"]` | `"alerta"` | Qualquer popup aberto |
| `ESTADOS["PRONTO"]` | `"pronto"` | Tela limpa, formulário ok |
| `ESTADOS["DOWNLOAD_SALVAR"]` | `"download_salvar"` | Barra de download do Edge |
| `ESTADOS["DESCONHECIDO"]` | `"desconhecido"` | IA não reconheceu |

**Como usar:**
```python
if analise.get("estado") == ESTADOS["SEM_DADOS"]:
    return "skip"

if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
    return "skip"
```

---

### `relatorio_uso_tokens()` — chamada automática pelo executor

Loga o consumo total de tokens e custo estimado da sessão inteira. Chamada automaticamente pelo `executor.py` no fim de cada execução — você não precisa chamar nas rotinas.

**Caso queira chamar manualmente (ex: em testes):**
```python
from function.ai_vision import relatorio_uso_tokens
relatorio_uso_tokens()
```

**Exemplo de saída no log:**
```
──────────────────────────────────────────────────
🔢 CONSUMO DE TOKENS DA SESSÃO
   Chamadas realizadas : 34
   Erros de API        : 0
   Tokens de entrada   : 74.200
   Tokens de saída     : 3.100
   Total de tokens     : 77.300
   Custo estimado      : $0.268950 USD (~R$ 1.5330)
──────────────────────────────────────────────────
```

---

## Ações do `acoes.py`

As ações são dicionários prontos com `pergunta`, `estados_esperados`, `timeout` e `intervalo` já configurados. Use o spread `**` para passar tudo de uma vez.

---

### Ações de espera → `aguardar_estado_ia(**ACAO, contexto="...")`

| Ação | Quando usar | Timeout | Intervalo | Termina em |
|---|---|---|---|---|
| `AGUARDAR_CSV` | Maioria das rotinas — botão CSV no toolbar | 300s | 4s | csv_disponivel, sem_dados, alerta, erro |
| `AGUARDAR_CSV_PESADO` | Relatórios lentos (020304, 03013604_MES, 030237) | 600s | 8s | csv_disponivel, sem_dados, alerta, erro |
| `AGUARDAR_DOWNLOAD_SALVAR` | Barra de download do Edge com botão "Salvar ▼" (0111, 01250802) | 60s | 2s | download_salvar, erro |
| `AGUARDAR_SALVAR_BOTAO_PAGINA` | Botão Salvar dentro da própria página (0421, 01250802) | 180s | 4s | download_salvar, csv_disponivel, erro |
| `AGUARDAR_TODOS_0105070402` | Somente 0105070402 — aguarda checkbox "Todos" | 30s | 2s | pronto, erro |
| `AGUARDAR_CSV_GERADO_0105070402` | Somente 0105070402 — popup "CSV gerado com Sucesso!" | 120s | 3s | alerta, erro |
| `AGUARDAR_PROMAX_PRONTO` | Após `fechar_popups_inicio()` no main.py | 30s | 2s | pronto |

---

### Ações de clique → `clicar_elemento_ia(**ACAO)`

| Ação | Quando usar | Timeout |
|---|---|---|
| `CLICAR_CSV` | Maioria das rotinas — botão CSV do toolbar | 30s |
| `CLICAR_DOWNLOAD_SALVAR` | Botão "Salvar ▼" da barra de download do Edge | 30s |
| `CLICAR_SALVAR_BOTAO_PAGINA` | Botão "Salvar" dentro do corpo da página (0421) | 30s |
| `CLICAR_TODOS_0105070402` | Somente 0105070402 — checkbox "Todos" | 20s |
| `CLICAR_DUPLICADOS_0105070402` | Somente 0105070402 — checkbox "Duplicados" | 20s |
| `CLICAR_AS_0105070402` | Somente 0105070402 — checkbox "AS" | 20s |
| `CLICAR_GERAR_CSV_0105070402` | Somente 0105070402 — botão "Gerar CSV" | 20s |
| `CLICAR_OK_CSV_GERADO_0105070402` | Somente 0105070402 — botão OK no popup de sucesso | 20s |

---

## Padrão completo de uma rotina migrada

```python
"""
Rotina: XX.XX
"""
import logging
import pyautogui
from function.abrir_rotinas import abrir_rotinas
from function.ai_vision import aguardar_estado_ia, clicar_elemento_ia, ESTADOS
from function.acoes import AGUARDAR_CSV, CLICAR_CSV
from function.funcoes_rotina import aguardar_tela_carregar
from function.troca_janela import trocar_para_nova_janela
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CODIGO_ROTINA = "XXXX"

def executar(driver, **kwargs):

    # 1. Abre a rotina e troca de janela
    abrir_rotinas(driver, CODIGO_ROTINA)
    trocar_para_nova_janela(driver)
    driver.maximize_window()

    # 2. Aguarda carregar (Selenium — rápido, sem custo de API)
    wait = WebDriverWait(driver, 60)
    aguardar_tela_carregar(wait)

    # 3. Centraliza o mouse (mantém tela viva no VNC)
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(width / 2, height / 2)
    pyautogui.FAILSAFE = True

    # 4. Configura os parâmetros da rotina via Selenium
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "rotina")))
    # ... sua lógica de configuração aqui ...

    # 5. Dispara o relatório via JS
    driver.execute_script("return Visualizar();")  # ou GerarCsv(), GeraPlanilha()...

    # 6. IA aguarda o resultado
    try:
        analise = aguardar_estado_ia(**AGUARDAR_CSV, contexto=f"Rotina {CODIGO_ROTINA}")
    except TimeoutError:
        logging.error(f"❌ Timeout na rotina {CODIGO_ROTINA}")
        return "skip"

    if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
        logging.warning(f"⏭️ {analise.get('mensagem')} — pulando")
        return "skip"

    # 7. IA clica no CSV
    if not clicar_elemento_ia(**CLICAR_CSV):
        logging.error("❌ Não foi possível clicar no CSV")
        return "skip"

    logging.info("⏳ Aguardando download...")
    # executor.py chama salvar_arquivo() após o retorno
```

---

## Regras gerais

✅ Sempre envolva `aguardar_estado_ia()` em `try/except TimeoutError`  
✅ Sempre verifique o estado retornado antes de continuar  
✅ Use `AGUARDAR_CSV_PESADO` para relatórios que costumam demorar mais de 2 min  
✅ Use `contexto=` para facilitar o debug no log  
✅ Mantenha `aguardar_tela_carregar(wait)` — é Selenium puro, sem custo de API  

❌ Não use `time.sleep()` fixos — a IA aguarda pelo estado, não pelo tempo  
❌ Não importe mais `encontrar_imagem` / `clicar_imagem` nas rotinas migradas  
❌ Não deixe código comentado — o Git guarda o histórico  

---

## Quando e como criar uma nova ação no `acoes.py`

### Quando criar

✅ Uma rotina nova espera por um elemento que nenhuma ação existente cobre  
✅ Uma rotina precisa de timeout ou intervalo diferente das ações existentes  
✅ Você vai usar o mesmo texto de pergunta/descrição em 2 ou mais rotinas — se está copiando e colando entre rotinas, vire uma ação  
✅ Uma rotina tem fluxo visual próprio (como a 0105070402) — crie ações com sufixo do código  

❌ Não crie se só vai usar em um lugar e o texto é muito específico daquela tela — escreva a pergunta direto no `aguardar_estado_ia()` da rotina  
❌ Não crie se já existe uma ação que cobre o caso — reutilize  

---

### Como criar uma ação de espera

Adicione um dicionário no `acoes.py` com estas 4 chaves:

```python
AGUARDAR_MINHA_ACAO = {
    "pergunta": (
        "Descreva o que a IA deve procurar na tela. "
        "Mencione o texto do elemento, onde fica, "
        "e quais outros estados são possíveis nesse momento."
    ),
    "estados_esperados": ["csv_disponivel", "sem_dados", "erro"],
    "timeout": 120,   # segundos — quanto tempo esperar antes de desistir
    "intervalo": 4,   # segundos entre cada chamada à IA
}
```

**Dicas para o campo `pergunta`:**
- Mencione o texto exato do elemento se souber (`"botão com texto 'Exportar'"`)
- Mencione onde fica na tela (`"no canto superior direito"`)
- Liste os outros estados possíveis (`"se não houver dados, informe 'sem_dados'"`)
- Mais contexto = IA erra menos = menos chamadas = menos custo

**Referência de timeout e intervalo por velocidade do relatório:**

| Velocidade | Timeout | Intervalo |
|---|---|---|
| Rápido (< 1 min) | 120s | 3s |
| Normal (1–5 min) | 300s | 4s |
| Lento (5–10 min) | 600s | 8s |
| Muito lento (> 10 min) | 900s | 30s |

> Intervalo maior = menos chamadas à API = mais barato. Use intervalo pequeno só quando a resposta precisa ser imediata.

---

### Como criar uma ação de clique

```python
CLICAR_MINHA_ACAO = {
    "descricao": (
        "Descreva o elemento a ser clicado de forma que a IA consiga "
        "localizá-lo visualmente. Mencione: texto, cor, posição, formato."
    ),
    "timeout": 30,   # segundos para encontrar o elemento
}
```

**Dicas para o campo `descricao`:**
- Texto do botão sempre que possível (`"botão com texto 'Salvar'"`)
- Cor ou estilo se ajudar (`"botão azul escuro"`, `"botão verde"`)
- Posição relativa (`"no topo da página"`, `"na barra de ferramentas"`)
- O que **não** é, se houver risco de confusão: `"botão Salvar dentro da página — NÃO a barra de download do Edge"`

---

### Exemplo real — nova rotina com botão "Exportar XLSX"

No `acoes.py`:
```python
# --- Rotina 09XXXX ---
AGUARDAR_XLSX_09XXXX = {
    "pergunta": (
        "O relatório do Promax terminou de carregar? "
        "Procure um botão com o texto 'Exportar XLSX' na barra de ferramentas. "
        "Se não houver dados, informe 'sem_dados'."
    ),
    "estados_esperados": ["csv_disponivel", "sem_dados", "erro"],
    "timeout": 180,
    "intervalo": 5,
}

CLICAR_XLSX_09XXXX = {
    "descricao": (
        "botão 'Exportar XLSX' na barra de ferramentas do relatório Promax. "
        "Fica no topo da página ao lado de outros botões de exportação."
    ),
    "timeout": 30,
}
```

Na rotina `09XXXX.py`:
```python
from function.acoes import AGUARDAR_XLSX_09XXXX, CLICAR_XLSX_09XXXX

analise = aguardar_estado_ia(**AGUARDAR_XLSX_09XXXX, contexto=f"Rotina {CODIGO_ROTINA}")
clicar_elemento_ia(**CLICAR_XLSX_09XXXX)
```

---

## Quando e como criar uma nova função no `ai_vision.py`

### Quando criar

O `ai_vision.py` já cobre os cenários principais:
- `aguardar_estado_ia` → esperar algo aparecer
- `clicar_elemento_ia` → clicar em algo
- `fechar_popups_inicio` → tratar popups do login
- `diagnosticar_e_decidir` → analisar falhas

Crie uma nova função somente se:

✅ Uma sequência de passos visuais se repete em várias rotinas  
✅ Você precisa de comportamento diferente do loop padrão (ex: comparar dois screenshots)  
✅ Você adicionou um tipo de interação novo (scroll, arrastar, digitação guiada por IA)  
✅ Você quer encapsular lógica de retry customizada  

❌ Não crie se dá para resolver com `aguardar_estado_ia` + `clicar_elemento_ia` normalmente  
❌ Não crie se a lógica é específica de uma única rotina — nesse caso fica na própria rotina  
❌ Não crie se é só variação de pergunta/timeout — nesse caso é uma ação no `acoes.py`  

---

### Como criar

Adicione na seção **"Funções de alto nível"** do `ai_vision.py`:

```python
def minha_nova_funcao(parametro1, contexto: str = "") -> tipo_retorno:
    """
    Uma linha explicando o que faz.

    Quando usar:
        Descreva o cenário específico.

    Args:
        parametro1: O que é.
        contexto:   Info extra para o log.

    Returns:
        Descreva o que retorna.
    """
    logging.info(f"... iniciando | {contexto}")

    # REGRA DE OURO: sempre use analisar_tela() — nunca chame
    # client.messages.create() diretamente fora dela.
    # Isso garante que o contador de tokens registre tudo corretamente.

    analise = analisar_tela("sua pergunta aqui")

    # trate os casos e retorne algo claro
    return resultado
```

---

### Exemplo real — função que aguarda CSV e já clica

Cenário: você percebeu que em 80% das rotinas o padrão é sempre aguardar CSV → checar dados → clicar CSV. Faz sentido virar uma função:

```python
def aguardar_e_clicar_csv(contexto: str = "") -> bool:
    """
    Aguarda o CSV ficar disponível e já clica nele.

    Quando usar:
        Rotinas padrão onde o fluxo é sempre:
        gerar relatório → esperar CSV → clicar CSV.
        Substitui as 3 chamadas separadas por uma só.

    Returns:
        True se clicou no CSV, False se não havia dados ou deu erro.
    """
    from function.acoes import AGUARDAR_CSV, CLICAR_CSV

    try:
        analise = aguardar_estado_ia(**AGUARDAR_CSV, contexto=contexto)
    except TimeoutError:
        logging.error(f"❌ Timeout aguardando CSV | {contexto}")
        return False

    if analise.get("estado") in (ESTADOS["SEM_DADOS"], ESTADOS["ERRO"]):
        logging.warning(f"⏭️ {analise.get('mensagem')} | {contexto}")
        return False

    return clicar_elemento_ia(**CLICAR_CSV)
```

Na rotina:
```python
from function.ai_vision import aguardar_e_clicar_csv

if not aguardar_e_clicar_csv(contexto=f"Rotina {CODIGO_ROTINA}"):
    return "skip"
```

---

### Resumo — onde cada coisa vai

| Mudança | Onde mexe |
|---|---|
| Novo texto de pergunta ou descrição | `acoes.py` — nova ação |
| Novo timeout ou intervalo | `acoes.py` — nova ação |
| Novo comportamento ou lógica de decisão | `ai_vision.py` — nova função |
| Sequência repetida em várias rotinas | `ai_vision.py` — nova função |
| Lógica específica de uma única rotina | Na própria rotina |
