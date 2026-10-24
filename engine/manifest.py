"""Manifest: what makes a verdict reproducible (ARQUITECTURA.md §3, §7).

    FIELDS                         the seven required keys
    is_complete(manifest) -> list  empty when complete; else the names of missing or empty parts
    build(law_version, package, adapters, source_snapshots, code, log_head, produced_at) -> dict
    manifest_hash(manifest) -> str sha256 of the canonical manifest; two verdicts with equal manifests replay alike

Complete means: every key present, every list non-empty, code names repository, commit and engine version. The schema
(schemas/manifesto.schema.json) says the same; this module is what the engine and verify call.
"""
from engine.canon import content_hash

VERSION = "ccp-manifest-0.1"
FIELDS = ("law_version", "package", "adapters", "source_snapshots", "code", "log_head", "produced_at")
LISTS = ("adapters", "source_snapshots")
CODE_KEYS = ("repository", "commit", "engine_version")


def is_complete(manifest) -> list:
    if not isinstance(manifest, dict):
        return ["manifest"]
    missing = [k for k in FIELDS if not manifest.get(k)]
    missing += [k for k in LISTS if isinstance(manifest.get(k), list) and len(manifest[k]) == 0 and k not in missing]
    code = manifest.get("code")
    if isinstance(code, dict):
        missing += [f"code.{k}" for k in CODE_KEYS if not code.get(k)]
    return missing


def build(law_version, package, adapters, source_snapshots, code, log_head, produced_at) -> dict:
    manifest = {"law_version": law_version, "package": package, "adapters": sorted(adapters), "source_snapshots": sorted(source_snapshots, key=lambda s: s["source"]),
                "code": dict(code), "log_head": log_head, "produced_at": produced_at}
    missing = is_complete(manifest)
    if missing:
        raise ValueError(f"incomplete manifest: {', '.join(missing)}")
    return manifest


def manifest_hash(manifest) -> str:
    return content_hash(manifest)
