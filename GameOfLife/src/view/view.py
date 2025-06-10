from pygame_gui.elements import UIButton, UITextEntryLine

from src.utils.visuals import GridPanel


class BaseView:

    """
    Reprezentuje interfejs graficzny widoczny dla użytkownika.
    Jego metody pozwalają manipulowac elementami, z którymi użytkownik
    wchodzi bezpośrednio w interakcję. Niezalecane jest implementowanie
    w nim skomplikowanej logiki biznesowej.
    """

    def __init__(self, alive_colour, dead_colour,
                 setup_grd: GridPanel, display_grd: GridPanel,
                 start_btn: UIButton, stop_btn: UIButton, pause_btn: UIButton, clear_btn: UIButton,
                 alive_entry: UITextEntryLine, dead_entry: UITextEntryLine):
        """
        Args:
            alive_colour (tuple): Kolor żywych komórek, wyrażony jako krotka z rgb
            dead_colour (tuple): Kolor martwych komórek, wyrażony jako krotka z rgb
            setup_grd (GridPanel): Plansza, na której użytkownik może modyfikować stan początkowy gry
            display_grd (GridPanel): Plansza, na której wyświetlana jest animacja
            start_btn (UIButton): Przycisk do uruchamiania animacji
            stop_btn (UIButton): Przycisk do zakończenia animacji
            pause_btn (UIButton): Przycisk do przerwania animacji
            clear_btn (UIButton): Przycisk do czyszczenia planszy do ustawiania stanu początkowego
            alive_entry (UITextEntryLine): Okno do wprowadzania wartości przy jakich ilościach żywych "sąsiadów" komórka pozostaje żywa
            dead_entry (UITextEntryLine): Okno do wprowadzania wartości przy jakich ilościach żywych "sąsiadów" martwa komórka ożywa
        """
        self.alive_colour = alive_colour
        self.dead_colour = dead_colour
        self.setup_grd = setup_grd
        self.display_grd = display_grd
        self.start_btn = start_btn
        self.stop_btn = stop_btn
        self.pause_btn = pause_btn
        self.clear_btn = clear_btn
        self.alive_entry = alive_entry
        self.dead_entry = dead_entry
        self.display_alive_colour = alive_colour
        self.display_dead_colour = dead_colour

    def set_inverted(self, inverted: bool):
        """
        Funkcja ustawia negatyw na planszy wyświetlającej animację.

        Args:
            inverted (bool): czy ma być negatyw
        """
        raise NotImplementedError()

    def set_display_alive(self, row: int, column: int, alive: bool):
        """
        Ustawia stan komórki o danych koordynatach na planszy z animacją.

        Args:
            row (int): wiersz, w którym znajduje się komórka
            column (int): kolumna, w której znajduje się komórka
            alive (bool): czy ma być żywa
        """
        raise NotImplementedError()

    def set_setup_alive(self, row: int, column: int, alive: bool):
        """
        Ustawia stan komórki o danych koordynatach na planszy ze stanem wejściowym.

        Args:
            row (int): wiersz, w którym znajduje się komórka
            column (int): kolumna, w której znajduje się komórka
            alive (bool): czy ma być żywa
        """
        raise NotImplementedError()

    def update_display_size(self, rows: int, columns: int):
        """
        Ustawia wymiary planszy z animacją.

        Args:
            rows (int): nowa ilość wierszy planszy
            columns (int): nowa ilość kolumn planszy
        """
        raise NotImplementedError()

    def update_setup_size(self, rows: int, columns: int):
        """
        Ustawia wymiary planszy ze stanem wejśćiowym.

        Args:
            rows (int): nowa ilość wierszy planszy
            columns (int): nowa ilość kolumn planszy
        """
        raise NotImplementedError()

    def clear_display_board(self):
        """
        Ustawia wszystkie komórki planszy z animacją na martwe.
        """
        raise NotImplementedError()

    def clear_setup_board(self):
        """
        Ustawia wszystkie komórki planszy ze stanem wejściowym na martwe.
        """
        raise NotImplementedError()

    def set_stay_alive_counts(self, counts: str):
        """
        Ustawia wyświetlane ilości żywych "sąsiadów", przy których komórka pozostaje żywa.
        Ilości są przyjmowane w postaci napisu, a metoda nie ma na celu walidacji
        informacji w nich wprowadzonych.
        """
        raise NotImplementedError()

    def set_revive_counts(self, counts: str):
        """
        Ustawia wyświetlane ilości żywych "sąsiadów", przy których martwa komórka ożywa.
        Ilości są przyjmowane w postaci napisu, a metoda nie ma na celu walidacji
        informacji w nich wprowadzonych.
        """
        raise NotImplementedError()

    def set_speed_display(self, speed: float):
        """
        Ustawia wyświetlaną częstotliwość aktualizacji obrazu (w sekundach).

        Args:
            speed (float): Wyświetlana częstotliwość aktualizacji obrazu (w sekundach)
        """
        raise NotImplementedError


class PygameView(BaseView):

    def __init__(self, alive_colour, dead_colour,
                 setup_grd: GridPanel, display_grd: GridPanel,
                 start_btn: UIButton, stop_btn: UIButton, pause_btn: UIButton, clear_btn: UIButton,
                 alive_entry, dead_entry):
        super().__init__(alive_colour, dead_colour,
                         setup_grd, display_grd,
                         start_btn, stop_btn, pause_btn, clear_btn,
                         alive_entry, dead_entry)

    def set_inverted(self, inverted: bool):
        for r in range(self.display_grd.rows):
            for c in range(self.display_grd.columns):
                f = self.display_grd.get_field_by_index(r, c)
                if f.fill_colour == self.alive_colour:
                    f.set_fill_colour(self.dead_colour)
                else:
                    f.set_fill_colour(self.alive_colour)
        if inverted:
            self.display_alive_colour = self.dead_colour
            self.display_dead_colour = self.alive_colour
        else:
            self.display_alive_colour = self.alive_colour
            self.display_dead_colour = self.dead_colour

    def set_display_alive(self, row: int, column: int, alive: bool):
        if alive:
            self.display_grd.get_field_by_index(row, column).set_fill_colour(self.display_alive_colour)
        else:
            self.display_grd.get_field_by_index(row, column).set_fill_colour(self.display_dead_colour)

    def set_setup_alive(self, row: int, column: int, alive: bool):
        if alive:
            self.setup_grd.get_field_by_index(row, column).set_fill_colour(self.alive_colour)
        else:
            self.setup_grd.get_field_by_index(row, column).set_fill_colour(self.dead_colour)

    def update_display_size(self, rows: int, columns: int):
        self.display_grd.set_rows(rows)
        self.display_grd.set_columns(columns)

    def update_setup_size(self, rows: int, columns: int):
        self.setup_grd.set_rows(rows)
        self.setup_grd.set_columns(columns)

    def clear_display_board(self):
        for r in range(self.display_grd.rows):
            for c in range(self.display_grd.columns):
                self.display_grd.get_field_by_index(r, c).set_fill_colour(self.display_dead_colour)

    def clear_setup_board(self):
        for r in range(self.setup_grd.rows):
            for c in range(self.setup_grd.columns):
                self.setup_grd.get_field_by_index(r, c).set_fill_colour(self.dead_colour)

    def set_stay_alive_counts(self, counts: str):
        self.alive_entry.set_text(counts)

    def set_revive_counts(self, counts: str):
        self.dead_entry.set_text(counts)