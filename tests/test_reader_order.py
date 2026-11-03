"""D66: the family-A reader's --order required gives back the factory's schema. data-v12's rows are written with
sort_keys, so each stored schema has its properties in alphabetical order; the guided decoder writes keys in the schema's
order, and the model was trained on answers in the factory's order (read_rules_v3.schema). The reader cannot import the
engine (readers/ stays self-contained), so its function is taken from the file's source."""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as data  # noqa: E402
import read_rules_v3 as v3  # noqa: E402


def reader_function(name):
    tree = ast.parse((ROOT / "readers/leitor_a_modal.py").read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    ns = {}
    exec(compile(ast.Module([fn], type_ignores=[]), "readers/leitor_a_modal.py", "exec"), ns)
    return ns[name]


def orders(s, path="$"):
    """Each object's property order, by path."""
    out = {}
    if isinstance(s, dict):
        if isinstance(s.get("properties"), dict):
            out[path] = list(s["properties"])
        for k, v in s.items():
            out.update(orders(v, f"{path}.{k}"))
    elif isinstance(s, list):
        for i, v in enumerate(s):
            out.update(orders(v, f"{path}[{i}]"))
    return out


def test_order_required_gives_back_the_factory_schema():
    in_answer_order = reader_function("in_answer_order")
    arts = {f"{data.TASK}:{ex['id']}": ex for pattern, _ in data.SOURCES for ex in data.load(pattern)}
    n = 0
    for name in ("dev", "sealed", "dev_antigo"):
        for line in (ROOT / f"training/data-v12/regra_lida/{name}.jsonl").read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            ex = arts[r["id"]]
            want = v3.schema(data.ctx_of(ex), ex["tipo"])
            assert orders(r["schema"]) != orders(want), r["id"]  # stored alphabetised: the reason for --order
            got = in_answer_order(r["schema"])
            assert got == want and orders(got) == orders(want), r["id"]
            assert list(json.loads(r["answer"])) == list(got["properties"]), r["id"]
            n += 1
    assert n == 593


def test_order_required_leaves_a_schema_in_order_as_it_is():
    in_answer_order = reader_function("in_answer_order")
    s = {"type": "object", "properties": {"b": {"type": "string"}, "a": {"type": "object", "properties": {"y": {}, "x": {}}, "required": ["y", "x"]}},
         "required": ["b", "a"]}
    assert json.dumps(in_answer_order(s)) == json.dumps(s)
