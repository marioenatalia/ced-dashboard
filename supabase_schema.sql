-- ╔══════════════════════════════════════════════════════════════╗
-- ║  CED Dashboard · Foglio Pagamenti · schema Supabase           ║
-- ║  Esegui questo SQL nel SQL Editor di Supabase (una volta)      ║
-- ╚══════════════════════════════════════════════════════════════╝

-- Clienti (replica le righe dei fogli FOCUS/ALTRI/RAGAZZI/BILANCIO)
create table if not exists clienti (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  categoria   text not null default 'focus',   -- focus | altri | ragazzi | bilancio
  cadenza     text,                              -- trimestrale | mensile | annuale | semestrale | forfettino
  tariffa     text,                              -- nota tariffaria (es. "660+iva forfettino")
  stato       text not null default 'attivo',    -- attivo | uscito | inattivo
  arretrati   numeric not null default 0,        -- arretrati al 31/12 anno prec.
  ordine      int default 0,
  creato_il   timestamptz default now()
);

-- Proforma: una riga per cliente × periodo (il "cella" della matrice Excel)
create table if not exists proforme (
  id            uuid primary key default gen_random_uuid(),
  cliente_id    uuid references clienti(id) on delete cascade,
  anno          int not null default 2026,
  periodo       text not null,    -- 'I','II','III','IV' | 'GEN'..'DIC' | 'ANNO' | 'BILANCIO'
  importo       numeric not null default 0,
  pagato        boolean not null default false,
  data_pagamento date,
  data_emissione date,
  pdf_path      text,             -- collegamento al PDF su Yandex (opzionale)
  note          text,
  creato_il     timestamptz default now(),
  unique (cliente_id, anno, periodo)
);

create index if not exists idx_proforme_cliente on proforme(cliente_id);
create index if not exists idx_proforme_anno on proforme(anno);

-- RLS: strumento interno con login proprio nell'app -> politica permissiva per la anon key.
alter table clienti  enable row level security;
alter table proforme enable row level security;
create policy "anon full clienti"  on clienti  for all using (true) with check (true);
create policy "anon full proforme" on proforme for all using (true) with check (true);

-- Vista comoda: totale da incassare per cliente (periodi non pagati + arretrati)
create or replace view v_da_incassare as
select c.id, c.nome, c.categoria, c.stato, c.arretrati,
       coalesce(sum(case when not p.pagato then p.importo else 0 end),0) + c.arretrati as da_incassare,
       coalesce(sum(case when p.pagato then p.importo else 0 end),0) as incassato
from clienti c
left join proforme p on p.cliente_id = c.id
group by c.id;
