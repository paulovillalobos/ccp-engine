-- D55: each source's daily run (db/daily.py) leaves one row, so the health of a source is a query. Append-only as the rest.

create table ccp.ingesta (
  run_id text not null, source text not null, started_at timestamptz not null, finished_at timestamptz not null,
  status text not null check (status in ('ok', 'nothing_new', 'error')),
  detail jsonb not null default '{}',
  primary key (run_id, source));

create trigger ingesta_append_only before update or delete on ccp.ingesta for each row execute function ccp.refuse_change();
alter table ccp.ingesta enable row level security;

-- per source: the last run, its status and detail, and the last run that did not fail
create view ccp.saude as
select source, max(started_at) as last_run, max(started_at) filter (where status <> 'error') as last_ok,
  (array_agg(status order by started_at desc))[1] as last_status, (array_agg(detail order by started_at desc))[1] as last_detail
from ccp.ingesta group by source;

revoke all on all tables in schema ccp from anon, authenticated;
