-- D49, second step: after db/pg.py move-d48 copied every D48 row of facto, raw and unidade into the compact tables and
-- compared each object (181 628 objects, 0 missing, 0 different; BUILD-LOG), the D48 tables go and the views take
-- their names, so a reader asks ccp.facto, ccp.raw and ccp.unidade as before and gets the same doc.

drop table ccp.facto, ccp.raw, ccp.unidade;
alter view ccp.facto_v rename to facto;
alter view ccp.raw_v rename to raw;
alter view ccp.unidade_v rename to unidade;
revoke all on all tables in schema ccp from anon, authenticated;
