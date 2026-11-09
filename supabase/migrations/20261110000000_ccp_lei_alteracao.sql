-- D92: the law watch. Every day the cloud reads the consolidated CCP on the Diário da República and compares each article
-- with the text the repository holds in force; an article that differs is pending here until the readers (AMALIA and
-- Reader B, on the person's Mac) have read it and the repository holds the new text. While an article is pending, the engine
-- gives no verdict under a rule that cites it (db/run_engine.load_rules). A row is closed, not deleted, when the article
-- no longer differs.

create table ccp.lei_alteracao (
  passagem text not null,
  detetada_em timestamptz not null default now(),
  pagina_sha256 text,
  fechada_em timestamptz,
  primary key (passagem, detetada_em));
create index on ccp.lei_alteracao (passagem) where fechada_em is null;

create view ccp.lei_pendente as
select passagem, min(detetada_em) as desde from ccp.lei_alteracao where fechada_em is null group by passagem;

-- the law watch's own runs, read failures included (a failed read is never "no change")
create table ccp.lei_vigia (
  em timestamptz primary key default now(),
  ok boolean not null,
  artigos int,
  diferentes text[],
  novas text[],
  erro text);

revoke all on ccp.lei_alteracao, ccp.lei_pendente, ccp.lei_vigia from anon, authenticated;
