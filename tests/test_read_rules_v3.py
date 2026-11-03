"""D66: the reading protocol v3's checker on the real law. Answers for targets already settled (or closed by L12) pass;
broken copies carrying the mistakes the readers made in rounds 1-5 fail. Test fixtures for the checker only: never a
reading, never training data, never shown to a reader."""
import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import read_rules_v3 as v  # noqa: E402
from engine.store import Store  # noqa: E402


@pytest.fixture(scope="module")
def law():
    return v.Law(Store([ROOT / "law"]).load())


def S(texto, de):
    return [{"texto": texto, "de": de}]


def C(field, op, value, fontes):
    return {"field": field, "op": op, "value": value, "fontes": fontes}


def prazo(conds, days, field, frm, f_days, f_field, f_from, usual=None, f_usual=None):
    return {"tipo": "prazo_minimo", "condicoes": conds, "params": {"minimum_days": days, "deadline_field": field, "counted_from": frm, "usual_days": usual},
            "fontes": {"minimum_days": f_days, "deadline_field": f_field, "counted_from": f_from, "usual_days": f_usual}}


CLPQ3 = "ccp:parte-ii.titulo-iii.capitulo-iii"
CASES = {
    ("ccp:art174.2", "prazo_minimo"): {"regras": [prazo(
        [C("tipo_procedimento", "eq", "concurso_limitado_previa_qualificacao", S("Concurso limitado por prévia qualificação", CLPQ3)),
         C("publicado_joue", "eq", True, S("seja publicado no Jornal Oficial da União Europeia", "ccp:art174.1")),
         C("urgencia_fundamentada", "eq", True, S("uma situação de urgência devidamente fundamentada", "ccp:art174.2"))],
        15, "prazo_candidaturas_dias", "data_envio_anuncio", S("pode ser reduzido para 15 dias", "ccp:art174.2"),
        S("apresentação das candidaturas", "ccp:art174.1"), S("a contar da data do envio desse anúncio", "ccp:art174.1"))], "nao_tipavel": None},
    ("ccp:art190.1", "prazo_minimo"): {"regras": [
        prazo([C("tipo_procedimento", "eq", "concurso_limitado_previa_qualificacao", S("concurso limitado por prévia qualificação", "ccp:art190.1")),
               C("publicado_joue", "eq", False, S("não seja publicado no Jornal Oficial da União Europeia", "ccp:art190.1")),
               C("tipo_contrato", "ne", "obras", S("contrato de empreitada de obras públicas", "ccp:art190.1"))],
              6, "prazo_propostas_dias", "data_envio_convite", S("inferior a seis dias", "ccp:art190.1"),
              S("apresentação das propostas", "ccp:art190.1"), S("a contar da data do envio do convite", "ccp:art190.1")),
        prazo([C("tipo_procedimento", "eq", "concurso_limitado_previa_qualificacao", S("concurso limitado por prévia qualificação", "ccp:art190.1")),
               C("publicado_joue", "eq", False, S("não seja publicado no Jornal Oficial da União Europeia", "ccp:art190.1")),
               C("tipo_contrato", "eq", "obras", S("contrato de empreitada de obras públicas", "ccp:art190.1"))],
              14, "prazo_propostas_dias", "data_envio_convite", S("inferior a 14 dias", "ccp:art190.1"),
              S("apresentação das propostas", "ccp:art190.1"), S("a contar da data do envio do convite", "ccp:art190.1"))], "nao_tipavel": None},
    ("ccp:art219-b.5", "prazo_minimo"): {"regras": [
        prazo([C("tipo_procedimento", "eq", "concurso_concecao", S("Concurso de concepção", "ccp:parte-ii.titulo-iv.capitulo-i")),
               C("modalidade_concecao", "in", ["limitado", "publico"], S("nos concursos público e limitado", "ccp:art219-b.5"))],
              30, "prazo_trabalhos_concecao_dias", "nao_indicado", S("não pode ser inferior a 30 dias", "ccp:art219-b.5"),
              S("documentos que materializam os trabalhos de conceção", "ccp:art219-b.5"), None),
        prazo([C("tipo_procedimento", "eq", "concurso_concecao", S("Concurso de concepção", "ccp:parte-ii.titulo-iv.capitulo-i")),
               C("modalidade_concecao", "eq", "simplificado", S("no concurso simplificado", "ccp:art219-b.5"))],
              15, "prazo_trabalhos_concecao_dias", "nao_indicado", S("e 15 dias, no concurso simplificado", "ccp:art219-b.5"),
              S("documentos que materializam os trabalhos de conceção", "ccp:art219-b.5"), None)], "nao_tipavel": None},
    ("ccp:art219-j.3", "prazo_minimo"): {"regras": [prazo(
        [C("tipo_procedimento", "eq", "concurso_ideias", S("Concurso de ideias", "ccp:art219-j"))],
        60, "prazo_propostas_dias", "data_publicacao_anuncio", S("não pode ser inferior a 60 dias", "ccp:art219-j.3"),
        S("apresentação de propostas", "ccp:art219-j.3"), S("a partir da data de publicação do anúncio", "ccp:art219-j.3"))], "nao_tipavel": None},
    ("ccp:art19.d", "limiar"): {"regras": [{"tipo": "limiar", "condicoes": [
        C("tipo_procedimento", "eq", "ajuste_direto", S("Ajuste direto", "ccp:art19.d")),
        C("tipo_contrato", "eq", "obras", S("contratos de empreitadas de obras públicas", "ccp:art19"))],
        "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 150000, "currency": "EUR"}},
        "fontes": {"field": S("valor estimado do contrato", "ccp:art19.d"), "comparator": S("inferior a", "ccp:art19.d"), "value": S("150 000 €", "ccp:art19.d")}}],
        "nao_tipavel": None},
    ("ccp:art135.1", "prazo_minimo"): {"regras": [
        prazo([C("tipo_procedimento", "eq", "concurso_publico", S("concurso público", "ccp:art135.1")),
               C("publicado_joue", "eq", False, S("não seja publicado no Jornal Oficial da União Europeia", "ccp:art135.1")),
               C("tipo_contrato", "ne", "obras", S("contrato de empreitada de obras públicas", "ccp:art135.1"))],
              6, "prazo_propostas_dias", "data_envio_anuncio", S("inferior a seis dias", "ccp:art135.1"),
              S("apresentação das propostas", "ccp:art135.1"), S("a contar da data do envio, para publicação, do anúncio", "ccp:art135.1")),
        prazo([C("tipo_procedimento", "eq", "concurso_publico", S("concurso público", "ccp:art135.1")),
               C("publicado_joue", "eq", False, S("não seja publicado no Jornal Oficial da União Europeia", "ccp:art135.1")),
               C("tipo_contrato", "eq", "obras", S("contrato de empreitada de obras públicas", "ccp:art135.1"))],
              14, "prazo_propostas_dias", "data_envio_anuncio", S("a 14 dias", "ccp:art135.1"),
              S("apresentação das propostas", "ccp:art135.1"), S("a contar da data do envio, para publicação, do anúncio", "ccp:art135.1"))], "nao_tipavel": None},
    ("ccp:art88.2.a", "limiar"): {"regras": [], "nao_tipavel": {
        "motivo": "nao_e_limiar", "fontes": S("Pode não ser exigida prestação de caução", "ccp:art88.2"),
        "falta": "o valor dispensa a caução; não é o limite até ao qual um procedimento pode ser escolhido"}},
}


def broken(key, reading, ctx):
    """Copies with the mistakes seen in rounds 1-5."""
    out = []

    def mut(name, fn):
        r = copy.deepcopy(reading)
        fn(r)
        out.append((name, r))

    def r0(r):
        return r["regras"][0]
    alvo_text = ctx["allowed"][key[0]]
    viz = [pid for pid, role in ctx["roles"].items() if role == "vizinho"]
    if key[1] == "prazo_minimo":
        mut("a fact the text does not deny, set false", lambda r: r0(r)["condicoes"].append(C("urgencia_fundamentada", "eq", False, S(alvo_text[:12], key[0]))))
        mut("the reference date as a condition (v11, 198.1)", lambda r: r0(r)["condicoes"].append(C("data_inicio_procedimento", "eq", "2026-10-01", S(alvo_text[:12], key[0]))))
        mut("contract types the text does not name (v11, 174.3)", lambda r: r0(r)["condicoes"].append(C("tipo_contrato", "not_in", ["concessao_obras", "concessao_servicos"], S(alvo_text[:20], key[0]))))
        mut("a procedure the text does not name (v11, 241-B)", lambda r: r0(r)["condicoes"].__setitem__(0, C("tipo_procedimento", "eq", "dialogo_concorrencial", r0(r)["condicoes"][0]["fontes"])))
        mut("days from another number", lambda r: r0(r)["params"].__setitem__("minimum_days", r0(r)["params"]["minimum_days"] + 7))
        mut("the wrong starting point", lambda r: r0(r)["params"].__setitem__("counted_from", "data_publicacao_anuncio" if r0(r)["params"]["counted_from"] != "data_publicacao_anuncio" else "data_envio_convite"))
        if viz:
            mut("a quote from a neighbouring number", lambda r: r0(r)["condicoes"][0]["fontes"].__setitem__(0, {"texto": ctx["allowed"][viz[-1]][:25], "de": viz[-1]}))
    elif reading["regras"]:
        mut("the comparator changed (127.º-C)", lambda r: r0(r)["params"]["threshold"].__setitem__("comparator", "le"))
        mut("a value from outside the text (Reader B, 20.º n.º 1 b): 140 000)", lambda r: r0(r)["params"]["threshold"].__setitem__("value", r0(r)["params"]["threshold"]["value"] + 10000))
        mut("preço base for valor estimado", lambda r: r0(r)["params"]["threshold"].__setitem__("field", "preco_base"))
        mut("a contract type the text does not name (v11, 31.4)", lambda r: r0(r)["condicoes"][1].__setitem__("value", "servicos"))
    else:
        mut("a limiar without its procedure (88.º n.º 2 a), settled in round 5)", lambda r: (r.__setitem__("nao_tipavel", None), r.__setitem__("regras", [
            {"tipo": "limiar", "condicoes": [], "params": {"threshold": {"field": "preco_contratual", "comparator": "lt", "value": 1000000, "currency": "EUR"}},
             "fontes": {"field": S("preço contratual", "ccp:art88.2.a"), "comparator": S("inferior a", "ccp:art88.2.a"), "value": S("1 000 000 €", "ccp:art88.2.a")}}])))
        mut("a reason outside the list", lambda r: r["nao_tipavel"].__setitem__("motivo", "outro"))
    return out


@pytest.mark.parametrize("key", sorted(CASES))
def test_correct_answers_pass_and_broken_copies_fail(law, key):
    ctx = v.context(law, key[0], "2026-10-01")
    assert v.check(CASES[key], ctx, key[1]) == []
    for name, r in broken(key, CASES[key], ctx):
        assert v.check(r, ctx, key[1]), name


def test_a_quote_cut_from_a_longer_phrase_fails(law):
    ctx = v.context(law, "ccp:art31.4", "2026-10-01")
    reading = {"regras": [{"tipo": "limiar", "condicoes": [
        C("tipo_procedimento", "in", ["ajuste_direto", "consulta_previa"], S("consulta prévia ou ajuste direto", "ccp:art31.4")),
        C("tipo_contrato", "eq", "servicos", S("serviços", "ccp:art31.4"))],
        "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}},
        "fontes": {"field": S("valor estimado do contrato", "ccp:art31.4"), "comparator": S("inferior a", "ccp:art31.4"), "value": S("1 000 000 €", "ccp:art31.4")}}],
        "nao_tipavel": None}
    assert any("parte de uma expressão" in e for e in v.check(reading, ctx, "limiar"))


def test_the_prompt_example_passes_and_its_broken_copies_fail():
    assert v.selftest()
