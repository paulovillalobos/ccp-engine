import { useEffect, useState } from "react";
import { Icon, NonIdealState, Spinner, Tag } from "@blueprintjs/core";
import { api, num } from "./api.js";
import Problems from "./Problems.jsx";
import Kpis from "./Kpis.jsx";
import Panel from "./Panel.jsx";

// One adjudicante as an object view: how many of its contracts were checked, how many break the law, and which.
export default function Buyer({ nif }) {
  const [s, setS] = useState({ loading: true });
  const [filter, setFilter] = useState(null);
  useEffect(() => {
    setS({ loading: true }); setFilter(null);
    api.buyerAll(nif).then((d) => setS({ d })).catch((e) => setS({ error: e.message }));
  }, [nif]);

  if (s.loading) return <div className="center"><Spinner size={32} /></div>;
  if (s.error) return <NonIdealState icon="error" title={s.error} />;
  const items = s.d.veredictos;
  const bad = items.filter((v) => v.resultado === "nao_cumpre");
  const good = items.filter((v) => v.resultado === "cumpre");
  const shown = filter || (bad.length ? "nao_cumpre" : "todos");
  const list = shown === "cumpre" ? good : shown === "nao_cumpre" ? bad : [...bad, ...good];

  return (
    <>
      <div className="object-head">
        <div className="object-icon"><Icon icon="office" size={22} /></div>
        <div className="object-title">
          <div className="eyebrow">Entidade adjudicante</div>
          <h1 className="mono">NIF {nif}</h1>
        </div>
        {items.length > 0 && <Tag large intent={bad.length ? "danger" : "success"} icon={bad.length ? "error" : "tick-circle"}>{bad.length ? `${bad.length} não cumpre` : "Tudo cumpre"}</Tag>}
      </div>

      {items.length === 0 ? <NonIdealState icon="search" title="Nenhum contrato desta entidade tem veredicto na última verificação" /> : (
        <>
          <Kpis active={shown} items={[
            { key: "todos", icon: "database", label: "Contratos verificados", value: num(items.length) + (s.d.completo ? "" : "+"), onClick: () => setFilter("todos") },
            { key: "cumpre", icon: "tick-circle", label: "Cumprem", value: num(good.length), tone: "ok", onClick: () => setFilter("cumpre") },
            { key: "nao_cumpre", icon: "error", label: "Não cumprem", value: num(bad.length), tone: "bad", onClick: () => setFilter("nao_cumpre") },
          ]} />
          <Panel icon={shown === "cumpre" ? "tick-circle" : shown === "nao_cumpre" ? "warning-sign" : "database"} flush
            title={shown === "cumpre" ? "Cumprem" : shown === "nao_cumpre" ? "Não cumprem" : "Todos os contratos verificados"}
            right={<Tag minimal intent={shown === "cumpre" ? "success" : shown === "nao_cumpre" ? "danger" : "none"}>{num(list.length)}</Tag>}>
            {list.length ? <Problems items={list} /> : <div className="panel-note">Nenhum.</div>}
          </Panel>
        </>
      )}
    </>
  );
}
