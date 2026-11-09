import { useState } from "react";
import { Button, InputGroup } from "@blueprintjs/core";
import { go } from "./App.jsx";
import { unitOf } from "./api.js";

// One box: a 9-digit NIF opens the buyer, anything else is read as a BASE procedure id.
export default function Search() {
  const [q, setQ] = useState("");
  const v = q.trim();
  const ok = /^\d{9}$/.test(v) || /^(proc:base:)?[A-Za-z0-9._-]{1,80}$/.test(v);
  const submit = (e) => {
    e.preventDefault();
    if (/^\d{9}$/.test(v)) go("e", v);
    else if (ok) go("p", unitOf(v));
  };
  return (
    <form onSubmit={submit}>
      <InputGroup large leftIcon="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="NIF da entidade ou número do procedimento"
        rightElement={<Button intent="primary" text="Procurar" type="submit" disabled={!ok} />} />
    </form>
  );
}
