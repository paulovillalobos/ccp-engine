"""D81: the holidays are the days Código do Trabalho art. 234.º n.º 1 names in its text in force; a name the code
cannot place stops it instead of counting a holiday as a working day."""
import datetime

import pytest

from engine import calendario as cal

TEXT = ("1 - São feriados obrigatórios os dias 1 de janeiro, de Sexta-Feira Santa, de Domingo de Páscoa, 25 de abril, 1 de maio, "
        "de Corpo de Deus, 10 de junho, 15 de agosto, 5 de outubro, 1 de novembro, 1, 8 e 25 de dezembro.")
D = datetime.date


def test_easter():
    assert [cal.easter(y) for y in (2024, 2025, 2026)] == [D(2024, 3, 31), D(2025, 4, 20), D(2026, 4, 5)]


def test_the_thirteen_days_of_2026():
    h = cal.holidays(TEXT, 2026)
    assert len(h) == 13
    assert {D(2026, 4, 3), D(2026, 4, 5), D(2026, 6, 4), D(2026, 12, 1), D(2026, 12, 8), D(2026, 12, 25)} <= set(h)


def test_next_working_day():
    text_of = lambda y: TEXT  # noqa: E731
    assert cal.next_working_day(D(2026, 4, 3), text_of) == D(2026, 4, 6)  # Good Friday, then the weekend
    assert cal.next_working_day(D(2026, 11, 4), text_of) == D(2026, 11, 4)


def test_an_unknown_day_stops_the_count():
    with pytest.raises(cal.Unreadable):
        cal.holidays(TEXT.replace("de Corpo de Deus", "de Dia do Município"), 2026)
    with pytest.raises(cal.Unreadable):
        cal.holidays("Não há feriados.", 2026)
