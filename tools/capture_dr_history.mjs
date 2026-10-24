// Captures the "Ver alterações ao texto" view of every article of the consolidated CCP that has one, from
// diariodarepublica.pt, by walking the articles in order: the consolidated page is loaded ONCE, then each article is
// reached by one click on "Artigo seguinte" and its history opened by one click on "Ver alterações ao texto".
// Every page is read once; at least 3 s between clicks; nothing is submitted; a page that fails is noted and skipped
// (never retried in the same run). Each history view is written as <out>/<seq>.html with an entry in <out>/manifest.json;
// tools/record_histories.py records them through engine.sources.record_raw.
//   node tools/capture_dr_history.mjs --out DIR [--skip ccp-art20,ccp-art113,ccp-art136] [--max 900] [--attach PORT]
//   node tools/capture_dr_history.mjs --out DIR --urls URL1,URL2     (an article's detail address, read by one GET,
//        then one click on its "Ver alterações ao texto"; for articles a walk recorded but could not name)
//   node tools/capture_dr_history.mjs --out DIR --attach PORT --targets "Anexo I,Anexo II"   (named index entries only:
//        one click on the entry in the open "Índice", one on its "Ver alterações ao texto")
// Ids: ccp-artN (code), ccp-dl-artN (the approving decree's own articles), ccp-anexo-i (the code's annexes).
// --attach continues from the view already open in a running headless Chrome (a previous run's), so the consolidated
// page is not loaded again. The first history link of the consolidated page is the act's own ("Ato"), not an article's:
// the walk leaves it through "Voltar ao detalhe do artigo" and goes on by "Artigo seguinte".
// Version ccp-capture-dr-history-0.4 (0.1 reloaded the consolidated page per article; 0.2 walks it once; 0.3 keeps the
// DOM of every failure; 0.4 starts from the act view through its index and can attach to the Chrome a failed run left open; 0.5
// captures named index entries: the walk by "Artigo seguinte" ends at the last article and never reaches the annexes;
// 0.6 reads "Artigo 410-A" (no º) as an article and captures given detail addresses).
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const CONSOLIDADO = "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475";
const GAP_MS = 3000;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const arg = (name, dflt) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const OUT = arg("--out", null);
const SKIP = new Set((arg("--skip", "") || "").split(",").filter(Boolean));
const MAX = parseInt(arg("--max", "900"), 10);
const ATTACH = arg("--attach", null);
const TARGETS = (arg("--targets", "") || "").split(",").map((x) => x.trim()).filter(Boolean);
const URLS = (arg("--urls", "") || "").split(",").map((x) => x.trim()).filter(Boolean);
const PORT = ATTACH ? parseInt(ATTACH, 10) : 9334;
if (!OUT) { console.error("--out DIR is required"); process.exit(2); }
mkdirSync(OUT, { recursive: true });

const chrome = ATTACH ? null : spawn(CHROME, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "ccp-dr-"))}`, "about:blank"], { stdio: "ignore" });

async function pageSocket() {
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

const ws = new WebSocket(await pageSocket());
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pending = new Map();
ws.onmessage = (m) => { const msg = JSON.parse(m.data); if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); } };
const send = (method, params = {}) => new Promise((r) => { const n = ++id; pending.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result.result?.value;

// what the current view is: the article title, its structural path, whether the history (versions) is open
const STATE = `(() => {
  const t = [...document.querySelectorAll('.tituloletters')].map(e => e.textContent.trim());
  const path = document.querySelector('.fullpathletters')?.textContent.trim() || '';
  const home = document.querySelector('a[aria-current="page"][href$="2008-34455475"]');
  const crumb = home && home.parentElement.lastElementChild !== home ? home.parentElement.lastElementChild.textContent.trim() : '';
  return { url: location.href, title: t.find(Boolean) || crumb || null, path,
           back: [...document.querySelectorAll('a')].some(a => /Voltar ao detalhe/.test(a.textContent)), versions: document.querySelectorAll('[id$="-DetalheArtigo"]').length,
           inicial: !!document.querySelector('.versaoinicialText'),
           histLink: [...document.querySelectorAll('a')].some(a => /Ver altera/i.test(a.textContent)),
           next: [...document.querySelectorAll('a')].some(a => /Artigo seguinte/.test(a.textContent)) };
})()`;
const click = (re) => evaluate(`(() => { const a = [...document.querySelectorAll('a')].find(a => ${re}.test(a.textContent));
  if (!a) return false; a.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); return true; })()`);
async function waitFor(pred, ms = 25000) {
  const t0 = Date.now();
  let s = null;
  while (Date.now() - t0 < ms) { s = await evaluate(STATE); if (s && pred(s)) return s; await sleep(500); }
  return s;
}
const idOf = (s) => {
  const an = /^Anexo ([IVXLC]+)$/.exec(s.title || "");
  if (an) return `ccp-anexo-${an[1].toLowerCase()}`;
  const m = /^Artigo (\d+)(?:\.º)?(?:-([A-Z]+))?$/.exec(s.title || "");  // the DR prints "Artigo 410-A" too
  if (!m) return null;
  const inCode = /^Anexo\b/.test(s.path);
  return `ccp-${inCode ? "" : "dl-"}art${m[1]}${m[2] ? "-" + m[2].toLowerCase() : ""}`;
};

// on any failure the live DOM is kept as <out>/failure-<n>.html so the next run is fixed from evidence, not guessed
const dumpFailure = async (why, at) => {
  const n = manifest.failures.length + 1;
  const html = await evaluate("document.documentElement ? document.documentElement.outerHTML : ''").catch(() => "");
  writeFileSync(join(OUT, `failure-${n}.html`), html || "");
  manifest.failures.push({ at, why, dom: `failure-${n}.html` });
};
const manifest = { tool: "ccp-capture-dr-history-0.6", consolidated: CONSOLIDADO, started: new Date().toISOString(), pages: [], failures: [], visited: [] };
const save = () => writeFileSync(join(OUT, "manifest.json"), JSON.stringify(manifest, null, 1));

const quit = (code) => { save(); ws.close(); if (chrome) chrome.kill(); process.exit(code); };
let s;
if (URLS.length) {
  let seqU = 0;
  for (const url of URLS) {
    if (seqU || manifest.visited.length) await sleep(GAP_MS);
    await send("Page.navigate", { url });
    s = await waitFor((x) => x.title && (x.histLink || x.versions > 0 || x.inicial), 60000);
    manifest.visited.push({ title: s && s.title, path: s && s.path, url, id: s && idOf(s), history_link: s && s.histLink });
    if (!s || !idOf(s)) { await dumpFailure(`${url}: no article view within 60 s`, url); save(); continue; }
    if (s.histLink && !(s.versions > 0 || s.inicial)) {
      await sleep(GAP_MS);
      await click("/Ver altera/i");
      s = await waitFor((x) => x.title && (x.versions > 0 || x.inicial) && !x.histLink);
    }
    if (s && (s.versions > 0 || s.inicial)) {
      seqU += 1;
      const html = await evaluate(`'<!-- captured ' + new Date().toISOString() + ' from ' + location.href + ' (opened history view, live DOM) -->\\n' + document.documentElement.outerHTML`);
      const file = `${String(seqU).padStart(4, "0")}.html`;
      writeFileSync(join(OUT, file), html);
      manifest.pages.push({ seq: seqU, id: idOf(s), title: s.title, path: s.path, url: s.url, captured_at: new Date().toISOString().replace(/\.\d+Z$/, "Z"),
                            versions_listed: s.versions, has_versao_inicial: s.inicial, file, bytes: Buffer.byteLength(html) });
    } else {
      await dumpFailure(`${url}: no history view`, url);
    }
    save();
  }
  manifest.finished = new Date().toISOString();
  console.log(JSON.stringify({ pages: manifest.pages.length, visited: manifest.visited.length, failures: manifest.failures.length }));
  quit(0);
}
if (ATTACH) {
  s = await evaluate(STATE);
  manifest.attached = { port: PORT, url: s && s.url, title: s && s.title };
} else {
  await send("Page.navigate", { url: CONSOLIDADO });
  await sleep(15000); // one load of the consolidated page (~2.6 MB rendered client-side)
  // the first "Ver alterações" link of the page is the act's own history ("Ato")
  const started = await click("/Ver altera/i");
  if (!started) { await dumpFailure("no history link on the consolidated page", "start"); quit(1); }
  s = await waitFor((x) => x.url !== CONSOLIDADO && x.title && (x.versions > 0 || x.inicial || x.next), 60000);
}
if (!s || !s.title) { await dumpFailure("the first view did not render within 60 s", s && s.url); quit(1); }
if (TARGETS.length) {
  let seqT = 0;
  for (const target of TARGETS) {
    await sleep(GAP_MS);
    const before = s.url + "|" + s.title;
    const ok = await evaluate(`(() => { const e = [...document.querySelectorAll('a span')].find(e => e.textContent.trim() === ${JSON.stringify(target)});
      if (!e) return false; e.closest('a').dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); return true; })()`);
    if (!ok) { manifest.failures.push({ at: target, why: "no index entry with this text" }); save(); continue; }
    s = await waitFor((x) => x.title === target && (x.url + "|" + x.title) !== before && (x.histLink || x.versions > 0 || x.inicial));
    manifest.visited.push({ title: s && s.title, path: s && s.path, url: s && s.url, id: s && idOf(s), history_link: s && s.histLink });
    if (!s || s.title !== target) { await dumpFailure(`${target}: the index entry did not open within 25 s`, s && s.url); save(); continue; }
    if (s.histLink && !(s.versions > 0 || s.inicial)) {
      await sleep(GAP_MS);
      await click("/Ver altera/i");
      s = await waitFor((x) => x.title === target && (x.versions > 0 || x.inicial) && !x.histLink);
    }
    if (s && (s.versions > 0 || s.inicial)) {
      seqT += 1;
      const html = await evaluate(`'<!-- captured ' + new Date().toISOString() + ' from ' + location.href + ' (opened history view, live DOM) -->\\n' + document.documentElement.outerHTML`);
      const file = `${String(seqT).padStart(4, "0")}.html`;
      writeFileSync(join(OUT, file), html);
      manifest.pages.push({ seq: seqT, id: idOf(s), title: s.title, path: s.path, url: s.url, captured_at: new Date().toISOString().replace(/\.\d+Z$/, "Z"),
                            versions_listed: s.versions, has_versao_inicial: s.inicial, file, bytes: Buffer.byteLength(html) });
    } else {
      await dumpFailure(`${target}: no history view`, s && s.url);
    }
    save();
    // back to a view that shows the index: the history view keeps it, so the next entry is clicked from here
  }
  manifest.finished = new Date().toISOString();
  save();
  console.log(JSON.stringify({ pages: manifest.pages.length, visited: manifest.visited.length, failures: manifest.failures.length }));
  ws.close();
  process.exit(0);
}
// the act's history view has no "Artigo seguinte": back to the act's detail, then its "Índice" and the index's first
// "Artigo 1.º" (the decree's article 1), from which "Artigo seguinte" walks the rest
if (!idOf(s) && !s.next && s.back) {
  manifest.visited.push({ title: s.title, path: s.path, url: s.url, id: null, history_link: s.histLink });
  await sleep(GAP_MS);
  await click("/Voltar ao detalhe/");
  s = await waitFor((x) => !x.back);
}
if (!idOf(s) && !s.next) {
  const indexOpen = () => evaluate(`[...document.querySelectorAll('a span')].some(e => e.textContent.trim() === 'Artigo 1.º')`);
  if (!(await indexOpen())) {
    await sleep(GAP_MS);
    await evaluate(`(() => { const b = [...document.querySelectorAll('button,[role=button]')].find(b => b.textContent.trim() === 'Índice');
      if (b) b.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); })()`);
    for (let i = 0; i < 30 && !(await indexOpen()); i++) await sleep(500);
  }
  await sleep(GAP_MS);
  const before = s.url + "|" + s.title;
  await evaluate(`(() => { const e = [...document.querySelectorAll('a span')].find(e => e.textContent.trim() === 'Artigo 1.º');
    if (e) e.closest('a').dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); })()`);
  s = await waitFor((x) => idOf(x) && (x.url + "|" + x.title) !== before && (x.histLink || x.next));
  if (!s || !idOf(s)) { await dumpFailure("the index's Artigo 1.º did not open an article within 25 s", s && s.url); quit(1); }
}
let seq = 0, last = null;
for (let step = 0; step < MAX && s; step++) {
  const key = idOf(s);
  manifest.visited.push({ title: s.title, path: s.path, url: s.url, id: key, history_link: s.histLink });
  if (key && key === last) { manifest.failures.push({ at: s.url, why: "Artigo seguinte did not move; walk ends" }); break; }
  last = key;
  if (key && !SKIP.has(key)) {
    if (!(s.versions > 0 || s.inicial) && s.histLink) {
      await sleep(GAP_MS);
      await click("/Ver altera/i");
      s = await waitFor((x) => x.title && (x.versions > 0 || x.inicial) && !x.histLink);
    }
    if (s.versions > 0 || s.inicial) {
      seq += 1;
      const html = await evaluate(`'<!-- captured ' + new Date().toISOString() + ' from ' + location.href + ' (opened history view, live DOM) -->\\n' + document.documentElement.outerHTML`);
      const file = `${String(seq).padStart(4, "0")}.html`;
      writeFileSync(join(OUT, file), html);
      manifest.pages.push({ seq, id: key, title: s.title, path: s.path, url: s.url, captured_at: new Date().toISOString().replace(/\.\d+Z$/, "Z"),
                            versions_listed: s.versions, has_versao_inicial: s.inicial, file, bytes: Buffer.byteLength(html) });
    } else if (s.histLink) {
      await dumpFailure(`${key}: history link clicked, no versions rendered within 25 s`, s.url);
    }
  }
  save();
  if (!s.next) break;
  await sleep(GAP_MS);
  const before = s.url + "|" + s.title;
  await click("/Artigo seguinte/");
  s = await waitFor((x) => x.title && (x.url + "|" + x.title) !== before && (x.histLink || x.next));
  if (!s || !s.title || (s.url + "|" + s.title) === before) { await dumpFailure("Artigo seguinte: no new article within 25 s; walk ends", before); break; }
}
manifest.finished = new Date().toISOString();
save();
console.log(JSON.stringify({ pages: manifest.pages.length, visited: manifest.visited.length, failures: manifest.failures.length }));
ws.close();
if (chrome) chrome.kill();
