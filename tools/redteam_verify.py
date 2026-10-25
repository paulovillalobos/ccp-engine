"""Red-team mutations the twelve broken overlays do not cover (audit of 2026-10-24). Each MISSED line is a gap in verify.py;
closing one means adding the check and turning the mutation into a fixtures/broken overlay. Run: .venv/bin/python tools/redteam_verify.py"""
import json, shutil, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT))
import verify
V = ROOT / "fixtures/valid"
PRAZO = "veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json"
LIM = "regra/ccp-limiar-ajuste-direto-bens.json"

MISSED = []

def run(name, mutate):
    with tempfile.TemporaryDirectory() as tmp:
        s = Path(tmp) / "s"; shutil.copytree(V, s)
        mutate(s)
        _, out = verify.check_store([s])
        codes = sorted({c for c, _ in out})
        print(f"{'CAUGHT ' if out else 'MISSED '} {name}: {codes}")
        if not out:
            MISSED.append(name)

def edit(s, rel, fn):
    p = s / rel; o = json.loads(p.read_text()); fn(o); p.write_text(json.dumps(o, ensure_ascii=False))

run("M01 verdict manifest.package does not contain the verdict's rule", lambda s: edit(s, PRAZO, lambda o: o["manifest"].update(package="pacote:ccp@2026-09-30") if False else o["manifest"].update(package="pacote:ccp@2026-09-30")))
# prazo IS in the old package; use limiar verdict instead
run("M01b limiar verdict with manifest.package = old package (limiar not in it)", lambda s: edit(s, "veredicto/limiar-ajuste-direto-bens-FX-2026-000001.json", lambda o: o["manifest"].update(package="pacote:ccp@2026-09-30")))
run("M02 verdict names rule revision 2 that does not exist", lambda s: edit(s, PRAZO, lambda o: o["rule"].update(revision=2)))
run("M03 verdict valid_at before the cited passage version was in force", lambda s: edit(s, PRAZO, lambda o: o.update(valid_at="2026-09-15")))
run("M04 verdict uses a fact of another unit", lambda s: edit(s, PRAZO, lambda o: o.update(unit="contrato:base:99000001")))
def m05(s):
    from engine.canon import content_hash
    def fn(o):
        o["rules"].append({"id": "regra:ccp:proibicao-fracionamento@v1", "revision": 1}); o["rules"].sort(key=lambda r: r["id"]); o["hash"] = content_hash(o["rules"])
    edit(s, "pacote/ccp-2026-10-01.json", fn)
run("M05 package names a rule whose state is proposed", m05)
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
# Added while implementing A3b (2026-10-24): each is a way around a check that a weaker version would have let through.
run("M24 disputa adjudicated by a registered pessoa that the log does not name (the disputant)", lambda s: edit(s, "disputa/fx-1.json", lambda o: o["adjudication"].update(by="pessoa:paulo")))
run("M25 conflito records a value its fact does not carry", lambda s: edit(s, "conflito/proc-base-FX-2026-000001-preco_base.json", lambda o: o["values"][0].update(value=99)))
run("M26 manifest source snapshot names bytes no raw record has", lambda s: edit(s, PRAZO, lambda o: o["manifest"]["source_snapshots"][0].update(sha256="c" * 64)))
run("M27 verdict uses base-dump facts but its manifest lists only base-api", lambda s: edit(s, PRAZO, lambda o: o["manifest"].update(adapters=["adaptador:base-api@1"])))
run("M28 afirmacao conversion_evento points at the link proposal", lambda s: edit(s, "afirmacao/proc-base-FX-2026-000001-regime.json", lambda o: o.update(conversion_evento="evento:17")))
run("M29 unit kind inversion: the contract's parent relabelled mod", lambda s: edit(s, "unidade/proc-base-FX-2026-000001.json", lambda o: o.update(kind="mod")))
run("M30 passage version closes before it opens", lambda s: edit(s, "passagem/ccp-art136.1.json", lambda o: o["versions"][0].update(valid_to="2026-09-01")))
run("M31 rule open-ended while the version it cites closes", lambda s: edit(s, "passagem/ccp-art16.1.json", lambda o: o["versions"][0].update(valid_to="2027-01-01")))
run("M32 package log_head the log never had", lambda s: edit(s, "pacote/ccp-2026-10-01.json", lambda o: o.update(log_head="d" * 64)))
run("M33 fact read from a source field its adapter maps to another field", lambda s: edit(s, "facto/proc-base-FX-2026-000001-prazo_propostas_dias-base-dump.json", lambda o: o["origin"].update(field="precoBase")))
run("M34 manifest law_version disagrees with its package", lambda s: edit(s, PRAZO, lambda o: o["manifest"].update(law_version="lei:ccp@2026-09-30")))
run("M35 verdict result flipped to nao_cumpre with the same facts", lambda s: edit(s, PRAZO, lambda o: o.update(result="nao_cumpre", detail="prazo_propostas_dias=9 < 6")))
run("M36 conflito moved to the child contract (no longer the unit the verdict reads)", lambda s: edit(s, "conflito/proc-base-FX-2026-000001-preco_base.json", lambda o: o.update(unit="contrato:base:99000001")))
# audit of phase 1 (2026-10-24)
run("N3 verdict omits an entity with a role on the unit's lineage", lambda s: edit(s, PRAZO, lambda o: o.update(entities=o["entities"][:1])))
run("N4 verdict lists an entity with no role on the unit", lambda s: edit(s, PRAZO, lambda o: o["entities"].append({"id": "ent:cand:PT:fornecedor-fixture-unipessoal", "type": "privada", "role": "concorrente"})))
run("N5 verdict cites a passage version marked revoked", lambda s: edit(s, "passagem/ccp-art136.1.json", lambda o: o["versions"][0].update(revoked=True)))
def _gap(o):
    v0 = dict(o["versions"][0]); v0.update(version="2020-01-01", valid_from="2020-01-01", valid_to="2024-01-01"); o["versions"].insert(0, v0)
run("N6 gap between passage versions", lambda s: edit(s, "passagem/ccp-art136.1.json", _gap))
def _stale_entity(s):
    e = json.loads((V / "entidade/nif-500000000.json").read_text()); e.update(revision=2, supersedes=1, stale=True, stale_reason="dup", recorded_at="2026-10-24T21:00:00Z")
    (s / "entidade/nif-500000000-r2.json").write_text(json.dumps(e))
run("N9 settled link to an entity whose head revision is stale", _stale_entity)
run("N11 verdict known_at earlier than the log head it claims", lambda s: edit(s, PRAZO, lambda o: o.update(known_at="2026-10-24T19:05:00Z", recorded_at="2026-10-24T19:05:00Z", id=o["id"].replace("19:30:00Z", "19:05:00Z"))))
# phase 4 (2026-10-25): D41 — a retired principal's events count only up to retired_at
def _retire(at):
    def fn(s):
        p = s / "governance/principals.json"; d = json.loads(p.read_text())
        for e in d["principals"]:
            if e["id"] == "leitor:b":
                e.update(retired=True, retired_at=at)
        p.write_text(json.dumps(d, ensure_ascii=False))
    return fn
run("P1 leitor:b retired before the events it signed (retired_at earlier than its first event)", _retire("2026-10-24T19:00:00Z"))
run("P2 leitor:b retired with no retired_at: none of its events may count", lambda s: _retire(None)(s) or (lambda p: p.write_text(json.dumps({"principals": [{k: v for k, v in e.items() if k != "retired_at"} for e in json.loads(p.read_text())["principals"]]})))(s / "governance/principals.json"))
# phase 4 (T1): training data must be the generator's output
run("Q1 a listed training file deleted", lambda s: (s / "training/data/nota_dr/train.jsonl").unlink())
run("Q2 an unlisted file dropped into training/data", lambda s: (s / "training/data/nota_dr/extra.jsonl").write_text("{}\n"))
run("Q3 the reservation file edited after generation (an article un-reserved)", lambda s: edit(s, "training/TRAIN-HELD-OUT.json", lambda o: o.update(reserved_articles=o["reserved_articles"][1:])))
print(f"{len(MISSED)} MISSED")
sys.exit(1 if MISSED else 0)
