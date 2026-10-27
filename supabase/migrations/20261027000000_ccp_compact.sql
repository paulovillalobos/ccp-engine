-- D55: the three big tables in a compact layout, so the 2018–2026 history fits the Micro instance (8 GB disk). The
-- object stays the unit of storage: each row is one (id, revision) and the views below rebuild its doc exactly
-- (db/pg.py roundtrip compares every object, canonical JSON). What changes is how a row spells it: every repeated
-- string (unit, raw and field ids, adapters, URLs, standard request objects) is a number in ccp.nome; a fact's id is
-- derived from (unit, field, source), as every adapter writes it; anything a column cannot say exactly stays in rest.

create table ccp.nome (no int generated always as identity primary key, txt text not null unique);

create table ccp.facto_c (
  unit int not null, field int not null, src int not null, revision smallint not null,
  recorded_at timestamptz not null, adapter int, value jsonb, valid_at date, known_at timestamptz,
  oraw int, ofield int, rest jsonb,
  primary key (unit, field, src, revision));
create index on ccp.facto_c (field, valid_at);

create table ccp.raw_c (
  id int not null, revision smallint not null, recorded_at timestamptz not null,
  source int, kind int, source_id text, sha256 bytea, media_type int, encoding int, url int, captured_at timestamptz,
  request int, rest jsonb,
  primary key (id, revision));

create table ccp.unidade_c (
  id int not null, revision smallint not null, recorded_at timestamptz not null,
  kind int, parent int, raw int[], rest jsonb,
  primary key (id, revision));
create index on ccp.unidade_c (parent);

create function ccp.utc(t timestamptz) returns text language sql immutable as
  $$ select to_char(t at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"') $$;

create view ccp.facto_v as
select x.id, c.revision, c.recorded_at, u.txt as unit, f.txt as field, c.value, c.valid_at, c.known_at, a.txt as adapter, r.txt as raw,
  jsonb_build_object('id', x.id, 'revision', c.revision, 'recorded_at', ccp.utc(c.recorded_at), 'unit', u.txt, 'field', f.txt)
  || case when c.value is null then '{}' else jsonb_build_object('value', c.value) end
  || case when c.valid_at is null then '{}' else jsonb_build_object('valid_at', to_char(c.valid_at, 'YYYY-MM-DD')) end
  || case when c.known_at is null then '{}' else jsonb_build_object('known_at', ccp.utc(c.known_at)) end
  || case when a.txt is null then '{}' else jsonb_build_object('adapter', a.txt) end
  || case when r.txt is null then '{}' else jsonb_build_object('origin', jsonb_build_object('raw', r.txt, 'field', o.txt)) end
  || coalesce(c.rest, '{}') as doc
from ccp.facto_c c
join ccp.nome u on u.no = c.unit join ccp.nome f on f.no = c.field join ccp.nome s on s.no = c.src
left join ccp.nome a on a.no = c.adapter left join ccp.nome r on r.no = c.oraw left join ccp.nome o on o.no = c.ofield
cross join lateral (select 'facto:' || replace(u.txt, ':', '-') || ':' || f.txt || ':' || s.txt as id) x;

create view ccp.raw_v as
select i.txt as id, c.revision, c.recorded_at, so.txt as source, encode(c.sha256, 'hex') as sha256, ur.txt as url, c.captured_at,
  jsonb_build_object('id', i.txt, 'revision', c.revision, 'recorded_at', ccp.utc(c.recorded_at))
  || case when so.txt is null then '{}' else jsonb_build_object('source', so.txt) end
  || case when k.txt is null then '{}' else jsonb_build_object('kind', k.txt) end
  || case when c.source_id is null then '{}' else jsonb_build_object('source_id', c.source_id) end
  || case when c.sha256 is null then '{}' else jsonb_build_object('sha256', encode(c.sha256, 'hex'), 'bytes', 'raw_bytes/' || encode(c.sha256, 'hex')) end
  || case when m.txt is null then '{}' else jsonb_build_object('media_type', m.txt) end
  || case when e.txt is null then '{}' else jsonb_build_object('encoding', e.txt) end
  || case when ur.txt is null then '{}' else jsonb_build_object('url', ur.txt) end
  || case when c.captured_at is null then '{}' else jsonb_build_object('captured_at', ccp.utc(c.captured_at)) end
  || case when q.txt is null then '{}' else jsonb_build_object('request', q.txt::jsonb) end
  || coalesce(c.rest, '{}') as doc
from ccp.raw_c c
join ccp.nome i on i.no = c.id
left join ccp.nome so on so.no = c.source left join ccp.nome k on k.no = c.kind left join ccp.nome m on m.no = c.media_type
left join ccp.nome e on e.no = c.encoding left join ccp.nome ur on ur.no = c.url left join ccp.nome q on q.no = c.request;

create view ccp.unidade_v as
select i.txt as id, c.revision, c.recorded_at, k.txt as kind, p.txt as parent,
  jsonb_build_object('id', i.txt, 'revision', c.revision, 'recorded_at', ccp.utc(c.recorded_at))
  || case when k.txt is null then '{}' else jsonb_build_object('kind', k.txt) end
  || case when c.parent is null then '{}' else jsonb_build_object('parent', p.txt) end
  || case when c.raw is null then '{}' else jsonb_build_object('raw',
       (select coalesce(jsonb_agg(n.txt order by t.ord), '[]') from unnest(c.raw) with ordinality t(no, ord) join ccp.nome n on n.no = t.no)) end
  || coalesce(c.rest, '{}') as doc
from ccp.unidade_c c
join ccp.nome i on i.no = c.id
left join ccp.nome k on k.no = c.kind left join ccp.nome p on p.no = c.parent;

do $$
declare t text;
begin
  foreach t in array array['nome', 'facto_c', 'raw_c', 'unidade_c'] loop
    execute format('create trigger %I_append_only before update or delete on ccp.%I for each row execute function ccp.refuse_change()', t, t);
    execute format('alter table ccp.%I enable row level security', t);
  end loop;
end $$;

revoke all on all tables in schema ccp from anon, authenticated;
