# ➕ Como criar uma nova rotina

## Criar um novo arquivo em rotinas/<categoria>/<codigo>.py

### Adicionar

```python
CODIGO_ROTINA


função executar(driver, **kwargs)

Não é necessário registrar manualmente (loader automático)

Exemplo:

CODIGO_ROTINA = "010111"

def executar(driver, **kwargs):
```

## ⚠️ Observações importantes

Todas as pastas devem conter __init__.py

O sistema deve ser executado a partir da raiz

## Boas práticas

- Não usar sleep

- Sempre validar abertura da tela

- Isolar lógica em funções auxiliares

- Não tratar exceções silenciosamente
