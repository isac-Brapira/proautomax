import importlib
import pkgutil
import rotinas


def carregar_rotinas():
    registradas = {}

    for module_info in pkgutil.walk_packages(
        rotinas.__path__,
        rotinas.__name__ + "."
    ):
        module = importlib.import_module(module_info.name)

        if hasattr(module, "CODIGO_ROTINA") and hasattr(module, "executar"):
            registradas[module.CODIGO_ROTINA] = module.executar

    return registradas
