// Read-only client for db/api.py. Every call is a GET on /v1; Vite proxies it in development.
async function get(path) {
  const r = await fetch(path, { headers: { Accept: "application/json" } });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(body.erro || `HTTP ${r.status}`);
  return body;
}

export const api = {
  stats: () => get("/v1/estatisticas"),
  verdicts: ({ resultado, apos, limite = 50 } = {}) => {
    const q = new URLSearchParams({ limite: String(limite) });
    if (resultado) q.set("resultado", resultado);
    if (apos) q.set("apos", apos);
    return get(`/v1/veredictos?${q}`);
  },
  report: (unit) => get(`/v1/procedimentos/${encodeURIComponent(unit)}/relatorio`),
  procedure: (unit) => get(`/v1/procedimentos/${encodeURIComponent(unit)}`),
  // Every verdict of one adjudicante, page after page, so the counts are the whole run's.
  buyerAll: async (nif, max = 50) => {
    let all = [], apos = "";
    for (let i = 0; i < max; i++) {
      const q = new URLSearchParams({ limite: "200" });
      if (apos) q.set("apos", apos);
      const d = await get(`/v1/entidades/${nif}/veredictos?${q}`);
      all = all.concat(d.veredictos);
      if (!d.seguinte) return { veredictos: all, completo: true };
      apos = d.seguinte;
    }
    return { veredictos: all, completo: false };
  },
};

export const shortId = (unit) => unit.replace("proc:base:idproc-", "");
export const unitOf = (id) => (id.startsWith("proc:base:") ? id : `proc:base:idproc-${id}`);
export const euro = (n) => Number(n).toLocaleString("pt-PT", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
export const num = (n) => Number(n).toLocaleString("pt-PT");

// The verdict in one plain sentence. A limiar detail reads «preco_base=350000 lt 150000; …».
export function plain(v) {
  if (v.resultado === "nao_avaliado") // D96/D97: an abstention, in its own words
    return { text: (v.detalhe || "").replace(/ \(product_rule:[^)]*\)/, "").split("; início entre")[0] };
  const a = v.agregado; // D96: a cumulative limit (CCP art. 113.º n.º 2): the contracts already adjudicated to the same entity
  if (a) {
    const lim = /cumpre se \w+ ([\d.]+)/.exec(v.detalhe || "");
    const limit = lim ? euro(lim[1]) : "o limite";
    const n = a.sure.length;
    return v.resultado === "nao_cumpre"
      ? { text: `A entidade já tinha adjudicado ${euro(a.sum_min)} ao mesmo adjudicatário em ${n} contrato${n === 1 ? "" : "s"} (de ${a.window[0]} a ${a.window[1]}). A lei não deixa convidá-lo a partir de ${limit}.` }
      : { text: `Ao mesmo adjudicatário, ${euro(a.sum_min)} em ${n} contrato${n === 1 ? "" : "s"} anteriores: abaixo de ${limit}.` };
  }
  const m = /^preco_base=([\d.]+) lt ([\d.]+)/.exec(v.detalhe || "");
  if (m) {
    const [price, limit] = [euro(m[1]), euro(m[2])];
    return v.resultado === "nao_cumpre"
      ? { price, limit, text: `Preço base de ${price}. A lei só permite este procedimento abaixo de ${limit}.` }
      : { price, limit, text: `Preço base de ${price}, abaixo do limite de ${limit} que a lei fixa.` };
  }
  return { text: v.regra.titulo || v.regra.id };
}
