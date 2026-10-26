"""TED notice parser, TED-XML (R2.0.9, before eForms) and eForms (UBL), by element names. Code only, no model.

    parse(xml_bytes) -> dict of the fields below (None where the notice does not give one)

format, notice_type, notice_id, dispatch_date, publication_date, buyer_name, buyer_nif, buyer_country, buyer_nuts,
procedure_type, contract_type, deadline_date, deadline_time, estimated_value, currency, main_cpv.

TED-XML: the coded data (TD_DOCUMENT_TYPE, NO_DOC_OJS, DATE_PUB, DS_DATE_DISPATCH, ISO_COUNTRY) and the form
(ADDRESS_CONTRACTING_BODY, PR_PROC, TYPE_CONTRACT, DATE_RECEIPT_TENDERS, TIME_RECEIPT_TENDERS, VAL_ESTIMATED_TOTAL,
CPV_MAIN); for the older R2.0.8 forms still found in 2018, CA_CE_CONCESSIONAIRE_PROFILE, the CTYPE attribute and
RECEIPT_LIMIT_DATE (no estimated value is read from them). eForms: the buyer is the organisation the ContractingParty names (cac:Party/cac:PartyIdentification/cbc:ID),
read in efac:Organizations; the deadline is the first lot's TenderSubmissionDeadlinePeriod; dates keep only the date
part (the zone offset is reported in deadline_time when present). Written on the development months 2018-01 and 2026-01
(not in the measured sample) and frozen by its sha256 before the sample is drawn (CRITERIA-ted-contratos-v1.md).
"""
import xml.etree.ElementTree as ET


def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def first(node, *path):
    """The first descendant following local names in order (each step: any depth below the previous)."""
    cur = [node]
    for name in path:
        nxt = None
        for c in cur:
            for d in c.iter():
                if d is not c and local(d.tag) == name:
                    nxt = d
                    break
            if nxt is not None:
                break
        if nxt is None:
            return None
        cur = [nxt]
    return cur[0]


def text(node, *path):
    n = first(node, *path) if path else node
    if n is None or n.text is None:
        return None
    t = n.text.strip()
    return t or None


def date_only(v):
    if not v:
        return None
    v = v.strip()
    if len(v) == 8 and v.isdigit():
        return f"{v[:4]}-{v[4:6]}-{v[6:]}"
    return v[:10] if len(v) >= 10 and v[4] == "-" else None


def parse_tedxml(root):
    out = {"format": "ted-xml"}
    td = first(root, "TD_DOCUMENT_TYPE")
    out["notice_type"] = f"{td.get('CODE')} {(td.text or '').strip()}".strip() if td is not None else None
    out["notice_id"] = text(root, "NO_DOC_OJS")
    out["dispatch_date"] = date_only(text(root, "DATE_DISPATCH_NOTICE") or text(root, "DS_DATE_DISPATCH"))
    out["publication_date"] = date_only(text(root, "DATE_PUB"))
    body = first(root, "ADDRESS_CONTRACTING_BODY") or first(root, "CA_CE_CONCESSIONAIRE_PROFILE")  # R2.0.9, else R2.0.8
    out["buyer_name"] = text(body, "OFFICIALNAME") if body is not None else None
    out["buyer_nif"] = text(body, "NATIONALID") if body is not None else None
    iso = first(root, "ISO_COUNTRY")
    out["buyer_country"] = iso.get("VALUE") if iso is not None else None
    nuts = first(body, "NUTS") if body is not None else None
    out["buyer_nuts"] = nuts.get("CODE") if nuts is not None else None
    pr = first(root, "PR_PROC")
    out["procedure_type"] = f"{pr.get('CODE')} {(pr.text or '').strip()}".strip() if pr is not None else None
    tc = first(root, "TYPE_CONTRACT")
    if tc is None:  # R2.0.8: the CTYPE attribute of FD_CONTRACT and its kin
        tc = next((e for e in root.iter() if e.get("CTYPE")), None)
    out["contract_type"] = tc.get("CTYPE") if tc is not None else None
    out["deadline_date"] = date_only(text(root, "DATE_RECEIPT_TENDERS"))
    out["deadline_time"] = text(root, "TIME_RECEIPT_TENDERS")
    rld = first(root, "RECEIPT_LIMIT_DATE")  # R2.0.8: DAY, MONTH, YEAR, TIME
    if out["deadline_date"] is None and rld is not None and text(rld, "YEAR") and text(rld, "MONTH") and text(rld, "DAY"):
        out["deadline_date"] = f"{text(rld, 'YEAR')}-{int(text(rld, 'MONTH')):02d}-{int(text(rld, 'DAY')):02d}"
        out["deadline_time"] = text(rld, "TIME")
    val = first(root, "VAL_ESTIMATED_TOTAL")
    out["estimated_value"] = val.text.strip() if val is not None and val.text and val.text.strip() else None
    out["currency"] = val.get("CURRENCY") if val is not None else None
    cpv = first(root, "CPV_MAIN", "CPV_CODE")
    out["main_cpv"] = cpv.get("CODE") if cpv is not None else None
    return out


def parse_eforms(root):
    out = {"format": "eforms", "notice_type": text(root, "NoticeSubType", "SubTypeCode")}
    out["notice_id"] = text(root, "Publication", "NoticePublicationID")
    out["dispatch_date"] = date_only(text(root, "IssueDate"))
    out["publication_date"] = date_only(text(root, "Publication", "PublicationDate"))
    buyer_ref = text(root, "ContractingParty", "Party", "PartyIdentification", "ID")
    org = None
    for o in root.iter():
        if local(o.tag) == "Organization":
            company = first(o, "Company")
            if company is not None and text(company, "PartyIdentification", "ID") == buyer_ref:
                org = company
                break
    out["buyer_name"] = text(org, "PartyName", "Name") if org is not None else None
    out["buyer_nif"] = text(org, "PartyLegalEntity", "CompanyID") if org is not None else None
    out["buyer_country"] = text(org, "PostalAddress", "Country", "IdentificationCode") if org is not None else None
    out["buyer_nuts"] = text(org, "PostalAddress", "CountrySubentityCode") if org is not None else None
    out["procedure_type"] = next((text(t, "ProcedureCode") for t in root if local(t.tag) == "TenderingProcess"), None)
    project = None
    for p in root:
        if local(p.tag) == "ProcurementProject":
            project = p
            break
    out["contract_type"] = text(project, "ProcurementTypeCode") if project is not None else None
    amount = first(project, "RequestedTenderTotal", "EstimatedOverallContractAmount") if project is not None else None
    out["estimated_value"] = amount.text.strip() if amount is not None and amount.text else None
    out["currency"] = amount.get("currencyID") if amount is not None else None
    out["main_cpv"] = text(project, "MainCommodityClassification", "ItemClassificationCode") if project is not None else None
    period = first(root, "ProcurementProjectLot", "TenderSubmissionDeadlinePeriod")
    out["deadline_date"] = date_only(text(period, "EndDate")) if period is not None else None
    out["deadline_time"] = text(period, "EndTime") if period is not None else None
    return out


FIELDS = ["format", "notice_type", "notice_id", "dispatch_date", "publication_date", "buyer_name", "buyer_nif", "buyer_country",
          "buyer_nuts", "procedure_type", "contract_type", "deadline_date", "deadline_time", "estimated_value", "currency", "main_cpv"]


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = parse_tedxml(root) if local(root.tag) == "TED_EXPORT" else parse_eforms(root)
    return {k: out.get(k) for k in FIELDS}
