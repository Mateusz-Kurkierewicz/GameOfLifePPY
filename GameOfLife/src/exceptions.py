class InvalidArgumentException(Exception):

    """
    Wyjątek ten zostaje podniesiony w momencie podania argumentów o nieprawidłowych
    wartościach lub typach
    """

    def __init__(self, msg: str):
        """
        Args:
            msg (str): Wiadomość, która zostanie wyświetlona w momencie podniesienia wyjątku
        """
        self.msg = msg

    def __str__(self):
        return self.msg