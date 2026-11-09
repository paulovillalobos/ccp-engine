-- D90: each run records the adjudicante of the procedure it gave a verdict on, so the API finds one entity's verdicts by
-- an index instead of a scan of every adjudicante fact (11–20 s).
alter table ccp.corrida_veredicto add column adjudicante text;
create index on ccp.corrida_veredicto (corrida, adjudicante);
create or replace view ccp.veredicto_atual as
select v.*, cv.adjudicante from ccp.veredicto v
join ccp.corrida_veredicto cv on cv.veredicto = v.id and cv.revision = v.revision
where cv.corrida = (select id from ccp.corrida order by at desc limit 1);
revoke all on ccp.veredicto_atual from anon, authenticated;
