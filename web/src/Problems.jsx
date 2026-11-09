import { HTMLTable, Tag } from "@blueprintjs/core";
import { go } from "./App.jsx";
import { plain, shortId } from "./api.js";

// Verdicts as a dense, clickable table: procedure, finding, price, limit, result.
export default function Problems({ items }) {
  return (
    <HTMLTable interactive compact className="grid">
      <thead>
        <tr><th>Procedimento</th><th>Constatação</th><th className="num">Preço base</th><th className="num">Limite legal</th><th>Resultado</th></tr>
      </thead>
      <tbody>
        {items.map((v) => {
          const p = plain(v);
          return (
            <tr key={v.procedimento + v.regra.id} onClick={() => go("p", v.procedimento)}>
              <td className="mono">{shortId(v.procedimento)}</td>
              <td>{v.regra.titulo || v.regra.id}</td>
              <td className="num mono">{p.price || "—"}</td>
              <td className="num mono">{p.limit || "—"}</td>
              <td><Tag minimal intent={v.resultado === "nao_cumpre" ? "danger" : "success"}>{v.resultado === "nao_cumpre" ? "Não cumpre" : "Cumpre"}</Tag></td>
            </tr>
          );
        })}
      </tbody>
    </HTMLTable>
  );
}
