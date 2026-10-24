"""Canonical JSON and hashing. One definition, used by the store, the governance chain, packages and manifests.

    canonical(value) -> str      JSON with sorted keys, no spaces, UTF-8 characters kept (not escaped)
    sha256_text(text) -> str     hex digest of the UTF-8 bytes
    sha256_bytes(data) -> str
    content_hash(value) -> str   sha256_text(canonical(value))
"""
import hashlib
import json

VERSION = "ccp-canon-0.1"


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def content_hash(value) -> str:
    return sha256_text(canonical(value))
