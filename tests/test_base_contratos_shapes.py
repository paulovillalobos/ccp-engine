"""BASE dumps changed shape on 2026-11-04: entities went from "NIF - name" strings to objects. The adapter must read both the
same way, so the history (old shape) and the daily dump (new shape) give identical facts."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("base_contratos_adapter", ROOT / "adapters/base-contratos/adapter.py")
ad = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ad)

COMMON = {"tipoprocedimento": "Consulta Prévia", "precoBaseProcedimento": 2984756.26, "tipoContrato": ["Empreitadas de obras públicas"],
          "precoContratual": 2984700.0, "dataCelebracaoContrato": "12/01/2021", "dataPublicacao": "08/03/2021"}
OLD = {**COMMON, "adjudicante": ["500745943 - Município de Oeiras"],
       "adjudicatarios": ["500073945 - Tâmega Engineering, S.A.", "509999999 - Outra, Lda"]}
NEW = {**COMMON, "adjudicante": [{"nifEntContrato": "500745943", "descEntContrato": "Município de Oeiras", "codPaisEntContrato": "PRT"}],
       "adjudicatarios": [{"nifEntContrato": "500073945", "descEntContrato": "Tâmega Engineering, S.A."},
                          {"nifEntContrato": "509999999", "descEntContrato": "Outra, Lda"}]}


class Shapes(unittest.TestCase):
    def test_old_and_new_give_the_same_facts(self):
        self.assertEqual(ad.contract_values(OLD), ad.contract_values(NEW))
        got, _ = ad.contract_values(NEW)
        self.assertEqual(got["adjudicante"], ("500745943", "adjudicante"))
        self.assertEqual(got["adjudicatario"], (["500073945", "509999999"], "adjudicatarios"))

    def test_foreign_or_unknown_nif_is_refused_in_both_shapes(self):
        old = {**OLD, "adjudicatarios": ["500073945 - Tâmega", "- Fremde GmbH"]}
        new = {**NEW, "adjudicatarios": [{"nifEntContrato": "500073945"}, {"nifEntContrato": "-", "codPaisEntContrato": "DEU"}]}
        for rec in (old, new):
            got, why = ad.contract_values(rec)
            self.assertNotIn("adjudicatario", got)
            self.assertEqual(why["adjudicatario"], "an adjudicatário without NIF ('-')")

    def test_two_adjudicantes_or_none_are_refused(self):
        for adj in ([], [{"nifEntContrato": "500745943"}, {"nifEntContrato": "505181266"}], [{"nifEntContrato": None}], [{}]):
            got, why = ad.contract_values({**NEW, "adjudicante": adj})
            self.assertNotIn("adjudicante", got)
            self.assertIn("adjudicante", why)


if __name__ == "__main__":
    unittest.main()
