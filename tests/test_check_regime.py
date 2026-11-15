"""D96: the document check finds the basis a procedure's own documents state, in the wording (and OCR noise) of real
invitations and contracts, and never reads a mention or a page number as a basis. No network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "adapters/plataformas"), str(ROOT)]
import check_regime as c  # noqa: E402


def test_the_general_basis_in_its_printed_and_ocr_forms():
    for t in ("nos termos do disposto na alínea c) do artigo 19.º do Código dos Contratos Públicos",
              "nos termos da alínea c), do artigo 19,º do Código", "em conformidade com o art.º 19.º, al. c) e conduzido",
              "ao abrigo dos artigos 18.º e 19.0, alínea c), do Código", "da alínea c) do artigo 19º do CCP"):
        assert c.GERAL.search(t), t
    assert not c.GERAL.search("por concurso público realizado nos termos da alínea b) do artigo 19.º")


def test_another_basis_and_not_its_lookalikes():
    for t in ("nos termos da alínea b) do artigo 24º, conjugado com ao artigo 27. A", "Consulta Prévia em função de critérios materiais",
              "o ajuste direto critério material", "ao abrigo do n.º 1 do artigo 2.º do Decreto-Lei n,º 135 — A/2017",
              "por concurso público realizado nos termos da alínea b) do artigo 19.º"):
        assert c.OUTRA.search(t), t
    for t in ("e 27-A/2020, de 24 de julho", "Página 15 de 27 A B", "G4_127 A p1", "(pg. 27 a 30)"):
        assert not c.OUTRA.search(t), t


def test_special_measures_and_the_form_answer():
    assert c.ESPECIAL.search("consulta prévia simplificada, com convite a pelo menos cinco entidades, nos termos da alínea b), do artigo 2.º da lei 30/2021")
    assert not c.ESPECIAL.search("CCP, na redação dada pela Lei n.º 30/2021, de 21 de maio")
    m = c.RESPOSTA.search("O procedimento é realizado para as medidas especiais de contratação pública? Não 6 - Preço Base")
    assert m and m.group(1) == "Não"
