from datetime import datetime, timedelta

def data_hoje():
    hoje = datetime.today()
    data_formatada = hoje.strftime('%d/%m/%Y')
    return data_formatada

def data_ontem():
    hoje = datetime.today()
    ontem = hoje - timedelta(days=1)
    data_formatada = ontem.strftime('%d/%m/%Y')
    return data_formatada

def primeiro_dia_mes():
    hoje = datetime.today()
    primeiro_dia = hoje.replace(day=1)
    data_formatada = primeiro_dia.strftime('%d/%m/%Y')
    return data_formatada