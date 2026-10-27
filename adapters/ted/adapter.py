"""TED Portuguese notices (the monthly bundles of H.5) -> one raw per notice; for competition notices, a proc unit and its facts.

    used by db/history.py ted (straight into Postgres, D55); no command of its own

Per notice, the exact XML member kept by adapters/ted/modal_ted.py (its sha256 is in the month's index) is the raw
raw:ted:aviso:<publication number>. A competition notice (TED-XML document type 3, «Contract notice»; eForms root
ContractNotice without efac:Changes, which would make it a change to an earlier one) is a procedure: unit proc:ted:<publication number>, with these facts when the notice states them
unambiguously, each with its origin (raw, element):

  publicado_joue          true (the notice is in the OJ S)                  NO_DOC_OJS / NoticePublicationID
  data_publicacao_joue    DATE_PUB / efbc:PublicationDate (the date part)
  data_envio_joue         DATE_DISPATCH_NOTICE / cbc:IssueDate (sent to the Publications Office)
  tipo_procedimento       open, restricted, competitive negotiation (and the utilities' negotiated with a call),
                          competitive dialogue, innovation partnership -> the CCP's five procedures with publication;
                          any other code gives no fact
  tipo_contrato           WORKS / SUPPLIES / SERVICES -> obras / bens / servicos; under Directive 2014/23 (form F24,
                          RegulatoryDomain 32014L0023) works and services are concessao_obras / concessao_servicos
  valor_estimado          VAL_ESTIMATED_TOTAL / EstimatedOverallContractAmount, in EUR only (not the CCP's preço base)
  cpv                     the main CPV code
  data_limite_propostas   DATE_RECEIPT_TENDERS / TenderSubmissionDeadlinePeriod EndDate, when every lot gives the same
  adjudicante             the buyer's national id when it is a nine-digit NIF (a leading PT and spaces dropped)

Award notices, prior information and the rest are raws only for now: linking an award to its procedure (NOTICE_NUMBER_OJ,
ContractFolderID) and a TED procedure to its DR/BASE procedure are joins of their own, not guesses made here.
No model reads anything; nothing is sent anywhere.
"""
import re
import xml.etree.ElementTree as ET

SOURCE = "ted"
ADAPTADOR = "adaptador:ted@1"
PROC_TEDXML = {"PT_OPEN": "concurso_publico", "PT_RESTRICTED": "concurso_limitado_previa_qualificacao",
               "PT_COMPETITIVE_NEGOTIATION": "procedimento_negociacao", "PT_NEGOTIATED_WITH_PRIOR_CALL": "procedimento_negociacao",
               "PT_COMPETITIVE_DIALOGUE": "dialogo_concorrencial", "PT_INNOVATION_PARTNERSHIP": "parceria_inovacao"}
PROC_EFORMS = {"open": "concurso_publico", "restricted": "concurso_limitado_previa_qualificacao", "neg-w-call": "procedimento_negociacao",
               "comp-dial": "dialogo_concorrencial", "innovation": "parceria_inovacao"}
CONTRACT = {"WORKS": "obras", "SUPPLIES": "bens", "SERVICES": "servicos", "works": "obras", "supplies": "bens", "services": "servicos"}
CONCESSION = {"obras": "concessao_obras", "servicos": "concessao_servicos"}   # Directive 2014/23: form F24, RegulatoryDomain 32014L0023
NIF = re.compile(r"(?:PT)?\s*([0-9]{9})")


def local(tag):
    return tag.rsplit("}", 1)[-1]


def find(el, *path):
    """Elements under el along local names (namespaces ignored); '*' matches any child."""
    out = [el]
    for name in path:
        out = [c for e in out for c in e if name == "*" or local(c.tag) == name]
    return out


def first_text(el, *path):
    xs = [x.text.strip() for x in find(el, *path) if x.text and x.text.strip()]
    return xs[0] if xs else None


def ymd(v):
    m = re.fullmatch(r"([0-9]{4})-?([0-9]{2})-?([0-9]{2})(?:Z|[+-][0-9]{2}:[0-9]{2})?", v or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def amount(el):
    if el is None or el.get("CURRENCY", el.get("currencyID")) != "EUR":
        return None
    try:
        v = float(el.text)
    except (TypeError, ValueError):
        return None
    return None if v <= 0 else (int(v) if v.is_integer() else v)


def read_tedxml(root):
    """(publication number, is a competition notice, {field: (value, element)}, {field: reason})."""
    got, why = {}, {}
    pub = (root.get("DOC_ID") or "").strip()
    doc_type = next((e.get("CODE") for e in find(root, "CODED_DATA_SECTION", "CODIF_DATA", "TD_DOCUMENT_TYPE")), None)
    forms = [f for f in find(root, "FORM_SECTION", "*") if f.get("CATEGORY") == "ORIGINAL"] or find(root, "FORM_SECTION", "*")
    form = forms[0] if forms else None
    got["publicado_joue"] = (True, "NO_DOC_OJS")
    d = ymd(first_text(root, "CODED_DATA_SECTION", "REF_OJS", "DATE_PUB"))
    (got.__setitem__("data_publicacao_joue", (d, "DATE_PUB")) if d else why.__setitem__("data_publicacao_joue", "DATE_PUB absent or not a date"))
    if form is None:
        why["form"] = "no form"
        return pub, doc_type == "3", got, why
    d = ymd(first_text(form, "COMPLEMENTARY_INFO", "DATE_DISPATCH_NOTICE"))
    (got.__setitem__("data_envio_joue", (d, "DATE_DISPATCH_NOTICE")) if d else why.__setitem__("data_envio_joue", "DATE_DISPATCH_NOTICE absent"))
    procs = [local(c.tag) for p in find(form, "PROCEDURE") for c in p if local(c.tag).startswith("PT_")]
    if len(procs) == 1 and procs[0] in PROC_TEDXML:
        got["tipo_procedimento"] = (PROC_TEDXML[procs[0]], procs[0])
    else:
        why["tipo_procedimento"] = f"procedure {procs or 'absent'} outside the five with publication"
    ct = [e.get("CTYPE") for e in find(form, "OBJECT_CONTRACT", "TYPE_CONTRACT")]
    tipo = CONTRACT.get(ct[0]) if len(ct) == 1 else None
    if tipo and local(form.tag).startswith("F24"):
        tipo = CONCESSION.get(tipo)
    (got.__setitem__("tipo_contrato", (tipo, "TYPE_CONTRACT")) if tipo else why.__setitem__("tipo_contrato", f"TYPE_CONTRACT {ct} ({local(form.tag)})"))
    v = amount(next(iter(find(form, "OBJECT_CONTRACT", "VAL_ESTIMATED_TOTAL")), None))
    (got.__setitem__("valor_estimado", (v, "VAL_ESTIMATED_TOTAL")) if v is not None else why.__setitem__("valor_estimado", "absent, zero or not EUR"))
    cpv = [e.get("CODE") for e in find(form, "OBJECT_CONTRACT", "CPV_MAIN", "CPV_CODE")]
    (got.__setitem__("cpv", (cpv[0], "CPV_MAIN")) if len(cpv) == 1 and cpv[0] else why.__setitem__("cpv", "CPV_MAIN absent"))
    d = ymd(first_text(form, "PROCEDURE", "DATE_RECEIPT_TENDERS"))
    (got.__setitem__("data_limite_propostas", (d, "DATE_RECEIPT_TENDERS")) if d else why.__setitem__("data_limite_propostas", "DATE_RECEIPT_TENDERS absent"))
    nid = first_text(form, "CONTRACTING_BODY", "ADDRESS_CONTRACTING_BODY", "NATIONALID")
    m = NIF.fullmatch(nid or "")
    (got.__setitem__("adjudicante", (m.group(1), "NATIONALID")) if m else why.__setitem__("adjudicante", "NATIONALID absent" if not nid else "NATIONALID not a NIF"))
    return pub, doc_type == "3", got, why


def read_eforms(root):
    got, why = {}, {}
    pub = first_text(root, "UBLExtensions", "UBLExtension", "ExtensionContent", "EformsExtension", "Publication", "NoticePublicationID") or ""
    got["publicado_joue"] = (True, "NoticePublicationID")
    d = ymd(first_text(root, "UBLExtensions", "UBLExtension", "ExtensionContent", "EformsExtension", "Publication", "PublicationDate"))
    (got.__setitem__("data_publicacao_joue", (d, "PublicationDate")) if d else why.__setitem__("data_publicacao_joue", "PublicationDate absent"))
    d = ymd(first_text(root, "IssueDate"))
    (got.__setitem__("data_envio_joue", (d, "IssueDate")) if d else why.__setitem__("data_envio_joue", "IssueDate absent"))
    pc = [e.text.strip() for e in find(root, "TenderingProcess", "ProcedureCode") if e.text]
    (got.__setitem__("tipo_procedimento", (PROC_EFORMS[pc[0]], "ProcedureCode")) if len(pc) == 1 and pc[0] in PROC_EFORMS
     else why.__setitem__("tipo_procedimento", f"ProcedureCode {pc or 'absent'} outside the five with publication"))
    ct = [e.text.strip() for e in find(root, "ProcurementProject", "ProcurementTypeCode") if e.text]
    tipo = CONTRACT.get(ct[0]) if len(ct) == 1 else None
    if tipo and first_text(root, "RegulatoryDomain") == "32014L0023":
        tipo = CONCESSION.get(tipo)
    (got.__setitem__("tipo_contrato", (tipo, "ProcurementTypeCode")) if tipo else why.__setitem__("tipo_contrato", f"ProcurementTypeCode {ct}"))
    v = amount(next(iter(find(root, "ProcurementProject", "RequestedTenderTotal", "EstimatedOverallContractAmount")), None))
    (got.__setitem__("valor_estimado", (v, "EstimatedOverallContractAmount")) if v is not None else why.__setitem__("valor_estimado", "absent, zero or not EUR"))
    cpv = [e.text.strip() for e in find(root, "ProcurementProject", "MainCommodityClassification", "ItemClassificationCode") if e.text]
    (got.__setitem__("cpv", (cpv[0], "MainCommodityClassification")) if len(cpv) == 1 else why.__setitem__("cpv", "main CPV absent"))
    ends = {ymd(e.text.strip()) for e in find(root, "ProcurementProjectLot", "TenderingProcess", "TenderSubmissionDeadlinePeriod", "EndDate") if e.text}
    (got.__setitem__("data_limite_propostas", (ends.pop(), "TenderSubmissionDeadlinePeriod")) if len(ends) == 1 and None not in ends
     else why.__setitem__("data_limite_propostas", "absent" if not ends else "lots with different deadlines"))
    buyers = [first_text(p, "PartyIdentification", "ID") for p in find(root, "ContractingParty", "Party")]
    ids = []
    for org in find(root, "UBLExtensions", "UBLExtension", "ExtensionContent", "EformsExtension", "Organizations", "Organization", "Company"):
        if first_text(org, "PartyIdentification", "ID") in buyers:
            ids.append(first_text(org, "PartyLegalEntity", "CompanyID"))
    nifs = {NIF.fullmatch(i).group(1) for i in ids if i and NIF.fullmatch(i)}
    (got.__setitem__("adjudicante", (nifs.pop(), "CompanyID")) if len(buyers) == 1 and len(nifs) == 1
     else why.__setitem__("adjudicante", "several buyers" if len(buyers) > 1 else "buyer CompanyID not a NIF"))
    changes = find(root, "UBLExtensions", "UBLExtension", "ExtensionContent", "EformsExtension", "Changes")
    return pub, local(root.tag) == "ContractNotice" and not changes, got, why   # a change notice amends one already read


def notice(xml, member, month, recorded_at):
    """(raw, unit or None, facts, {field: reason}, kind) for one kept member of a month's bundle."""
    root = ET.fromstring(xml)
    pub, competition, got, why = (read_eforms if member["format"] == "eforms" else read_tedxml)(root)
    if not re.fullmatch(r"[0-9]{6,8}-[0-9]{4}", pub):
        raise ValueError(f"{member['member']}: publication number {pub!r}")
    rid = f"raw:{SOURCE}:aviso:{pub}"
    raw = {"id": rid, "revision": 1, "recorded_at": recorded_at, "source": SOURCE, "kind": "aviso", "source_id": pub, "sha256": member["sha256"],
           "bytes": f"raw_bytes/{member['sha256']}", "media_type": "application/xml", "encoding": "utf-8", "url": month["package_url"],
           "captured_at": month["captured_at"], "request": {"method": "GET", "reads_of_page": 1}}
    if not competition:
        return raw, None, [], {}, local(root.tag)
    unit_id = f"proc:{SOURCE}:{pub}"
    unit = {"id": unit_id, "revision": 1, "recorded_at": recorded_at, "kind": "proc", "parent": None, "raw": [rid],
            "consumer_ids": {"ted_publication_number": pub}}
    valid_at = got.get("data_publicacao_joue", (None,))[0]
    if valid_at is None:
        return raw, unit, [], {"*": "no publication date: no valid_at"}, local(root.tag)
    facts = [{"id": f"facto:{unit_id.replace(':', '-')}:{f}:{SOURCE}", "revision": 1, "recorded_at": recorded_at, "unit": unit_id, "field": f,
              "value": v, "origin": {"raw": rid, "field": src}, "adapter": ADAPTADOR, "valid_at": valid_at, "known_at": month["captured_at"]}
             for f, (v, src) in sorted(got.items())]
    return raw, unit, facts, why, local(root.tag)
