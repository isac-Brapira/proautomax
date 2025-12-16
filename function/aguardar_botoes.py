def aguardar_botoes_rotina(wait, driver):
    wait.until(
        lambda d: d.execute_script(
            "return document.getElementById('DivBtReservado') && "
            "document.getElementById('DivBtReservado').children.length > 0"
        )
    )