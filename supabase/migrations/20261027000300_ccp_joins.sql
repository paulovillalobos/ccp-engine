-- D56: the joins, as views over the latest revision of the facts and units (nothing copied, nothing merged). An exact join
-- names the identifier it rests on; a TED match without a shared identifier is a candidate with its method, never a
-- merge (ccp.ted_candidato, refreshed by db/joins.py).

create function ccp.n(t text) returns int language sql stable as $$ select no from ccp.nome where txt = t $$;

-- the latest revision of each fact and unit
create view ccp.facto_atual as
select f.* from ccp.facto_c f
where f.revision = (select max(x.revision) from ccp.facto_c x where x.unit = f.unit and x.field = f.field and x.src = f.src);

create view ccp.unidade_atual as
select u.* from ccp.unidade_c u where u.revision = (select max(x.revision) from ccp.unidade_c x where x.id = u.id);

-- procedure <-> contract: a contract's parent is the anúncio procedure whose key (nAnuncio + IdIncm) it names, else the
-- procedure idproc-<idprocedimento> gathered from BASE contratos
create view ccp.contrato_proc as
select i.txt as contrato, p.txt as proc,
  case when p.txt like 'proc:base:idproc-%' then 'idprocedimento' else 'nAnuncio+IdIncm' end as metodo
from ccp.unidade_atual u join ccp.nome i on i.no = u.id join ccp.nome p on p.no = u.parent
where u.kind = ccp.n('contrato');

-- procedure <-> DR notice: the documento the DR adapter read for the procedure (key nAnuncio + IdIncm, E1b)
create view ccp.proc_dr as
select distinct u.txt as proc, f.rest -> 'origin' ->> 'documento' as documento
from ccp.facto_c f join ccp.nome u on u.no = f.unit join ccp.nome a on a.no = f.adapter
where a.txt like 'adaptador:dr-anuncios@%' and f.rest -> 'origin' ? 'documento';

-- the entity graph by NIF: every adjudicante and adjudicatário a record names, with the unit, the raw and the date
create view ccp.entidade_papel as
select n.nif, fl.txt as papel, u.txt as unit, r.txt as raw, f.valid_at, a.txt as adapter
from ccp.facto_atual f
join ccp.nome fl on fl.no = f.field join ccp.nome u on u.no = f.unit join ccp.nome a on a.no = f.adapter
left join ccp.nome r on r.no = f.oraw
cross join lateral (
  select f.value #>> '{}' as nif where jsonb_typeof(f.value) = 'string'
  union all select e from jsonb_array_elements_text(case when jsonb_typeof(f.value) = 'array' then f.value else '[]' end) e) n
where f.field in (ccp.n('adjudicante'), ccp.n('adjudicatario'));

-- BASE procedure <-> TED competition notice, when no identifier is shared: same buyer NIF, same contract type, the TED
-- notice sent to the Publications Office in the 10 days before the DR publication up to 2 days after it. alternativas_*
-- count the other matches: a candidate is unique only when both are 1.
create materialized view ccp.ted_candidato as
with b as (
  select f.unit, f.value #>> '{}' as nif, f.valid_at as d, t.value #>> '{}' as tipo
  from ccp.facto_atual f join ccp.facto_atual t on t.unit = f.unit and t.field = ccp.n('tipo_contrato') and t.src = f.src
  where f.field = ccp.n('adjudicante') and f.src = ccp.n('base-anuncios')),
t as (
  select f.unit, f.value #>> '{}' as nif, (e.value #>> '{}')::date as d, t.value #>> '{}' as tipo
  from ccp.facto_atual f
  join ccp.facto_atual t on t.unit = f.unit and t.field = ccp.n('tipo_contrato') and t.src = f.src
  join ccp.facto_atual e on e.unit = f.unit and e.field = ccp.n('data_envio_joue') and e.src = f.src
  where f.field = ccp.n('adjudicante') and f.src = ccp.n('ted')),
m as (
  select b.unit as base_unit, t.unit as ted_unit, b.d - t.d as dias
  from b join t on t.nif = b.nif and t.tipo = b.tipo and t.d between b.d - 10 and b.d + 2)
select bu.txt as base_proc, tu.txt as ted_proc, m.dias, 'nif+tipo_contrato+janela_envio' as metodo,
  count(*) over (partition by m.base_unit) as alternativas_base, count(*) over (partition by m.ted_unit) as alternativas_ted
from m join ccp.nome bu on bu.no = m.base_unit join ccp.nome tu on tu.no = m.ted_unit;

revoke all on all tables in schema ccp from anon, authenticated;
