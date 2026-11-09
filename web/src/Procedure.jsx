import { useEffect, useState } from "react";
import { AnchorButton, Button, Collapse, Icon, NonIdealState, Spinner, Tag } from "@blueprintjs/core";
import { api, euro, plain, shortId } from "./api.js";
import { go } from "./App.jsx";
import Panel from "./Panel.jsx";

const LABEL = {
  adjudicante: "Entidade (NIF)",
  preco_base: "Preço base",
  tipo_contrato: "Tipo de contrato",
  tipo_procedimento: "Procedimento",
  fundamento_passagens: "Fundamento declarado",
};
const WORDS = { consulta_previa: "consulta prévia", ajuste_direto: "ajuste direto", concurso_publico: "concurso público", obras: "obras públicas", aquisicao_servicos: "aquisição de serviços", aquisicao_bens: "aquisição de bens" };
const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
const article = (p) => p.replace(/^ccp:art(\d+)\.([a-z])$/, "CCP, art. $1.º, alínea $2)").replace(/^ccp:art(\d+)\.(\d+)$/, "CCP, art. $1.º, n.º $2");
const show = (f) => (f.campo === "preco_base" ? euro(f.valor) : Array.isArray(f.valor) ? f.valor.map(article).join("; ") : cap(WORDS[f.valor] || String(f.valor).replace(/_/g, " ")));

function Verdict({ v }) {
  const [open, setOpen] = useState(false);
  const bad = v.resultado === "nao_cumpre";
  return (
    <Panel icon="take-action" title="Veredicto" className={bad ? "edge-bad" : "edge-ok"}>
      <div className="verdict-top">
        <Icon icon={bad ? "error" : "tick-circle"} size={28} className={bad ? "c-bad" : "c-ok"} />
        <div>
          <h2 className={bad ? "c-bad" : "c-ok"}>{bad ? "Não cumpre a lei" : "Cumpre a lei"}</h2>
          <p className="answer-text">{plain(v).text}</p>
        </div>
      </div>
      <blockquote className="law">
        «{v.citacao}»
        <cite><Icon icon="book" size={12} /> {article(v.passagem).replace(/^CCP/, "Código dos Contratos Públicos")}</cite>
      </blockquote>
      <Button minimal small icon={open ? "chevron-down" : "chevron-right"} text="Ver a prova" onClick={() => setOpen(!open)} className="proof-toggle" />
      <Collapse isOpen={open}>
        <dl className="proof">
          <dt>Regra</dt><dd className="mono">{v.regra.id}</dd>
          <dt>Lei em vigor</dt><dd className="mono">{v.manifesto.lei}</dd>
          <dt>Data do facto</dt><dd className="mono">{v.valido_em}</dd>
          <dt>Motor</dt><dd className="mono">{v.manifesto.motor} @ {v.manifesto.commit}</dd>
          <dt>Registo</dt><dd className="mono hash">{v.manifesto.registo}</dd>
          <dt>Cálculo</dt><dd className="mono">{v.detalhe}</dd>
        </dl>
      </Collapse>
    </Panel>
  );
}

// One procedure as an object view: header with its key properties, the verdict, then the data and links.
export default function Procedure({ unit }) {
  const [s, setS] = useState({ loading: true });
  useEffect(() => {
    setS({ loading: true });
    api.procedure(unit).then((d) => setS({ d })).catch((e) => setS({ error: e.message }));
  }, [unit]);

  if (s.loading) return <div className="center"><Spinner size={32} /></div>;
  if (s.error) return <NonIdealState icon="search" title={s.error === "procedimento desconhecido" ? "Este procedimento não existe na BASE" : s.error} />;
  const d = s.d;
  const fact = (k) => d.factos.find((f) => f.campo === k);
  const nif = fact("adjudicante")?.valor;
  const raw = d.factos[0]?.origem?.raw?.split(":").pop();
  const worst = d.veredictos.some((v) => v.resultado === "nao_cumpre") ? "nao_cumpre" : d.veredictos.length ? "cumpre" : null;

  return (
    <>
      <div className="object-head">
        <div className="object-icon"><Icon icon="document" size={22} /></div>
        <div className="object-title">
          <div className="eyebrow">Procedimento BASE</div>
          <h1 className="mono">{shortId(d.procedimento)}</h1>
        </div>
        {worst && <Tag large intent={worst === "nao_cumpre" ? "danger" : "success"} icon={worst === "nao_cumpre" ? "error" : "tick-circle"}>{worst === "nao_cumpre" ? "Não cumpre" : "Cumpre"}</Tag>}
      </div>
      <div className="props">
        {["adjudicante", "preco_base", "tipo_contrato", "tipo_procedimento"].map((k) => fact(k) && (
          <div key={k}><span>{LABEL[k]}</span><b className={k === "adjudicante" || k === "preco_base" ? "mono" : ""}>{show(fact(k))}</b></div>
        ))}
      </div>

      <div className="two">
        <div>
          {d.veredictos.length === 0 && (
            <Panel icon="help" title="Veredicto"><p>Ainda não há uma regra que se aplique a este procedimento, ou faltam dados.</p></Panel>
          )}
          {d.veredictos.map((v) => <Verdict key={v.regra.id} v={v} />)}
        </div>
        <div>
          <Panel icon="properties" title="Dados do contrato" flush>
            <dl className="facts">
              {d.factos.map((f) => (
                <div key={f.id}><dt>{LABEL[f.campo] || f.campo}</dt><dd>{show(f)}</dd></div>
              ))}
            </dl>
          </Panel>
          <Panel icon="link" title="Ligações">
            <div className="links">
              {d.veredictos.length > 0 && <Button fill alignText="left" intent="primary" icon="export" rightIcon="arrow-right" text="Relatório descarregável" onClick={() => go("r", d.procedimento)} />}
              {nif && <Button fill alignText="left" icon="office" rightIcon="arrow-right" text="Todos os contratos desta entidade" onClick={() => go("e", nif)} />}
              {raw && <AnchorButton fill alignText="left" icon="share" rightIcon="arrow-top-right" text="Abrir no portal BASE" href={`https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=${raw}`} target="_blank" rel="noopener noreferrer" />}
            </div>
          </Panel>
        </div>
      </div>
    </>
  );
}
