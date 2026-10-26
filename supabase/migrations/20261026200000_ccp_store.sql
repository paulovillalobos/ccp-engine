-- D48: the data/ store at scale. Each table keeps the whole store object (doc) keyed by (id, revision), plus the columns
-- a query needs. Rows are never updated or deleted: a change is a new revision. RLS on, no policy: nothing is readable
-- through the Data API until a read-only policy is written for the interface.

create schema if not exists ccp;

create table ccp.raw (
  id text not null, revision int not null, recorded_at timestamptz not null,
  source text, sha256 text, url text, fetched_at timestamptz,
  doc jsonb not null, primary key (id, revision));

create table ccp.adaptador (
  id text not null, revision int not null, recorded_at timestamptz not null,
  source text, version int, state text,
  doc jsonb not null, primary key (id, revision));

create table ccp.unidade (
  id text not null, revision int not null, recorded_at timestamptz not null,
  kind text not null, parent text,
  doc jsonb not null, primary key (id, revision));
create index on ccp.unidade (parent);

create table ccp.facto (
  id text not null, revision int not null, recorded_at timestamptz not null,
  unit text not null, field text not null, value jsonb, valid_at date, known_at timestamptz not null,
  adapter text, raw text,
  doc jsonb not null, primary key (id, revision));
create index on ccp.facto (unit);
create index on ccp.facto (field, valid_at);

create table ccp.entidade (
  id text not null, revision int not null, recorded_at timestamptz not null,
  nif text, name text, country text, type text,
  doc jsonb not null, primary key (id, revision));
create index on ccp.entidade (nif);

create table ccp.alias (
  id text not null, revision int not null, recorded_at timestamptz not null,
  link text, raw text, name_as_appears text,
  doc jsonb not null, primary key (id, revision));

create table ccp.link (
  id text not null, revision int not null, recorded_at timestamptz not null,
  from_id text not null, to_id text not null, method text, state text,
  doc jsonb not null, primary key (id, revision));
create index on ccp.link (to_id);

create table ccp.documento (
  id text not null, revision int not null, recorded_at timestamptz not null,
  doc jsonb not null, primary key (id, revision));

create table ccp.conflito (
  id text not null, revision int not null, recorded_at timestamptz not null,
  unit text, field text,
  doc jsonb not null, primary key (id, revision));

create table ccp.afirmacao (
  id text not null, revision int not null, recorded_at timestamptz not null,
  unit text,
  doc jsonb not null, primary key (id, revision));

create table ccp.veredicto (
  id text not null, revision int not null, recorded_at timestamptz not null,
  unit text not null, rule text not null, result text not null, valid_at date, known_at timestamptz,
  doc jsonb not null, primary key (id, revision));
create index on ccp.veredicto (unit);
create index on ccp.veredicto (rule, result);

-- a read-only copy of rules/ (git stays the source of truth), for the interface
create table ccp.regra (
  id text not null, revision int not null, recorded_at timestamptz not null,
  type text, state text, valid_from date, valid_to date,
  doc jsonb not null, primary key (id, revision));

create or replace function ccp.refuse_change() returns trigger language plpgsql as $$
begin
  raise exception 'ccp.%: rows are never updated or deleted; write a new revision (D48)', tg_table_name;
end $$;

do $$
declare t text;
begin
  foreach t in array array['raw','adaptador','unidade','facto','entidade','alias','link','documento','conflito','afirmacao','veredicto','regra'] loop
    execute format('create trigger %I_append_only before update or delete on ccp.%I for each row execute function ccp.refuse_change()', t, t);
    execute format('alter table ccp.%I enable row level security', t);
  end loop;
end $$;

revoke all on schema ccp from anon, authenticated;
