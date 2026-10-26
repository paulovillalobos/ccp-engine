"""TED monthly packages 2018–2026 read on the person's Modal account, filtered to Portugal there (BUILD-LOG H.3).

    <modal venv>/bin/modal run --detach adapters/ted/modal_ted.py [--first 2018-1] [--last 2026-9] [--limit N]

Per month, on a small CPU container with the volume ccp-raw-bytes mounted: one GET of
https://ted.europa.eu/packages/monthly/<yyyy>-<m> (all EU notices of that month, tar.gz), kept under
/vol/ted/packages/<sha256> as the raw bytes of that capture; then every XML member is read in the container (the daily packages inside a monthly one are opened in turn) and the
Portuguese notices are written, unchanged, into /vol/ted/pt/<yyyy>-<mm>.tar.gz, with /vol/ted/index/<yyyy>-<mm>.json
listing the package (URL, sha256, size, captured_at) and each kept member (name, sha256, size, format, why kept).
Portuguese: TED-XML (before eForms) with <ISO_COUNTRY VALUE="PT"/> in its coded data (the buyer's country); eForms
with a country code PRT in one of its organisations (the probe of M.2: 77 of 3 631 notices on 01/10/2026). A month
whose index exists is not read again. At most two packages at a time (TED allows three concurrent downloads).
User-Agent «ccp-engine research (passive read)». Nothing is sent but the GETs; no model reads anything.
"""
import json

import modal

app = modal.App("ccp-ted-pt")
volume = modal.Volume.from_name("ccp-raw-bytes")
image = modal.Image.debian_slim(python_version="3.12")


@app.function(image=image, volumes={"/vol": volume}, timeout=6 * 3600, cpu=1, memory=2048, max_containers=2)
def month(ym: str) -> dict:
    import datetime
    import hashlib
    import io
    import os
    import re
    import tarfile
    import urllib.error
    import urllib.request

    y, m = ym.split("-")
    tag = f"{y}-{int(m):02d}"
    for d in ("/vol/ted/packages", "/vol/ted/pt", "/vol/ted/index"):
        os.makedirs(d, exist_ok=True)
    idx_path = f"/vol/ted/index/{tag}.json"
    if os.path.exists(idx_path):
        return json.load(open(idx_path))["summary"]
    url = f"https://ted.europa.eu/packages/monthly/{y}-{int(m)}"
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    part = f"/vol/ted/packages/.{tag}.part"
    h = hashlib.sha256()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ccp-engine research (passive read)"}, method="GET")
        with urllib.request.urlopen(req, timeout=3600) as r, open(part, "wb") as f:
            status = r.status
            for chunk in iter(lambda: r.read(1 << 20), b""):
                h.update(chunk)
                f.write(chunk)
    except urllib.error.HTTPError as exc:
        return {"month": tag, "url": url, "at": at, "status": exc.code, "error": str(exc.reason)}
    sha = h.hexdigest()
    pkg = f"/vol/ted/packages/{sha}"
    os.replace(part, pkg)
    size = os.path.getsize(pkg)
    eforms_pt = re.compile(rb'listName="country">\s*PRT\s*<')
    tedxml_pt = re.compile(rb'<ISO_COUNTRY\s+VALUE="PT"')
    kept, total, formats = [], 0, {"eforms": 0, "ted-xml": 0}
    out_buf = io.BytesIO()
    def xml_members(tar, prefix=""):
        """XML notices of a package; a member that is itself a tar.gz (the daily packages inside a monthly one) is opened in turn."""
        for mem in tar:
            if not mem.isfile():
                continue
            name = prefix + mem.name
            if name.lower().endswith((".tar.gz", ".tgz")):
                with tarfile.open(fileobj=io.BytesIO(tar.extractfile(mem).read()), mode="r:gz") as inner:
                    yield from xml_members(inner, name + "!")
            elif name.lower().endswith(".xml"):
                yield name, mem.mtime, tar.extractfile(mem).read()

    with tarfile.open(pkg, "r:gz") as src, tarfile.open(fileobj=out_buf, mode="w:gz") as dst:
        for name, mtime, data in xml_members(src):
            total += 1
            fmt = "eforms" if b"urn:oasis:names:specification:ubl" in data[:4000] or b"efac:" in data else "ted-xml"
            why = None
            if fmt == "eforms" and eforms_pt.search(data):
                why = "an organisation with country PRT"
            elif fmt == "ted-xml" and tedxml_pt.search(data):
                why = "ISO_COUNTRY PT in the coded data"
            if why:
                formats[fmt] += 1
                info = tarfile.TarInfo(name.replace("!", "/"))
                info.size = len(data)
                info.mtime = mtime
                dst.addfile(info, io.BytesIO(data))
                kept.append({"member": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "format": fmt, "why": why})
    pt_bytes = out_buf.getvalue()
    pt_sha = hashlib.sha256(pt_bytes).hexdigest()
    with open(f"/vol/ted/pt/{tag}.tar.gz", "wb") as f:
        f.write(pt_bytes)
    summary = {"month": tag, "url": url, "at": at, "status": status, "package_sha256": sha, "package_bytes": size,
               "notices": total, "portuguese": len(kept), "by_format": formats, "pt_bundle_sha256": pt_sha, "pt_bundle_bytes": len(pt_bytes)}
    json.dump({"summary": summary, "kept": kept}, open(idx_path, "w"), ensure_ascii=False, indent=1)
    volume.commit()
    return summary


@app.local_entrypoint()
def main(first: str = "2018-1", last: str = "2026-9", limit: int = 0):
    fy, fm = map(int, first.split("-"))
    ly, lm = map(int, last.split("-"))
    months, y, m = [], fy, fm
    while (y, m) <= (ly, lm):
        months.append(f"{y}-{m}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    if limit:
        months = months[:limit]
    print(f"{len(months)} months: {months[0]} .. {months[-1]}")
    for s in month.map(months, return_exceptions=True):
        print(json.dumps(s if isinstance(s, dict) else {"error": repr(s)[:300]}, ensure_ascii=False))
