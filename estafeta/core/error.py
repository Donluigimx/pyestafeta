

class EstafetaWrongData(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)


class EstafetaEmptyField(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)
