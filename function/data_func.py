from datetime import datetime, timedelta
hoje = datetime.today()

MESES = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARCO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO"
}

def data_hoje():
    data_formatada = hoje.strftime('%d/%m/%Y')
    return data_formatada

def data_ontem():
    ontem = hoje - timedelta(days=1)
    data_formatada = ontem.strftime('%d/%m/%Y')
    return data_formatada

def primeiro_dia_mes():
    primeiro_dia = hoje.replace(day=1)
    data_formatada = primeiro_dia.strftime('%d/%m/%Y')
    return data_formatada

def gerar_nome_mes_vigente():
    # Dict lookup is safer than locale on Windows to avoid 'MARÇO' (encoding) issues
    return f"{hoje.month:02d}.{MESES[hoje.month]}"

def ano_vigente():
   return datetime.today().strftime("%Y") 