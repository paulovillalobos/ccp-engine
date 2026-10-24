"""Red-team mutations the twelve broken overlays do not cover (audit of 2026-10-24). Each MISSED line is a gap in verify.py;
closing one means adding the check and turning the mutation into a fixtures/broken overlay. Run: .venv/bin/python tools/redteam_verify.py"""
import json, shutil, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT))
import verify
V = ROOT / "fixtures/valid"
PRAZO = "veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json"
LIM = "regra/ccp-limiar-ajuste-direto-bens.json"

def run(name, mutate):
    with tempfile.TemporaryDirectory() as tmp:
        s = Path(tmp) / "s"; shutil.copytree(V, s)
        mutate(s)
        _, out = verify.check_store([s])
        codes = sorted({c for c, _ in out})
        print(f"{'CAUGHT ' if out else 'MISSED '} {name}: {codes}")

def edit(s, rel, fn):
    p = s / rel; o = json.loads(p.read_text()); fn(o); p.write_text(json.dumps(o, ensure_ascii=False))

run("M01 verdict manifest.package does not contain the verdict's rule", lambda s: edit(s, PRAZO, lambda o: o["manifest"].update(package="pacote:ccp@2026-09-30") if False else o["manifest"].update(package="pacote:ccp@2026-09-30")))
# prazo IS in the old package; use limiar verdict instead
run("M01b limiar verdict with manifest.package = old package (limiar not in it)", lambda s: edit(s, "veredicto/limiar-ajuste-direto-bens-FX-2026-000001.json", lambda o: o["manifest"].update(package="pacote:ccp@2026-09-30")))
run("M02 verdict names rule revision 2 that does not exist", lambda s: edit(s, PRAZO, lambda o: o["rule"].update(revision=2)))
run("M03 verdict valid_at before the cited passage version was in force", lambda s: edit(s, PRAZO, lambda o: o.update(valid_at="2026-09-15")))
run("M04 verdict uses a fact of another unit", lambda s: edit(s, PRAZO, lambda o: o.update(unit="contrato:base:99000001")))
run("M05 package includes a rule in state proposed", lambda s: None)  # fixture already does (agregada, proibicao) -> inspect separately
run("M06 manifest.log_head is not the log's head", lambda s: edit(s, PRAZO, lambda o: o["manifest"].update(log_head="a" * 64)))
run("M07 reading chose passages the rule does not cite", lambda s: edit(s, LIM, lambda o: o["readings"][1].update(chosen_passages=["ccp:art113.2"])))
run("M08 fact valid_at after the verdict's valid_at", lambda s: edit(s, "facto/proc-base-FX-2026-000001-prazo_propostas_dias-base-dump.json", lambda o: o.update(valid_at="2026-11-01")))
run("M09 link settled by an AI with no event and no approval", lambda s: edit(s, "link/fx-2.json", lambda o: o.update(state="settled")))
run("M10 adaptador state settled with no log event", lambda s: edit(s, "adaptador/base-dump-1.json", lambda o: o.update(state="settled")))
run("M11 vigencia valid_from matches no version of its passage", lambda s: edit(s, "vigencia/ccp-art20.1.a@2026-10-01.json", lambda o: o.update(id="ccp:art20.1.a@2026-11-01", valid_from="2026-11-01")))
run("M12 conflito over a field its facts do not carry", lambda s: edit(s, "conflito/proc-base-FX-2026-000001-preco_base.json", lambda o: o.update(field="prazo_propostas_dias")))
run("M13 unit parent cycle (proc points to its contract)", lambda s: edit(s, "unidade/proc-base-FX-2026-000001.json", lambda o: o.update(kind="lote", parent="contrato:base:99000001")))
run("M14 orphan raw bytes file", lambda s: (s / "raw_bytes" / ("b" * 64)).write_text("orphan"))
run("M15 passage versions overlap in time", lambda s: edit(s, "passagem/ccp-art20.1.a.json", lambda o: o["versions"].append(dict(o["versions"][0], version="2026-09-01", valid_from="2026-09-01"))))
run("M16 verdict result cumpre whose facts contradict it (prazo 3 < 6)", lambda s: edit(s, "facto/proc-base-FX-2026-000001-prazo_propostas_dias-base-dump.json", lambda o: o.update(value=3)))
run("M17 verdict cites a passage the rule does not cite", lambda s: edit(s, PRAZO, lambda o: o["citation"].update(passage="ccp:art20.1", quote="A escolha do ajuste direto permite a celebração de contratos", offsets={"start": 4, "end": 63})))
run("M18 fact field not in any adapter mapping of its adapter", lambda s: edit(s, "facto/proc-base-FX-2026-000001-prazo_propostas_dias-base-dump.json", lambda o: o.update(field="prazo_inventado")))
run("M19 regra valid_from after the passage version it cites entered force", lambda s: edit(s, LIM, lambda o: o.update(valid_from="2027-01-01")))
run("M20 two current revisions of a rule with different content, same state", lambda s: edit(s, LIM, lambda o: o.update(revision=2, supersedes=1, title="v2")) or shutil.copy(V / LIM, s / "regra/ccp-limiar-r1.json"))
run("M21 caso_referencia held_out true with frozen_at null", lambda s: edit(s, "caso_referencia/fx-1.json", lambda o: o.update(held_out=True)))
run("M22 disputa object says adjudicated by X but log says Y", lambda s: edit(s, "disputa/fx-1.json", lambda o: o["adjudication"].update(by="human:paulo")))
run("M23 entidade pessoa_singular typed as privada in the verdict", lambda s: edit(s, PRAZO, lambda o: o["entities"][1].update(type="privada", name="Fornecedor Fixture Unipessoal")))
