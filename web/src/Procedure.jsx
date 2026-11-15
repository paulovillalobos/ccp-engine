import { useEffect, useState } from "react";
import { AnchorButton, Button, Collapse, Icon, NonIdealState, Spinner, Tag } from "@blueprintjs/core";
import { api, euro, plain, shortId } from "./api.js";
import { go } from "./App.jsx";
import Panel from "./Panel.jsx";
import Contrato from "./Contrato.jsx";

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

// D96: the contracts a cumulative limit summed, each one as BASE publishes it.
function Summed({ a }) {
  return (
    <div className="summed">
      <div className="summed-head">
        Contratos somados (entidade {a.group.adjudicante}, adjudicatário {a.group.adjudicatario}, de {a.window[0]} até antes de {a.window[1]})
      </div>
      <table className="summed-table">
        <tbody>
          {a.sure.map((c) => (
            <tr key={c.id}>
              <td className="mono"><a href={c.url} target="_blank" rel="noopener noreferrer">BASE {c.id}</a></td>
              <td className="mono">{c.data_adjudicacao || c.data_celebracao}</td>
              <td>{c.fundamento}</td>
              <td className="mono num">{euro(c.preco_contratual)}</td>
            </tr>
          ))}
          <tr className="summed-total"><td colSpan={3}>Soma</td><td className="mono num">{euro(a.sum_min)}</td></tr>
        </tbody>
      </table>
      {a.maybe.length > 0 && <p className="summed-note">{a.maybe.length} contrato(s) incerto(s) não somados (sem NIF, sem fundamento ou sem data de adjudicação).</p>}
    </div>
  );
}

// D96: the engine abstains (a declared special regime, a special-sector buyer): no verdict, the reason instead.
function Abstained({ v }) {
  return (
    <Panel icon="take-action" title="Veredicto" className="edge-neutral">
      <div className="verdict-top">
        <Icon icon="disable" size={28} />
        <div>
          <h2>Não decidível</h2>
          <p className="answer-text">{(v.detalhe || "").replace(/ \(product_rule:[^)]*\)/, "").split("; início entre")[0]}</p>
        </div>
      </div>
      <dl className="proof">
        <dt>Regra</dt><dd className="mono">{v.regra.id}</dd>
        <dt>Motivo</dt><dd className="mono">{v.motivo}</dd>
        <dt>Registo</dt><dd className="mono hash">{v.manifesto.registo}</dd>
      </dl>
    </Panel>
  );
}

function Verdict({ v }) {
  const [open, setOpen] = useState(false);
  if (v.resultado === "nao_avaliado") return <Abstained v={v} />;
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
      {v.prova_documental && (
        <blockquote className="law doc-proof">
          «…{v.prova_documental.citacao}…»
          <cite><Icon icon="document" size={12} /> {v.prova_documental.documento}{v.prova_documental.pagina ? `, p. ${v.prova_documental.pagina}` : ""}
            {v.prova_documental.url && <> · <a href={v.prova_documental.url} target="_blank" rel="noopener noreferrer">documento</a></>}</cite>
        </blockquote>
      )}
      {v.agregado && <Summed a={v.agregado} />}
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
  const worst = d.veredictos.some((v) => v.resultado === "nao_cumpre") ? "nao_cumpre" : d.veredictos.some((v) => v.resultado === "cumpre") ? "cumpre" : null;

  return (
    <>
      <div className="object-head">
        <div className="object-icon"><Icon icon="document" size={22} /></div>
        <div className="object-title">
          <div className="eyebrow">Procedimento BASE</div>
          <h1 className="mono">{shortId(d.procedimento)}</h1>
          {d.contratos?.[0]?.objectoContrato && <div className="object-sub">{d.contratos[0].objectoContrato}</div>}
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
          {(d.contratos || []).map((c) => <Contrato key={c.id} c={c} many={d.contratos.length > 1} />)}
        </div>
        <div>
          <Panel icon="properties" title="Dados usados na verificação" flush>
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
