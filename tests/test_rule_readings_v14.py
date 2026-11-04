"""D68: data-v14's practice on the real law keeps the exam out. No practice row shows a target still open, an article that
holds one, or a passage close to one; a passage's own row passes the factory's checker again with the protocol 0.4 (build
checks each moved copy against its moved text), and the copies' gold has other numbers than the passage's own."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import make_rule_readings_v14 as data  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

STORE = v12.m.Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
LAW = v3.Law(STORE)
ROWS, REJECTED, PER = data.build(STORE)


def test_no_row_shows_the_exam():
    exam_arts = {LAW.article_of(p) for p in data.EXAM}
    for r in ROWS:
        assert not any(f"[{p}]" in r["prompt"] for p in data.EXAM), r["id"]
        assert not {LAW.article_of(s) for s in r["sources"] if s.startswith("ccp:art")} & exam_arts, r["id"]


def test_the_readings_left_out_say_why():
    assert set(REJECTED) == {"regra:ccp:auto-prazo-minimo-art174-1@v1", "regra:ccp:auto-prazo-minimo-art174-2@v1",
                             "regra:ccp:limiar-ajuste-direto-obras@v2", "regra:ccp:limiar-consulta-previa-obras@v1",
                             "regra:ccp:limiar-consulta-previa-obras@v2"}
    assert "close to one" in REJECTED["regra:ccp:limiar-ajuste-direto-obras@v2"]  # 19.º d) reads like the exam's 21.º n.º 1 c)


def test_own_rows_pass_the_checker_and_copies_move_the_numbers():
    tipo = {pid: ex["tipo"] for pid, ex in data.passages(LAW)[0].items()}
    by = {}
    for r in ROWS:
        pid = r["id"].split(":real:", 1)[1].rsplit(":", 1)[0]
        body = json.loads(r["answer"])
        if r["id"].endswith(":00"):
            assert v3.check(body, v3.context(LAW, pid, data.DATE), tipo[pid], data.PROTOCOL) == [], r["id"]
        by.setdefault(pid, []).append(body)
    for pid, bodies in by.items():
        if bodies[0]["regras"]:
            values = {json.dumps([x["params"] for x in b["regras"]], sort_keys=True) for b in bodies}
            assert len(values) > len(bodies) // 2, pid  # the copies have other numbers than the passage's own
    assert all(x["rows"] == data.VARIANTS + 1 for x in PER.values())
