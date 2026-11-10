-- D93: what the BASE portal shows of each contract, kept as BASE publishes it (db/base_detail.py): the procedure page
-- shows it next to the verdicts. Read from the same yearly dumps the facts come from (raw: the dump's raw id and sha256),
-- never interpreted: no field here is an input of any rule. One row per idcontrato; a changed record replaces the row.

create table ccp.base_contrato (
  id bigint primary key,            -- idcontrato
  ano smallint not null,            -- the dump's year
  raw text not null,                -- raw:base-contratos:<kind>:<id>, the dump the fields were read from
  doc bytea not null,               -- the record's portal fields as zlib-compressed JSON (names as in the dump, empty
                                    -- ones left out), against the fixed dictionary db/base_detail.zdict (sha256 d2b4c8f8…5e46)
  recorded_at timestamptz not null default now());

revoke all on ccp.base_contrato from anon, authenticated;
