-- D88: an engine run (corrida) and the verdicts it gave. Verdicts are append-only (D48): a later run that no longer
-- judges a procedure with a rule cannot withdraw the earlier verdict, so readers take the verdicts of the latest run.
create table ccp.corrida (
  id text primary key, at timestamptz not null, doc jsonb not null);
create table ccp.corrida_veredicto (
  corrida text not null, veredicto text not null, revision int not null, primary key (corrida, veredicto, revision));
create index on ccp.corrida_veredicto (veredicto);
create trigger corrida_append_only before update or delete on ccp.corrida for each row execute function ccp.refuse_change();
create trigger corrida_veredicto_append_only before update or delete on ccp.corrida_veredicto for each row execute function ccp.refuse_change();
alter table ccp.corrida enable row level security;
alter table ccp.corrida_veredicto enable row level security;
revoke all on ccp.corrida, ccp.corrida_veredicto from anon, authenticated;

-- the verdicts of the latest run
create view ccp.veredicto_atual as
select v.* from ccp.veredicto v
join ccp.corrida_veredicto cv on cv.veredicto = v.id and cv.revision = v.revision
where cv.corrida = (select id from ccp.corrida order by at desc limit 1);
revoke all on ccp.veredicto_atual from anon, authenticated;
