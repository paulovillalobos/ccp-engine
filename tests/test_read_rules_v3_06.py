"""D83: protocol 0.6 adds the contagem_prazo type and follows an article reference to the act it names; a 0.5 prompt
renders as before. The checker accepts each counting aspect only in the law's own words."""
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import read_rules_v3 as v3  # noqa: E402
from engine.store import Store  # noqa: E402

LAW = v3.Law(Store([ROOT / "law"]).load())
DATE = "2026-10-01"


def ctx(pid, version=v3.V06):
    return v3.context(LAW, pid, DATE, version=version)


def one(field, aspecto, valor, quote, de, dq=None, dde=None, conditions=()):
    return {"regras": [{"tipo": "contagem_prazo", "condicoes": list(conditions), "params": {"deadline_field": field, "aspecto": aspecto, "valor": valor},
                        "fontes": {"aspecto": [{"texto": quote, "de": de}], "deadline_field": [{"texto": dq, "de": dde}] if dq else None}}], "nao_tipavel": None}


def test_a_reference_to_another_code_goes_to_that_code_in_06_only():
    assert ("cpa:art87", "epigrafe") in ctx("ccp:art470.1")["refs"]
    assert ("ccp:art87", "epigrafe") in ctx("ccp:art470.1", v3.V05)["refs"]


def test_each_aspect_in_the_law_s_words():
    c = ctx("ccp:art470.3")
    ok = one("prazo_propostas_dias", "fins_de_semana", "continuo", "são contínuos", "ccp:art470.3", "apresentação das propostas", "ccp:art470.3")
    assert v3.check(ok, c, "contagem_prazo", v3.V06) == []
    wrong = copy.deepcopy(ok); wrong["regras"][0]["params"]["valor"] = "suspende"
    assert v3.check(wrong, c, "contagem_prazo", v3.V06)
    bad_pair = copy.deepcopy(ok); bad_pair["regras"][0]["params"]["valor"] = "transfere"
    assert any("não tem o valor" in e for e in v3.check(bad_pair, c, "contagem_prazo", v3.V06))


def test_todos_quotes_deadlines_in_general_or_nothing():
    c = ctx("cpa:art87.b")
    q = "Não se inclui na contagem o dia em que ocorra o evento a partir do qual o prazo começa a correr"
    assert v3.check(one("todos", "primeiro_dia", "nao_conta", q, "cpa:art87.b"), c, "contagem_prazo", v3.V06) == []
    general = one("todos", "primeiro_dia", "nao_conta", q, "cpa:art87.b", "À contagem dos prazos", "cpa:art87")
    assert v3.check(general, c, "contagem_prazo", v3.V06) == []


def test_05_prints_none_of_06():
    c5 = ctx("ccp:art470.3", v3.V05)
    assert "contagem_prazo" not in v3.render(c5, "prazo_minimo", v3.V05) and "nao_e_contagem" not in v3.render(c5, "prazo_minimo", v3.V05)
    assert "contagem_prazo —" in v3.render(ctx("ccp:art470.3"), "contagem_prazo", v3.V06)
