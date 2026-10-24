"""Append-only, bitemporal object store over plain JSON files (read side; the write side is added in A4).

Layout (DECISIONS D3): under any root, a directory named after a schema type holds its objects, one per `.json` file or
one per line in a `.jsonl` file; `governance/` holds `principals.json` and `events.jsonl`; `raw_bytes/<sha256>` holds
captured bytes. Several roots form one store (fixtures/valid; law/ + rules/ + governance/; data/).

    Store(roots).load()              reads everything; never raises on bad data, records (code, message) in .errors
    store.objects[type] -> list      every revision of every object of that type, in file order
    store.revisions(id) -> list      all revisions of one id, sorted by revision
    store.current(id) -> dict|None   the highest revision (stale or not); None when unknown
    store.exists(id) -> bool
    store.raw_text(raw_obj) -> str   decoded bytes of a raw record (utf-8 / latin-1), from raw_bytes/
    store.raw_path(raw_obj) -> Path|None

Invariant 9 at load time (code I09): the same (id, revision) may not appear twice; revisions of one id are 1..n without
gaps; a revision above 1 names the one it supersedes. Nothing here deletes or rewrites a file.
"""
import json
from pathlib import Path

from engine import schema

VERSION = "ccp-store-0.1"
SKIP_DIRS = {".venv", ".git", "__pycache__", "broken", "node_modules"}


class Store:
    def __init__(self, roots):
        self.roots = [Path(r) for r in roots]
        self.objects = {t: [] for t in schema.TYPES}
        self.by_id = {}
        self.files = {}
        self.raw_bytes = {}
        self.principals = None
        self.events = []
        self.governance_dir = None
        self.errors = []
        self.unknown_files = []

    # ---- loading ------------------------------------------------------------------------------------------------
    def load(self):
        for root in self.roots:
            if not root.exists():
                continue
            if root.name == "governance":
                self._load_governance(root)
                continue
            for path in sorted(root.rglob("*")):
                if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                    continue
                if path.is_dir():
                    continue
                parent = path.parent.name
                if parent == "raw_bytes":
                    self.raw_bytes[path.name] = path
                elif parent == "governance":
                    pass
                elif parent in schema.TYPES and path.suffix in (".json", ".jsonl"):
                    self._load_file(parent, path)
                elif path.suffix in (".json", ".jsonl") and "facts" in path.relative_to(root).parts:
                    self.unknown_files.append(path)
            for gov in sorted(p for p in root.rglob("governance") if p.is_dir() and not any(s in p.parts for s in SKIP_DIRS)):
                self._load_governance(gov)
        self._check_revisions()
        return self

    def _load_file(self, type_, path):
        try:
            text = path.read_text(encoding="utf-8")
            items = [json.loads(line) for line in text.splitlines() if line.strip()] if path.suffix == ".jsonl" else [json.loads(text)]
        except (OSError, json.JSONDecodeError) as exc:
            self.errors.append(("SCHEMA", f"{path}: unreadable JSON: {exc}"))
            return
        for i, obj in enumerate(items):
            for msg in schema.validate(type_, obj):
                self.errors.append(("SCHEMA", f"{path}#{i} ({type_}): {msg}"))
            if not isinstance(obj, dict):
                continue
            self.objects[type_].append(obj)
            if type_ == "manifesto":
                continue
            ident, rev = obj.get("id"), obj.get("revision")
            if not isinstance(ident, str) or not isinstance(rev, int):
                continue
            if schema.type_of(obj) not in (type_, None) and type_ != "manifesto":
                self.errors.append(("SCHEMA", f"{path}#{i}: id {ident} is a {schema.type_of(obj)}, stored under {type_}/"))
            key = (ident, rev)
            if key in self.files:
                self.errors.append(("I09", f"{ident} revision {rev} appears twice: {self.files[key]} and {path}; a change is a new revision, never a rewrite"))
            self.files[key] = path
            self.by_id.setdefault(ident, []).append(obj)

    def _load_governance(self, gov):
        if self.governance_dir is not None and self.governance_dir != gov:
            self.errors.append(("I09", f"two governance logs in one store: {self.governance_dir} and {gov}"))
        self.governance_dir = gov
        pfile, efile = gov / "principals.json", gov / "events.jsonl"
        if pfile.exists():
            try:
                self.principals = json.loads(pfile.read_text(encoding="utf-8"))
                for msg in schema.validate("principals", self.principals):
                    self.errors.append(("SCHEMA", f"{pfile}: {msg}"))
            except (OSError, json.JSONDecodeError) as exc:
                self.errors.append(("SCHEMA", f"{pfile}: {exc}"))
        if efile.exists():
            for n, line in enumerate(efile.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError as exc:
                    self.errors.append(("SCHEMA", f"{efile}:{n}: {exc}"))
                    continue
                for msg in schema.validate("evento", ev):
                    self.errors.append(("SCHEMA", f"{efile}:{n}: {msg}"))
                self.events.append((line, ev))

    def _check_revisions(self):
        for ident, revs in self.by_id.items():
            nums = sorted(r["revision"] for r in revs)
            if nums != list(range(1, len(nums) + 1)):
                self.errors.append(("I09", f"{ident}: revisions {nums} are not 1..n without gaps"))
            for r in revs:
                if r["revision"] > 1 and r.get("supersedes") != r["revision"] - 1:
                    self.errors.append(("I09", f"{ident} revision {r['revision']}: must name supersedes = {r['revision'] - 1}"))

    # ---- reading ------------------------------------------------------------------------------------------------
    def revisions(self, ident):
        return sorted(self.by_id.get(ident, []), key=lambda r: r["revision"])

    def current(self, ident):
        revs = self.revisions(ident)
        return revs[-1] if revs else None

    def exists(self, ident):
        return ident in self.by_id

    def raw_path(self, raw_obj):
        return self.raw_bytes.get(raw_obj.get("sha256"))

    def raw_text(self, raw_obj):
        path = self.raw_path(raw_obj)
        if path is None:
            return None
        enc = raw_obj.get("encoding", "utf-8")
        if enc == "binary":
            return None
        return path.read_text(encoding=enc)
