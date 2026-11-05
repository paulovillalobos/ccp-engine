"""Phase 19 data (DECISIONS D76): data-v16, for v16 trained from v15's adapter.

    .venv/bin/python tools/make_rule_readings_v16.py check | generate

- keys: every practice-stratum target the log holds settled in rounds 11–14 (round 13 re-reads round 12, round 14 round 11:
  the same strata), each with VARIANTS copies of its numbers moved, by data-v15's code (tools/make_rule_readings_v15.py); the exam (every
  reservado target) stays out, as do keys whose reader sees a reserved article or an exam passage.
- written: NEW_WRITTEN invented articles in the one shape v15 misread on round 13's practice targets (studied there only,
  never on the exam): an interested party's deadline for an act the vocabulary holds no field for (corrections, samples,
  a revised work plan…), asked for a prazo_maximo: L12 sem_vocabulario, not nao_e_prazo_maximo («não é para apresentar
  nada» is the entity's own act, a duration, an obligation to keep); and KEEP_V15 of data-v15's written rows by sha256 of the id.
- remind: REMIND of data-v15's remind rows (v14's practice, v13's articles) by sha256 of the id.
Every row is rendered and checked with the protocol 0.5. Nothing here calls a model.
"""
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import make_rule_readings_v13 as v13  # noqa: E402
import make_rule_readings_v15 as v15  # noqa: E402
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402

VERSION = "ccp-make-rule-readings-v16-0.1"
DATA = ROOT / "training/data-v16"
KEY_STRATA = {11: "texto_visto", 12: "pratica", 13: "pratica", 14: "texto_visto"}
NEW_WRITTEN = 300
KEEP_V15 = 450
REMIND = 300
VARIANTS = 7  # data-v15 moved each key's numbers 24 times for 77 keys; with ~240 keys 7 copies each keep the file under GitHub's 100 MB
SEED = "D76"
PARTY_NO_FIELD = [("Os concorrentes suprem as irregularidades formais das suas propostas", "o suprimento de irregularidades das propostas"),
                  ("Os concorrentes entregam as amostras exigidas no programa do procedimento", "a entrega de amostras"),
                  ("O empreiteiro apresenta o plano de trabalhos ajustado", "a apresentação do plano de trabalhos ajustado"),
                  ("O adjudicatário apresenta os comprovativos dos requisitos de capacidade técnica e financeira", "a apresentação dos comprovativos de capacidade"),
                  ("O cocontratante apresenta a lista atualizada dos subcontratados", "a apresentação da lista de subcontratados"),
                  ("O adjudicatário confirma por escrito os compromissos assumidos por terceiros", "a confirmação dos compromissos de terceiros"),
                  ("O empreiteiro apresenta a proposta de preço para os trabalhos complementares", "a proposta de preço dos trabalhos complementares"),
                  ("Os candidatos regularizam os documentos da fase de qualificação", "a regularização dos documentos de qualificação")]


def new_written():
    rng = random.Random(SEED)
    out = []
    for k in range(NEW_WRITTEN):
        subject, act = rng.choice(PARTY_NO_FIELD)
        d = rng.randint(3, 30)
        m = rng.choice(["no prazo de", "no prazo máximo de", "até"])
        dt = v15.days_text(d, rng)
        cf = rng.choice(["a contar da notificação para o efeito", "a contar da data da notificação", "contados da receção do pedido"])
        target = f"{subject} {m} {dt} {cf}."
        fonte = target[:target.index(dt) + len(dt)]
        place, _ = rng.choice(v15.CCP_PLACES)
        texts = [target, rng.choice(v15.FILLERS)] if rng.random() < 0.5 else [rng.choice(v15.FILLERS), target]
        out.append(v15.article(f"w16-semvoc-{k:03d}", "prazo_maximo", ["Título III — Tramitação procedimental", place], "Prazos dos interessados",
                               v15.numbered(texts, False), texts.index(target) + 1,
                               {"regras": [], "nao_tipavel": {"motivo": "sem_vocabulario", "fonte": fonte,
                                                              "falta": f"O vocabulário não prevê um campo de prazo para {act}."}, "estilo": "w16-sem-vocabulario"}))
    return out


def new_rows(store):
    law = v3.Law(store)
    ex_texts = [x for x in (law.text(p, rf.DATE) for p in v15.exam(store)) if x]
    rows, rejected = [], {}
    with v3._using(v15.PROTOCOL):
        for ex in new_written():
            try:
                ctx = v12.ctx_of(ex)
                if v12.close(ctx["allowed"][ctx["alvo"]], ex_texts):
                    rejected[ex["id"]] = "close to an exam passage"; continue
                answer = v12.derive(ex, ctx)
            except (v12.Gap, KeyError, ValueError, IndexError) as exc:
                rejected[ex["id"]] = f"gold: {exc}"; continue
            errs = v3.check(answer, ctx, ex["tipo"], v15.PROTOCOL)
            if errs:
                rejected[ex["id"]] = f"checker: {errs[0]}"; continue
            rows.append(v15.row(ex["id"], ex["tipo"], ctx, answer, ex["estilo"]))
    return rows, rejected


def by_hash(rows, n):
    return sorted(rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:n]


def build(store=None):
    from engine.store import Store
    store = store or Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    saved, saved_n = dict(v15.KEY_STRATA), v15.VARIANTS
    try:
        v15.KEY_STRATA.clear(); v15.KEY_STRATA.update(KEY_STRATA)
        v15.VARIANTS = VARIANTS
        keys, per, rej_k = v15.key_rows(store)
    finally:
        v15.KEY_STRATA.clear(); v15.KEY_STRATA.update(saved)
        v15.VARIANTS = saved_n
    old_written, rej_w = v15.written_rows(store)
    added, rej_n = new_rows(store)
    written = added + by_hash(old_written, KEEP_V15)
    remind = by_hash(v15.remind(), REMIND)
    return keys, written, remind, per, {**rej_k, **rej_w, **rej_n}


allowed_sources = v15.allowed_sources


def generate(store=None, held_doc=None):
    keys, written, old, per, rejected = build(store)
    files = {"regra_lida/train.jsonl": v13.dump(keys + written + old),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    styles = {}
    for r in written:
        styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
    index = {"tool": VERSION, "protocol": v15.PROTOCOL, "product_rule": v15.PRODUCT_RULE, "keys": per, "key_rows": len(keys), "written_rows": len(written),
             "written_by_style": styles, "remind_rows": len(old), "rejected": len(rejected),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D76: rounds 11-14's settled real readings with their numbers moved, the party deadline the vocabulary has no field for, part of data-v15 kept"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"])
    a = ap.parse_args()
    if a.cmd == "check":
        keys, written, old, per, rejected = build()
        print(f"keys {len(per)} -> rows {len(keys)}; written {len(written)}; remind {len(old)}; left out {len(rejected)}")
    else:
        files = generate()
        for rel, b in files.items():
            f = DATA / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b)
        print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k not in ("files", "keys")})
