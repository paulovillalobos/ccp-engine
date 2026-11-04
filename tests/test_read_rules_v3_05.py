"""D71: protocol 0.5 adds the prazo_maximo type and the EU directives' procedure names without changing what an earlier
prompt says: every recorded 0.4 prompt of rounds 9-11 re-renders byte for byte, its schema and context too. The checker
accepts a maximum quoted with its days and refuses one whose quote states no maximum; the engine says «não cumpre» to a
deadline set above the maximum."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402
from engine import evaluate, rules as rules_mod  # noqa: E402
from engine.store import Store  # noqa: E402

CTX = {"alvo": "exemplo:art5.2", "article": "exemplo:art5",
       "roles": {"exemplo:art5.2": "alvo", "exemplo:art5": "epigrafe", "exemplo:cap-i": "titulo"},
       "allowed": {"exemplo:art5.2": "2 - Os concorrentes podem pronunciar-se por escrito no prazo de cinco dias a contar da data da notificação do projeto de decisão.",
                   "exemplo:art5": "Audiência prévia", "exemplo:cap-i": "Capítulo I — Concurso público"}}
MAX = {"regras": [{"tipo": "prazo_maximo",
                   "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico", "fontes": [{"texto": "Concurso público", "de": "exemplo:cap-i"}]}],
                   "params": {"maximum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "data_notificacao"},
                   "fontes": {"maximum_days": [{"texto": "no prazo de cinco dias", "de": "exemplo:art5.2"}],
                              "deadline_field": [{"texto": "pronunciar-se", "de": "exemplo:art5.2"}],
                              "counted_from": [{"texto": "a contar da data da notificação", "de": "exemplo:art5.2"}]}}], "nao_tipavel": None}


def test_earlier_prompts_render_as_recorded():
    store = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    law, n = v3.Law(store), 0
    for rnd in (9, 10, 11):
        for t in rf.targets(store, rnd):
            f = rf.FROUNDS[rnd]["dir"] / rf.rr.slug(t["rule"]) / "prompt.json"
            body = json.loads(f.read_text(encoding="utf-8"))
            ver = body.get("protocol_version")
            ctx = v3.context(law, t["source_passage"], t["date"])
            assert body["prompt"] == v3.render(ctx, t["type"], ver), t["rule"]
            assert body["schema"] == v3.schema(ctx, t["type"], ver), t["rule"]
            n += 1
    assert n >= 80


def test_04_prints_none_of_05():
    s4 = json.dumps(v3.schema(CTX, "prazo_minimo", v3.V04), ensure_ascii=False)
    s5 = json.dumps(v3.schema(CTX, "prazo_minimo", v3.V05), ensure_ascii=False)
    assert "concurso_aberto" not in s4 and "nao_e_prazo_maximo" not in s4
    assert "concurso_aberto" in s5 and "nao_e_prazo_maximo" in s5
    assert "prazo_maximo" not in v3.vocab_text(v3.V04) and "prazo_maximo" in v3.vocab_text(v3.V05)


def test_checker_on_a_maximum():
    assert v3.check(MAX, CTX, "prazo_maximo", v3.V05) == []
    wrong = copy.deepcopy(MAX)
    wrong["regras"][0]["params"]["maximum_days"] = 10
    assert v3.check(wrong, CTX, "prazo_maximo", v3.V05)
    bare = copy.deepcopy(MAX)
    bare["regras"][0]["fontes"]["maximum_days"] = [{"texto": "cinco dias", "de": "exemplo:art5.2"}]
    assert any("máximo" in e for e in v3.check(bare, CTX, "prazo_maximo", v3.V05))
    assert v3.selftest()


def test_engine_evaluates_a_maximum():
    from tests.test_most_specific import prazo, rule, run
    assert rules_mod.REQUIRED_PARAMS["prazo_maximo"] == ("maximum_days", "deadline_field", "counted_from")
    base = prazo()
    r = rule(base, "regra:teste:maximo@v1", [], maximum_days=5, deadline_field="prazo_pronuncia_dias")
    r["type"] = "prazo_maximo"
    del r["params"]["minimum_days"]
    r["params"].pop("usual_days", None)
    assert run([r], prazo_pronuncia_dias=5)["regra:teste:maximo@v1"]["result"] == "cumpre"
    assert run([r], prazo_pronuncia_dias=10)["regra:teste:maximo@v1"]["result"] == "nao_cumpre"
    assert run([r])["regra:teste:maximo@v1"]["reason"] == "facto_ausente"
    assert evaluate.most_specific  # prazo_maximo rules of one field also give the most specific verdict (D66)
