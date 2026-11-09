import { Icon } from "@blueprintjs/core";

// A Palantir-style panel: a thin header bar with an icon and an uppercase title, then the body.
export default function Panel({ icon, title, right, children, className = "", flush }) {
  return (
    <section className={`panel ${className}`}>
      <header className="panel-head">
        <span><Icon icon={icon} size={14} /> {title}</span>
        {right}
      </header>
      <div className={flush ? "" : "panel-body"}>{children}</div>
    </section>
  );
}
