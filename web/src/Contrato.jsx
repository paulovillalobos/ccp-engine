import { AnchorButton } from "@blueprintjs/core";
import { go } from "./App.jsx";
import Panel from "./Panel.jsx";

// D93: what the BASE portal shows of a contract, in the portal's own order and words. Copied as published: no field here
// is read by a rule; a missing row is a field BASE leaves empty.
const ROWS = [
  ["objectoContrato", "Objeto do contrato"],
  ["descContrato", "Descrição"],
  ["dataPublicacao", "Data da publicação"],
  ["tipoContrato", "Tipo de contrato"],
  ["tipoprocedimento", "Tipo de procedimento"],
  ["fundamentacao", "Fundamentação"],
  ["fundamentAjusteDireto", "Fundamentação do ajuste direto"],
  ["regime", "Regime"],
  ["adjudicante", "Entidade adjudicante"],
  ["adjudicatarios", "Entidade adjudicatária"],
  ["concorrentes", "Concorrentes"],
  ["CPV", "CPV"],
  ["cpv", "CPV"],
  ["precoEstimadoProc", "Valor estimado do procedimento"],
  ["precoBaseProcedimento", "Preço base do procedimento"],
  ["precoContratual", "Preço contratual"],
  ["dataDecisaoAdjudicacao", "Data da decisão de adjudicação"],
  ["dataCelebracaoContrato", "Data do contrato"],
  ["prazoExecucao", "Prazo de execução"],
  ["localExecucao", "Local de execução"],
  ["TipoCriterioAdjudicacao", "Critério de adjudicação"],
  ["Lotes", "Lotes e propostas"],
  ["entidadesConvidadas", "Entidades convidadas"],
  ["numAcordoQuadro", "N.º do acordo-quadro"],
  ["DescrAcordoQuadro", "Acordo-quadro"],
  ["ProcedimentoCentralizado", "Procedimento centralizado"],
  ["compraConjunta", "Compra conjunta"],
  ["CritMateriais", "Critérios materiais"],
  ["ContratEcologico", "Critérios ambientais"],
  ["justifNReducEscrContrato", "Justificação para não redução a escrito"],
  ["nAnuncio", "Anúncio"],
  ["Observacoes", "Observações"],
];
const EXEC = [
  ["estadoContrato", "Estado do contrato"],
  ["tipoFimContrato", "Causa da extinção do contrato"],
  ["dataFechoContrato", "Data do fecho do contrato"],
  ["PrecoTotalEfetivo", "Preço total efetivo"],
  ["CausasAlteraPrazo", "Causas das alterações ao prazo"],
  ["CausasAlteraPreco", "Causas das alterações ao preço"],
];
// money to the cent, as BASE publishes it (168.780,91 €)
const cents = (n) => Number(n).toLocaleString("pt-PT", { style: "currency", currency: "EUR", minimumFractionDigits: 2 });
const MONEY = new Set(["precoEstimadoProc", "precoBaseProcedimento", "precoContratual", "PrecoTotalEfetivo"]);
const ENTITY = new Set(["adjudicante", "adjudicatarios", "concorrentes", "entidadesConvidadas"]);

// BASE writes an entity as «502177080 - Município de Mafra» (older dumps, and concorrentes as «500589593-AOF - …») or
// as an object {nifEntContrato, descEntContrato, NUTsDesc, adjudicatarioPME, …} (newer dumps): the NIF and the name.
function entity(x) {
  if (x && typeof x === "object") return { nif: x.nifEntContrato, name: x.descEntContrato, where: x.NUTsDesc, pme: x.adjudicatarioPME === "Sim" };
  const m = String(x).match(/^(\d{9})\s*-\s*(.*)$/);
  return m ? { nif: m[1], name: m[2] } : { name: String(x) };
}

function Entity({ x }) {
  const e = entity(x);
  return (
    <span className="entity">
      {e.nif ? <a onClick={() => go("e", e.nif)}>{e.name || e.nif}</a> : e.name}
      {e.nif && <span className="mono">{e.nif}</span>}
      {e.where && <span className="meta">{e.where}</span>}
      {e.pme && <span className="meta">PME</span>}
    </span>
  );
}

// «2026-05-04» (newer dumps) or «04/05/2026» (older): as the portal shows it, 04-05-2026
const DATE = new Set(["dataPublicacao", "dataCelebracaoContrato", "dataDecisaoAdjudicacao", "dataFechoContrato"]);
const date = (v) => { const s = String(v); const m = s.match(/^(\d{4})-(\d{2})-(\d{2})/); return m ? `${m[3]}-${m[2]}-${m[1]}` : s.replace(/\//g, "-"); };

// anything else BASE gives as an object: its values, joined
const text = (x) => (x && typeof x === "object" ? Object.values(x).filter((v) => v != null && v !== "").join(" · ") : String(x));

function value(k, v) {
  if (MONEY.has(k)) return <span className="mono">{cents(v)}</span>;
  if (k === "prazoExecucao") return `${v} dias`;
  if (DATE.has(k)) return <span className="mono">{date(v)}</span>;
  const list = Array.isArray(v) ? v : [v];
  if (ENTITY.has(k)) return <div className="vlist">{list.map((x, i) => <Entity key={i} x={x} />)}</div>;
  // newer dumps: {cpvID, cpvdescricao, cpvValor, CPVObjeto}
  if (k === "CPV") return <div className="vlist">{list.map((x, i) => (
    <span key={i}><span className="mono">{x.cpvID}</span> {x.cpvdescricao}{x.cpvValor ? <span className="mono"> ({cents(x.cpvValor)})</span> : null}</span>
  ))}</div>;
  // one per lot: its number, the award criterion and the number of bids
  if (k === "Lotes") return <div className="vlist">{list.map((x, i) => (
    <span key={i}>
      {list.length > 1 && <b>Lote {x.numLot}{x.designacaoLote ? ` — ${x.designacaoLote}` : ""}: </b>}
      {[x.criterioAdjudicacaoTipo, x.criterioAdjudicacaoTipoFator].filter(Boolean).join(", ")}
      {x.NumPropostas != null && <span className="meta-inline"> · {x.NumPropostas} {x.NumPropostas === 1 ? "proposta" : "propostas"}</span>}
    </span>
  ))}</div>;
  if (k === "cpv") return <div className="vlist">{list.map((x, i) => { const [code, ...rest] = text(x).split(" - "); return <span key={i}><span className="mono">{code}</span> {rest.join(" - ")}</span>; })}</div>;
  return <div className="vlist">{list.map((x, i) => <span key={i}>{text(x)}</span>)}</div>;
}

function Rows({ c, rows }) {
  return (
    <dl className="facts">
      {rows.filter(([k]) => c[k] != null).map(([k, label]) => (
        <div key={k}><dt>{label}</dt><dd>{value(k, c[k])}</dd></div>
      ))}
    </dl>
  );
}

export default function Contrato({ c, many }) {
  const executed = EXEC.some(([k]) => c[k] != null);
  return (
    <Panel icon="document-open" title={many ? `Contrato ${c.id}` : "Contrato (BASE)"} flush>
      <Rows c={c} rows={ROWS} />
      {executed && <><div className="panel-sub">Execução do contrato</div><Rows c={c} rows={EXEC} /></>}
      <div className="panel-links">
        {c.linkPecasProc && <AnchorButton minimal small icon="folder-open" text="Peças do procedimento" href={c.linkPecasProc} target="_blank" rel="noopener noreferrer" />}
        <AnchorButton minimal small icon="share" text="Abrir no portal BASE" href={c.url} target="_blank" rel="noopener noreferrer" />
      </div>
    </Panel>
  );
}
