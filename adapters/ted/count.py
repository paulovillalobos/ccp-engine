import tarfile, sys, re, collections
p = sys.argv[1]
tot, pt, kinds, nifs = 0, 0, collections.Counter(), 0
ex = []
with tarfile.open(p, "r:gz") as t:
    for m in t:
        if not m.isfile() or not m.name.endswith(".xml"):
            continue
        tot += 1
        x = t.extractfile(m).read().decode("utf-8", "replace")
        buyer_pt = re.search(r'<cac:Country>\s*<cbc:IdentificationCode listName="country">PRT</cbc:IdentificationCode>', x) is not None
        if not buyer_pt:
            continue
        pt += 1
        sub = re.search(r'listName="notice-subtype">([^<]+)<', x)
        kinds[sub.group(1) if sub else "?"] += 1
        nif = re.search(r'<cbc:CompanyID[^>]*>\s*(?:PT)?\s*([0-9]{9})\s*<', x)
        if nif:
            nifs += 1
        if len(ex) < 3:
            ex.append(m.name)
print("avisos en el paquete", tot, "| con un país PRT en alguna organización", pt, "| con un NIF de 9 dígitos", nifs)
print("subtipos eForms (PT)", kinds.most_common(10))
print("ejemplos", ex)
