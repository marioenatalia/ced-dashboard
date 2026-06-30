-- ╔══════════════════════════════════════════════════════════════╗
-- ║  CED Dashboard · Foglio Pagamenti · schema Supabase           ║
-- ║  Tabelle prefissate ced_ per convivere in un progetto esistente║
-- ║  Esegui nel SQL Editor del progetto Supabase scelto (una volta)║
-- ╚══════════════════════════════════════════════════════════════╝

create table if not exists ced_clienti (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  categoria   text not null default 'focus',   -- focus | altri | ragazzi | bilancio | nuovi
  cadenza     text,
  tariffa     text,
  stato       text not null default 'attivo',    -- attivo | uscito | inattivo
  arretrati   numeric not null default 0,
  ordine      int default 0,
  creato_il   timestamptz default now()
);

create table if not exists ced_proforme (
  id            uuid primary key default gen_random_uuid(),
  cliente_id    uuid references ced_clienti(id) on delete cascade,
  anno          int not null default 2026,
  periodo       text not null,    -- 'I','II','III','IV' | 'GEN'..'DIC' | 'ANNO' | 'I_SEM','II_SEM' | 'BILANCIO'
  importo       numeric not null default 0,
  pagato        boolean not null default false,
  data_pagamento date,
  data_emissione date,
  pdf_path      text,
  note          text,
  creato_il     timestamptz default now(),
  unique (cliente_id, anno, periodo)
);

create index if not exists idx_ced_proforme_cliente on ced_proforme(cliente_id);
create index if not exists idx_ced_proforme_anno on ced_proforme(anno);

alter table ced_clienti  enable row level security;
alter table ced_proforme enable row level security;
create policy "anon full ced_clienti"  on ced_clienti  for all using (true) with check (true);
create policy "anon full ced_proforme" on ced_proforme for all using (true) with check (true);
