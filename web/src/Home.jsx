import { useEffect, useState } from "react";
import { Button, Spinner, Tag } from "@blueprintjs/core";
import { api, num } from "./api.js";
import Search from "./Search.jsx";
import Problems from "./Problems.jsx";
import Kpis from "./Kpis.jsx";
import Panel from "./Panel.jsx";

const VIEW = {
  nao_cumpre: { title: "Contratos que não cumprem", icon: "warning-sign", intent: "danger" },
  cumpre: { title: "Contratos que cumprem", icon: "tick-circle", intent: "success" },
  nao_avaliado: { title: "Contratos não decidíveis (com o motivo)", icon: "disable", intent: "none" },
  "": { title: "Todos os contratos com veredicto", icon: "database", intent: "none" },
};

// The question, a search box, the totals (each one a filter), and the contracts of the chosen total.
export default function Home({ run }) {
  const [filter, setFilter] = useState("nao_cumpre");
  const [items, setItems] = useState([]);
  const [next, setNext] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = (apos) => {
    setLoading(true);
    api.verdicts({ resultado: filter, apos })
      .then((d) => { setItems((old) => (apos ? [...old, ...d.veredictos] : d.veredictos)); setNext(d.seguinte); })
      .finally(() => setLoading(false));
  };
  useEffect(() => { setItems([]); load(null); }, [filter]);

  const decided = run ? run.by_result.cumpre + run.by_result.nao_cumpre : 0;
  const count = run ? { nao_cumpre: run.by_result.nao_cumpre, cumpre: run.by_result.cumpre, nao_avaliado: run.by_result.nao_decidivel, "": decided }[filter] : null;
  const view = VIEW[filter];

  return (
    <>
      <section className="hero">
        <div className="eyebrow">Código dos Contratos Públicos · portal BASE</div>
        <h1>Os contratos públicos cumprem a lei?</h1>
        <p>Cada procedimento verificado contra a lei, com o artigo citado e a prova.</p>
        <Search />
      </section>

      {run && (
        <Kpis active={filter} items={[
          { key: "", icon: "database", label: "Procedimentos lidos", value: num(run.procedures), onClick: () => setFilter("") },
          { key: "cumpre", icon: "tick-circle", label: "Cumprem", value: num(run.by_result.cumpre), tone: "ok", onClick: () => setFilter("cumpre") },
          { key: "nao_cumpre", icon: "error", label: "Não cumprem", value: num(run.by_result.nao_cumpre), tone: "bad", onClick: () => setFilter("nao_cumpre") },
          ...(run.by_result.nao_decidivel != null ? [{ key: "nao_avaliado", icon: "disable", label: "Não decidíveis", value: num(run.by_result.nao_decidivel), onClick: () => setFilter("nao_avaliado") }] : []),
        ]} />
      )}

      <Panel icon={view.icon} title={view.title} flush right={count != null && <Tag minimal intent={view.intent}>{num(count)}</Tag>}>
        {filter === "" && run && (
          <div className="panel-note">{num(run.procedures)} procedimentos lidos; {num(decided)} têm uma regra que se aplica. Os outros ainda não têm veredicto.</div>
        )}
        {items.length ? <Problems items={items} /> : loading && <div className="center"><Spinner size={24} /></div>}
        {next && <div className="panel-foot"><Button minimal icon="more" loading={loading} text="Ver mais" onClick={() => load(next)} /></div>}
      </Panel>
    </>
  );
}
