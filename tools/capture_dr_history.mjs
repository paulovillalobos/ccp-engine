// Captures the opened "Ver alterações ao texto" view of one CCP article from diariodarepublica.pt.
// Passive: one load of the consolidated page + one click on the article's history link; nothing is submitted.
//   node capture_historico.mjs 20 113 136
import { spawn } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const CONSOLIDADO = "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475";
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "ccp-dr-"))}`, "about:blank"], { stdio: "ignore" });

async function page() {
  for (let i = 0; i < 50; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const p = list.find((t) => t.type === "page");
      if (p) return p.webSocketDebuggerUrl;
    } catch {}
    await sleep(200);
  }
  throw new Error("chrome did not start");
}

const ws = new WebSocket(await page());
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pending = new Map();
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
};
const send = (method, params = {}) => new Promise((r) => { const n = ++id; pending.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result.result.value;

const report = [];
for (const art of process.argv.slice(2)) {
  const started = new Date().toISOString();
  await send("Page.navigate", { url: CONSOLIDADO });
  await sleep(15000); // the consolidated page renders ~750k characters client-side
  const clicked = await evaluate(`(() => {
    const links = [...document.querySelectorAll('a')].filter(a => /Ver altera/i.test(a.textContent));
    const heads = [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && /^Artigo \\d+\\.º(-[A-Z])?$/.test(e.textContent.trim()));
    const h = heads.find(e => e.textContent.trim() === 'Artigo ${art}.º');
    if (!h) return { ok: false, why: 'heading not found' };
    const next = heads[heads.indexOf(h) + 1];
    const link = links.find(l => (h.compareDocumentPosition(l) & Node.DOCUMENT_POSITION_FOLLOWING) &&
      (!next || (next.compareDocumentPosition(l) & Node.DOCUMENT_POSITION_PRECEDING)));
    if (!link) return { ok: false, why: 'no history link between this heading and the next' };
    link.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    return { ok: true };
  })()`);
  if (!clicked.ok) { report.push({ art, started, ...clicked }); continue; }
  await sleep(8000);
  const view = await evaluate(`({ url: location.href, inicial: !!document.querySelector('.versaoinicialText'),
    versions: document.querySelectorAll('[id$="-DetalheArtigo"]').length,
    html: '<!-- captured ' + new Date().toISOString() + ' from ' + location.href + ' (opened history view, live DOM) -->\\n' + document.documentElement.outerHTML })`);
  writeFileSync(`art${art}-historico.html`, view.html);
  report.push({ art, started, url: view.url, versions_listed: view.versions, has_versao_inicial: view.inicial, bytes: view.html.length });
}
console.log(JSON.stringify(report, null, 1));
ws.close();
chrome.kill();
