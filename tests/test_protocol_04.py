"""D67: the reading protocol 0.4 next to 0.3. A 0.3 prompt renders byte for byte as data-v12 stored it, so verify regenerates
data-v12 and its measurement as they were; 0.4 prints every law phrase the checker accepts (C6), says in L5 and L10 what 0.3
left to the reader, and reads an anaphoric start in the passage it is quoted from (L9)."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import read_rules_v3 as v3  # noqa: E402


def articles():
    return {f"{v12.TASK}:{ex['id']}": ex for pattern, _ in v12.SOURCES for ex in v12.load(pattern)}


def test_protocol_03_renders_as_data_v12_stored_it():
    arts, n = articles(), 0
    for name in ("dev", "sealed", "dev_antigo"):
        for line in (ROOT / f"training/data-v12/regra_lida/{name}.jsonl").read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            ex = arts[r["id"]]
            assert v3.render(v12.ctx_of(ex), ex["tipo"], v3.V03) == r["prompt"], r["id"]
            n += 1
    assert n == 593


def test_protocol_04_prints_every_phrase_the_checker_accepts():
    t, t3 = v3.vocab_text(), v3.vocab_text(v3.V03)
    for table in ("deadline_fields", "counted_from", "threshold_fields"):
        for ws in v3.VOC[table].values():
            assert all(f"«{w}»" in t for w in ws), ws
    for field in ("tipo_contrato", "tipo_entidade"):
        for ws in v3.VOC["condition_fields"][field]["values"].values():
            assert all(f"«{w}»" in t for w in ws), ws
    assert not all(f"«{w}»" in t3 for ws in v3.VOC["deadline_fields"].values() for w in ws)


def test_protocol_04_says_what_03_left_to_the_reader():
    ctx = v12.ctx_of(next(iter(v12.load("eval3-01.jsonl"))))
    new, old = v3.render(ctx, "prazo_minimo"), v3.render(ctx, "prazo_minimo", v3.V03)
    for line in (v3.L5_04, v3.L10_04):
        assert line in new and line not in old


def test_an_anaphoric_start_is_read_in_its_passage():
    ex = next(e for e in v12.load("v4-01.jsonl") if e["id"] == "v4-01-092")  # «… o convite fixa um prazo … contados do seu envio»
    (answer, ctx), errs = v12.problems(ex, v3.VERSION)
    assert not errs
    a = copy.deepcopy(answer)
    a["regras"][0]["fontes"]["counted_from"] = [{"texto": "contados do seu envio", "de": a["regras"][0]["fontes"]["counted_from"][0]["de"]}]
    assert not v3.check(a, ctx, ex["tipo"])
    assert any("counted_from" in e for e in v3.check(a, ctx, ex["tipo"], v3.V03))
