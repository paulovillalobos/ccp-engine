import { useEffect, useState } from "react";
import { Alignment, Breadcrumbs, Icon, Navbar, Tag } from "@blueprintjs/core";
import { api, num, shortId } from "./api.js";
import Home from "./Home.jsx";
import Procedure from "./Procedure.jsx";
import Buyer from "./Buyer.jsx";
import Report from "./Report.jsx";

// Hash routes: #/ home, #/p/<unit> procedure, #/r/<unit> its report, #/e/<nif> buyer.
function useRoute() {
  const [hash, setHash] = useState(window.location.hash);
  useEffect(() => {
    const on = () => { setHash(window.location.hash); window.scrollTo(0, 0); };
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  const [, kind, id] = hash.match(/^#\/(p|r|e)\/(.+)$/) || [];
  return { kind, id: id && decodeURIComponent(id) };
}

export const go = (kind, id) => (window.location.hash = kind ? `#/${kind}/${encodeURIComponent(id)}` : "#/");

export default function App() {
  const route = useRoute();
  const [run, setRun] = useState(null);
  useEffect(() => {
    api.stats().then((s) => setRun(s.corrida)).catch(() => setRun(false));
  }, []);

  const crumbs = [{ text: "Contratos públicos", icon: "home", href: "#/" }];
  if (route.kind === "p") crumbs.push({ text: `Procedimento ${shortId(route.id)}`, icon: "document" });
  if (route.kind === "r") crumbs.push({ text: `Procedimento ${shortId(route.id)}`, icon: "document", href: `#/p/${encodeURIComponent(route.id)}` }, { text: "Relatório", icon: "export" });
  if (route.kind === "e") crumbs.push({ text: `Entidade ${route.id}`, icon: "office" });

  return (
    <>
      <Navbar className="top">
        <Navbar.Group align={Alignment.LEFT}>
          <a className="brand" href="#/"><span className="logo"><Icon icon="cube" size={14} /></span>CCP Engine</a>
          <Navbar.Divider />
          <Breadcrumbs items={crumbs} />
        </Navbar.Group>
        <Navbar.Group align={Alignment.RIGHT}>
          {run && <Tag minimal icon="time" className="mono">Verificação {run.id.slice(8, 12)}-{run.id.slice(12, 14)}-{run.id.slice(14, 16)} · {num(run.procedures)} procedimentos</Tag>}
          {run === false && <Tag intent="danger" icon="error">API indisponível</Tag>}
        </Navbar.Group>
      </Navbar>
      <main className="col">
        {route.kind === "p" ? <Procedure unit={route.id} /> : route.kind === "r" ? <Report unit={route.id} /> : route.kind === "e" ? <Buyer nif={route.id} /> : <Home run={run} />}
      </main>
    </>
  );
}
