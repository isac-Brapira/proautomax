"""
ProAutoMax - Catálogo de Ações
================================
Centraliza todos os prompts e configurações de IA em um único lugar.
Ao mudar um prompt, todas as rotinas que o usam são afetadas automaticamente.

USO NAS ROTINAS:
    from function.acoes import AGUARDAR_CSV, CLICAR_CSV
    
    analise = aguardar_estado_ia(**AGUARDAR_CSV, contexto=f"Rotina {CODIGO_ROTINA}")
    clicar_elemento_ia(**CLICAR_CSV)

ESTRUTURA DE CADA AÇÃO:
    - Ações de ESPERA  → usadas com aguardar_estado_ia()
    - Ações de CLIQUE  → usadas com clicar_elemento_ia()
    - Ações de STARTUP → usadas com fechar_popups_inicio()
"""


# ===========================================================================
# AÇÕES DE ESPERA — usadas com aguardar_estado_ia(**ACAO, contexto="...")
# ===========================================================================

# ---------------------------------------------------------------------------
# Download / Exportação
# ---------------------------------------------------------------------------

AGUARDAR_CSV = {
    # Maioria das rotinas: aguarda o botão CSV aparecer no toolbar do relatório
    "estados_esperados": ["csv_disponivel", "sem_dados", "alerta", "erro"],
    "timeout": 300,
    "intervalo": 4,
    "pergunta": (
        "O relatório já foi gerado no Promax? "
        "Procure um botão pequeno com o texto 'CSV' na barra de ferramentas do relatório. "
        "Se não houver dados ou aparecer uma mensagem de 'sem registros', informe 'sem_dados'. "
        "Se houver um popup/dialog aberto, informe 'alerta'."
    ),
}

AGUARDAR_CSV_PESADO = {
    # Relatórios lentos (020304, 03013604_MES, 030237): timeout maior, intervalo maior = menos chamadas = menos custo
    "estados_esperados": ["csv_disponivel", "sem_dados", "alerta", "erro"],
    "timeout": 600,
    "intervalo": 8,
    "pergunta": (
        "O relatório já foi gerado no Promax? "
        "Procure um botão pequeno com o texto 'CSV' na barra de ferramentas do relatório. "
        "Se não houver dados ou aparecer uma mensagem de 'sem registros', informe 'sem_dados'. "
        "Se houver um popup/dialog aberto, informe 'alerta'."
    ),
}

AGUARDAR_DOWNLOAD_SALVAR = {
    # Aguarda a barra de download do Edge aparecer com o botão "Salvar" (dropdown)
    # Aparece após clicar em CSV na maioria das rotinas
    "estados_esperados": ["download_salvar", "erro"],
    "timeout": 60,
    "intervalo": 2,
    "pergunta": (
        "A barra de download do Edge apareceu na parte inferior da tela? "
        "Procure um botão 'Salvar' com uma seta de dropdown ao lado. "
        "Essa barra aparece quando um arquivo está sendo baixado."
    ),
}

AGUARDAR_SALVAR_BOTAO_PAGINA = {
    # Aguarda botão "Salvar" dentro da própria página (rotina 0421 e 01250802)
    # É diferente da barra de download — fica no corpo da tela como botão de formulário
    "estados_esperados": ["download_salvar", "csv_disponivel", "erro"],
    "timeout": 180,
    "intervalo": 4,
    "pergunta": (
        "Apareceu um botão 'Salvar' na tela? "
        "Pode ser: (1) um botão 'Salvar' simples dentro da página do relatório, "
        "ou (2) a barra de download do Edge na parte inferior com botão 'Salvar'. "
        "Informe qual dos dois é visível e as coordenadas do botão."
    ),
}


# ---------------------------------------------------------------------------
# Rotina 0105070402 — Cliente Plus (fluxo próprio com imagens específicas)
# ---------------------------------------------------------------------------

AGUARDAR_TODOS_0105070402 = {
    # Aguarda o checkbox "Todos" aparecer no formulário de filtro
    "estados_esperados": ["pronto", "erro"],
    "timeout": 30,
    "intervalo": 2,
    "pergunta": (
        "Na tela do Promax, está visível um checkbox ou opção chamada 'Todos' "
        "em um formulário de seleção de clientes? "
        "O formulário deve conter opções como 'Todos', 'Duplicados', 'AS'."
    ),
}

AGUARDAR_CSV_GERADO_0105070402 = {
    # Aguarda o popup "CSV gerado com Sucesso!" aparecer
    "estados_esperados": ["alerta", "erro"],
    "timeout": 120,
    "intervalo": 3,
    "pergunta": (
        "Apareceu um popup/dialog com a mensagem 'CSV gerado com Sucesso!' ou similar? "
        "É uma janela pequena do sistema com um botão 'OK'."
    ),
}


# ===========================================================================
# AÇÕES DE CLIQUE — usadas com clicar_elemento_ia(**ACAO)
# ===========================================================================

CLICAR_CSV = {
    # Clica no botão CSV pequeno na barra de ferramentas do relatório
    # Presente na maioria das rotinas após o relatório carregar
    "descricao": (
        "botão com o texto 'CSV' (pode aparecer como 'CSV', 'Csv' ou 'csv') "
        "na barra de ferramentas horizontal do relatório Promax. "
        "Essa barra fica logo abaixo do cabeçalho azul da página e contém os botões: "
        "Pode também aparecer na parte inferior da tela"
        "O botão CSV é pequeno, branco com borda cinza, e fica entre o 'Salvar' e o 'PDF'. "
        "NÃO é o botão 'Salvar', NÃO é a barra de download do Edge na parte inferior da tela."
    ),
    "timeout": 30,
}

CLICAR_DOWNLOAD_SALVAR = {
    # Clica no botão "Salvar" da barra de download do Edge
    # Aparece na parte inferior da janela quando um arquivo está sendo baixado
    "descricao": (
        "botão 'Salvar' na barra de download do Microsoft Edge. "
        "Fica na parte inferior da tela, tem uma seta de dropdown ao lado. "
        "Clique na parte esquerda do botão (não na seta)."
    ),
    "timeout": 30,
}

CLICAR_SALVAR_BOTAO_PAGINA = {
    # Clica no botão "Salvar" que fica dentro do corpo da página (rotina 0421)
    # Diferente da barra de download — é um botão de formulário
    "descricao": (
        "botão 'Salvar' dentro da página do relatório Promax. "
        "Não é a barra de download do Edge — é um botão que aparece no corpo da tela "
        "após o relatório ser processado."
    ),
    "timeout": 30,
}


# ---------------------------------------------------------------------------
# Rotina 0105070402 — ações específicas em sequência
# ---------------------------------------------------------------------------

CLICAR_TODOS_0105070402 = {
    "descricao": (
        "checkbox ou opção 'Todos' no formulário de filtro de clientes do Promax. "
        "Deve ser marcado/clicado para selecionar todos os registros."
    ),
    "timeout": 20,
}

CLICAR_DUPLICADOS_0105070402 = {
    "descricao": (
        "checkbox 'Duplicados' no formulário de filtro de clientes do Promax. "
        "Fica abaixo do checkbox 'Todos'."
    ),
    "timeout": 20,
}

CLICAR_AS_0105070402 = {
    "descricao": (
        "checkbox 'AS' no formulário de filtro de clientes do Promax. "
        "É um checkbox de seleção de tipo de cliente, fica no formulário de filtros."
    ),
    "timeout": 20,
}

CLICAR_GERAR_CSV_0105070402 = {
    "descricao": (
        "botão 'Gerar CSV' no formulário do Promax. "
        "É um botão escuro/azul com o texto 'Gerar CSV', usado para iniciar a geração do arquivo."
    ),
    "timeout": 20,
}

CLICAR_OK_CSV_GERADO_0105070402 = {
    "descricao": (
        "botão 'OK' no popup 'CSV gerado com Sucesso!' do Promax. "
        "É uma janela de confirmação pequena com uma mensagem de sucesso e um botão OK."
    ),
    "timeout": 20,
}


# ===========================================================================
# STARTUP — popups imprevisíveis pós-login
# ===========================================================================

# Contexto descritivo para a IA entender o que pode aparecer na tela ao iniciar o Promax.
# Usado pela função fechar_popups_inicio() no aceitar_alertas.py
CONTEXTO_POPUPS_INICIO = (
    "O sistema Promax acabou de fazer login. "
    "Às vezes aparecem popups ou dialogs de configuração inicial que precisam ser fechados. "
    "Geralmente são janelas que aparecem no meio da tela, com um botão de fechar ou confirmar. "
    "Podem ser: \n"
    "  - Popups com filtros/dropdowns (Conta, Depto, NBZ, VBZ, Pacote) com opção 'Todos'\n"
    "  - Alertas JS do sistema (mensagens de aviso)\n"
    "  - Janelas de boas-vindas ou notificações\n"
    "  - Qualquer dialog com botão OK, Fechar, Confirmar\n"
    "Se a tela principal do Promax estiver limpa (tela toda branca, sem pop-ups visíveis ou menu lateral de navegação e menu lateral direito com campo de busca), "
    "a inicialização está concluída."
)

AGUARDAR_PROMAX_PRONTO = {
    # Usado após fechar todos os popups — confirma que o Promax está pronto para uso
    "estados_esperados": ["pronto"],
    "timeout": 30,
    "intervalo": 2,
    "pergunta": (
        "O Promax está com a tela principal carregada e sem nenhum popup aberto? "
        "A tela principal deve mostrar o menu lateral com as opções do sistema "
        "e um campo de atalho/busca de rotinas."
    ),
}