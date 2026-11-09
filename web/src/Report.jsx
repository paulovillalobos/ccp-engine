import { useEffect, useState } from "react";
import { Button, Icon, NonIdealState, Spinner, Tag } from "@blueprintjs/core";
import JSZip from "jszip";
import { api, euro, shortId } from "./api.js";
import { go } from "./App.jsx";
import Panel from "./Panel.jsx";

const article = (p) => (p || "").replace(/^ccp:art(\d+)\.([a-z])$/, "CCP, art. $1.º, alínea $2)").replace(/^ccp:art(\d+)\.(\d+)$/, "CCP, art. $1.º, n.º $2");
const val = (v) => (v == null ? "—" : Array.isArray(v) ? v.join(", ") : typeof v === "number" ? v.toLocaleString("pt-PT") : String(v));
const json = (x) => JSON.stringify(x, null, 2) + "\n";

// The files of the ZIP: each part of the report on its own, so every link of the chain can be checked separately.
function files(r) {
  const v = r.veredictos;
  const law = v.map((x) => `${article(x.passagem)} (versão de ${x.versao})\n\n${x.citacao}\n`).join("\n");
  const commit = v[0]?.reproducao.commit || "<commit>";
  return {
    "LEIA-ME.txt": `Relatório do CCP Engine para o procedimento ${shortId(r.procedimento)} (${r.procedimento}).
Gerado em ${r.gerado_em}, verificação ${r.corrida}.

registos-fonte.json  de onde vieram os dados: ficheiro oficial, id do registo e a impressão SHA-256 do registo
factos.json          cada facto, o campo da fonte de onde veio e o adaptador que o leu
lei.txt              o artigo citado, palavra por palavra, na versão em vigor
regra.json           a regra que o sistema aplicou e os leitores que a fixaram
calculo.json         cada passo do motor
veredicto.json       o resultado guardado, com o manifesto (lei, pacote, commit, registo)
reproducao.json      o motor corrido de novo sobre os mesmos factos, e se deu o mesmo resultado
reproduzir.sh        como correr o motor no seu computador
relatorio.json       tudo junto
`,
    "registos-fonte.json": json(r.entrada.registos),
    "factos.json": json(r.entrada.factos),
    "lei.txt": law,
    "regra.json": json(v.map((x) => ({ regra: x.regra_completa, leitores: x.leitores }))),
    "calculo.json": json(v.map((x) => ({ regra: x.regra.id, passos: x.passos }))),
    "veredicto.json": json(v.map(({ passos, regra_completa, leitores, codigo, reproducao, ...rest }) => rest)),
    "reproducao.json": json(v.map((x) => ({ regra: x.regra.id, guardado: x.resultado, ...x.reproducao }))),
    "reproduzir.sh": `#!/bin/sh
# Corre o motor do CCP Engine sobre o procedimento ${r.procedimento} e mostra o relatório.
# Precisa de acesso de leitura à base de dados (variáveis em .env, ver deploy/README.md).
git clone https://${v[0]?.codigo.repositorio || "github.com/paulovillalobos/ccp-engine"} ccp-engine && cd ccp-engine
git checkout ${commit}
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -I db/api.py --port 5341 &
sleep 30
curl -s http://127.0.0.1:5341/v1/procedimentos/${r.procedimento}/relatorio
`,
    "relatorio.json": json(r),
  };
}

async function downloadZip(r) {
  const zip = new JSZip();
  const dir = zip.folder(`relatorio-${shortId(r.procedimento)}`);
  for (const [name, text] of Object.entries(files(r))) dir.file(name, text);
  const blob = await zip.generateAsync({ type: "blob" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `relatorio-${shortId(r.procedimento)}.zip`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

function Step({ s }) {
  const tone = s.ok ? "ok" : "bad";
  return (
    <div className={`trace-row trace-${tone} ${s.decide ? "trace-decide" : ""}`}>
      <Icon icon={s.ok ? "tick" : "cross"} className={s.ok ? "c-ok" : "c-bad"} />
      <code className="mono">{s.teste}{s.valor != null && <span> · valor: {val(s.valor)}</span>}</code>
      <span className="trace-effect">{s.efeito}</span>
    </div>
  );
}

// One procedure's report: entrada → lógica → cálculo → resultado, then PDF (print) and ZIP downloads.
export default function Report({ unit }) {
  const [s, setS] = useState({ loading: true });
  useEffect(() => {
    setS({ loading: true });
    api.report(unit).then((r) => setS({ r })).catch((e) => setS({ error: e.message }));
  }, [unit]);

  if (s.loading) return <div className="center report-wait"><Spinner size={32} /><p>A correr o motor de novo sobre este procedimento…</p></div>;
  if (s.error) return <NonIdealState icon="error" title={s.error} />;
  const r = s.r;
  const bad = r.veredictos.some((v) => v.resultado === "nao_cumpre");
  const by = Object.fromEntries(r.entrada.factos.map((f) => [f.campo, f.valor]));

  return (
    <div className="report">
      <div className="report-actions no-print">
        <Button minimal icon="arrow-left" text="Procedimento" onClick={() => go("p", unit)} />
        <span className="grow" />
        <Button icon="archive" text="Descarregar ZIP" onClick={() => downloadZip(r)} />
        <Button intent="primary" icon="document" text="Descarregar PDF" onClick={() => window.print()} />
      </div>

      <header className="report-cover">
        <div>
          <div className="eyebrow">CCP Engine · Relatório de veredicto</div>
          <h1>Procedimento <span className="mono">{shortId(r.procedimento)}</span></h1>
          <p>{r.veredictos.map((v) => v.regra.titulo).join(" · ") || "Sem veredicto nesta verificação"}</p>
        </div>
        {r.veredictos.length > 0 && <Tag large intent={bad ? "danger" : "success"} icon={bad ? "error" : "tick-circle"}>{bad ? "Não cumpre a lei" : "Cumpre a lei"}</Tag>}
      </header>
      <div className="props">
        <div><span>Entidade (NIF)</span><b className="mono">{val(by.adjudicante)}</b></div>
        <div><span>Preço base</span><b className="mono">{by.preco_base != null ? euro(by.preco_base) : "—"}</b></div>
        <div><span>Verificação</span><b className="mono">{(r.corrida || "").replace("corrida:", "")}</b></div>
        <div><span>Relatório gerado</span><b className="mono">{r.gerado_em}</b></div>
      </div>

      <Panel icon="import" title="1 · Entrada: o que o sistema leu">
        <h3>Registo oficial de onde vieram os dados</h3>
        {r.entrada.registos.map((g) => (
          <dl key={g.id} className="proof">
            <dt>Fonte</dt><dd>Portal BASE (IMPIC), ficheiro publicado em dados.gov.pt</dd>
            <dt>Ficheiro</dt><dd className="mono hash"><a href={g.url} target="_blank" rel="noopener noreferrer">{g.url?.split("/").pop()}</a></dd>
            <dt>Registo</dt><dd className="mono">contrato {g.id_na_fonte}</dd>
            <dt>SHA-256</dt><dd className="mono hash">{g.sha256}</dd>
            <dt>Capturado</dt><dd className="mono">{g.capturado_em}</dd>
          </dl>
        ))}
        <h3>Factos extraídos</h3>
        <div className="scroll">
          <table className="rtable">
            <thead><tr><th>Campo na fonte</th><th /><th>Facto</th><th>Valor</th><th>Adaptador</th></tr></thead>
            <tbody>
              {r.entrada.factos.map((f) => (
                <tr key={f.id}><td className="mono">{f.campo_na_fonte || "—"}</td><td className="c-ok">→</td><td className="mono">{f.campo}</td><td className="mono">{val(f.valor)}</td><td className="mono">{f.adaptador}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>

      {r.veredictos.map((v) => (
        <div key={v.regra.id}>
          <Panel icon="book" title="2 · Lógica: a lei e a regra">
            <blockquote className="law">«{v.citacao}»<cite><Icon icon="book" size={12} /> {article(v.passagem)} · versão em vigor desde {v.versao} · {v.manifesto.lei}</cite></blockquote>
            <h3>A regra, como o sistema a guarda</h3>
            <pre className="code">{json({ id: v.regra_completa.id, revisao: v.regra_completa.revision, tipo: v.regra_completa.type, condicoes: v.regra_completa.conditions, parametros: v.regra_completa.params, em_vigor: [v.regra_completa.valid_from, v.regra_completa.valid_to] })}</pre>
            <h3>Quem fixou a regra</h3>
            <div className="readers">
              {v.leitores.map((l) => (
                <div key={l.leitor + l.evento}><span>Leitor {l.familia}</span><b className="mono">{l.leitor}</b><p>{l.em} · {l.evento} · leu {val(l.passagens)}</p></div>
              ))}
              <div><span>Resultado</span><b>Concordaram</b><p>Regra fixada, revisão {v.regra.revision}, estado {v.regra.estado}</p></div>
            </div>
          </Panel>

          <Panel icon="calculator" title="3 · Cálculo: os passos do motor">
            <div className="trace">{v.passos.map((s, i) => <Step key={i} s={s} />)}</div>
            <h3>O código que decide · {v.codigo.repositorio} @ {v.codigo.commit}</h3>
            <pre className="code">{v.codigo.funcoes.holds}</pre>
            <p className="note">Ficheiros: {v.codigo.ficheiros.join(", ")}.</p>
          </Panel>

          <Panel icon="endorsed" title="4 · Resultado e reprodução">
            <div className={`rerun ${v.reproducao.igual ? "rerun-ok" : "rerun-bad"}`}>
              <Icon icon={v.reproducao.igual ? "tick-circle" : "warning-sign"} size={20} />
              <div>
                <b>{v.reproducao.igual ? "Reproduzido: o motor, corrido de novo agora, dá o mesmo resultado." : "Atenção: o motor, corrido de novo agora, dá outro resultado."}</b>
                <p className="mono">guardado: {v.resultado} · agora: {v.reproducao.resultado_agora || "—"} · commit {v.reproducao.commit} · {v.reproducao.em}</p>
              </div>
            </div>
            <dl className="proof">
              <dt>Resultado</dt><dd className="mono">{v.resultado}</dd>
              <dt>Regra</dt><dd className="mono">{v.regra.id}</dd>
              <dt>Data do facto</dt><dd className="mono">{v.valido_em}</dd>
              <dt>Lei</dt><dd className="mono">{v.manifesto.lei}</dd>
              <dt>Pacote</dt><dd className="mono">{v.manifesto.pacote}</dd>
              <dt>Motor</dt><dd className="mono">{v.manifesto.motor} @ {v.manifesto.commit}</dd>
              <dt>Registo</dt><dd className="mono hash">{v.manifesto.registo}</dd>
            </dl>
          </Panel>
        </div>
      ))}
      <p className="note print-only">Relatório gerado pelo CCP Engine em {r.gerado_em} para {r.procedimento}.</p>
    </div>
  );
}
