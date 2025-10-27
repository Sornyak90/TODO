class Missing(Exception):
    """
    Исключение, вызванное ситуацией нехватки важного компонента.
    Attributes:
        msg (str): Сообщение об ошибке, описывающее причину возникновения исключения.
    """
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class Duplicate(Exception):
    """
    Исключение, вызванное попыткой создания дублирующей записи.
    Attributes:
        msg (str): Сообщение об ошибке, описывающее причину возникновения исключения.
    """
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg