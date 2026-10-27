# Proposals from the platform fetchers (Vortal, acinGov), 2026-10-26

## 1. Raw bytes offloaded to the person's Modal volume: verify cannot re-hash them locally
- Decided by the person (2026-10-26, «Si hazlo»): acinGov's pieces ZIPs (452 files, 14.9 GB, 33 MB on average, one of
  1.9 GB) were uploaded to the Modal volume `ccp-raw-bytes` (/pecas/raw_bytes/<sha256>), checked there by
  adapters/plataformas/offload_check.py (452/452 hash to their name; result in offload-check-pecas.json), and only
  then removed from the Mac. Their raw objects stay in data/raw/pecas/raw/.
- Consequence: `verify.py` on the Mac reports I01 «bytes not in the store» for those raws (as CI does for every
  gitignored byte). One file (the Vortal copy of the DR notice 419974431) still verifies, because the same bytes are
  stored under data/raw/dr-anuncios/raw_bytes/.
- Proposed (the builder's choice): an offload manifest verify trusts only with its check, e.g. a file listing
  (sha256, location) plus the check's own record, and an I01 variant that re-hashes those bytes where they live
  (a Modal function, as offload_check.py does) instead of skipping them.
