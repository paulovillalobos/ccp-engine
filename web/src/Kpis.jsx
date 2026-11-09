import { Icon } from "@blueprintjs/core";

// A row of metric tiles with a colored edge; a tile with onClick is a filter, the active one is outlined.
export default function Kpis({ items, active }) {
  return (
    <div className="kpis">
      {items.map((k) => (
        <button key={k.label} type="button" disabled={!k.onClick} onClick={k.onClick}
          className={`kpi kpi-${k.tone || "neutral"} ${k.onClick ? "kpi-click" : ""} ${active === k.key ? "kpi-on" : ""}`}>
          <div className="kpi-label"><Icon icon={k.icon} size={12} /> {k.label}</div>
          <div className="kpi-n mono">{k.value}</div>
        </button>
      ))}
    </div>
  );
}
