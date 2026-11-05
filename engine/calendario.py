"""The national holidays a date falls on, read from the text of the law in force (DECISIONS D81): Código do Trabalho
art. 234.º n.º 1 («São feriados obrigatórios os dias …»). The caller passes that passage's text as it read on the date;
nothing here reads the store or the network.

    holidays(text, year) -> {date: name}     the fixed days the text names, and the three movable ones by Easter
    working_day(d, text_of) -> bool          not a Saturday, a Sunday or a holiday (text_of(year) gives the text)
    next_working_day(d, text_of) -> date     d itself when it is one

A text that names a day this code cannot place (a name it does not know) raises Unreadable: the caller reads that as a
missing fact, never as a day without holidays. Local holidays (n.º 2, the municipal ones) and the Monday moves of n.º 3
are not in the text of n.º 1 and are not counted.
"""
import datetime
import re

VERSION = "ccp-calendario-0.1"
MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
          "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
MOVABLE = {"sexta-feira santa": -2, "domingo de páscoa": 0, "corpo de deus": 60, "carnaval": -47}  # days from Easter Sunday


class Unreadable(ValueError):
    pass


def easter(year):
    """Easter Sunday of the Gregorian calendar (the anonymous algorithm, as published by Butcher)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    return datetime.date(year, month, (h + l - 7 * m + 114) % 31 + 1)


def holidays(text, year):
    m = re.search(r"São feriados obrigatórios os dias (.+?)\.(?:\s|$)", text or "", re.S)
    if not m:
        raise Unreadable("the text does not say «São feriados obrigatórios os dias …»")
    out, days = {}, []
    for part in re.split(r",\s*|\s+e\s+", m.group(1)):
        part = part.strip()
        if not part:
            continue
        fixed = re.fullmatch(r"(\d{1,2})(?: de (\w+))?", part)
        if fixed:
            days.append(int(fixed.group(1)))
            if fixed.group(2):
                month = MONTHS.get(fixed.group(2).lower())
                if month is None:
                    raise Unreadable(f"month «{fixed.group(2)}»")
                for day in days:
                    out[datetime.date(year, month, day)] = f"{day} de {fixed.group(2)}"
                days = []
            continue
        name = re.sub(r"^de\s+", "", part).lower()
        if name not in MOVABLE:
            raise Unreadable(f"day «{part}»")
        out[easter(year) + datetime.timedelta(days=MOVABLE[name])] = re.sub(r"^de\s+", "", part)
    if days:
        raise Unreadable(f"days {days} without a month")
    return out


def working_day(d, text_of):
    return d.weekday() < 5 and d not in holidays(text_of(d.year), d.year)


def next_working_day(d, text_of):
    while not working_day(d, text_of):
        d += datetime.timedelta(days=1)
    return d
