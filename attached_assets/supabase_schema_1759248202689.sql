-- Minimal ODYC schema (run in Supabase SQL editor)
create extension if not exists pgcrypto;

create table if not exists pathways (
  id bigserial primary key,
  title text not null,
  ksas text[] default '{}',
  milestones text[] default '{}',
  wage_bands text[] default '{}',
  created_at timestamptz default now()
);

create table if not exists project_cards (
  id bigserial primary key,
  pathway_id bigint references pathways(id) on delete cascade,
  title text not null,
  duration_hours int,
  objective text,
  prereqs text[] default '{}',
  steps text[] default '{}',
  artifact_spec jsonb default '{}'::jsonb,
  capacity_month int default 0,
  created_at timestamptz default now()
);

create table if not exists rubrics (
  id bigserial primary key,
  pathway_id bigint references pathways(id) on delete cascade,
  competency text not null,
  novice text,
  developing text,
  proficient text,
  created_at timestamptz default now()
);

-- Simple placeholder view for Transcript (replace with real joins)
drop view if exists artifacts_view;
create view artifacts_view as
select
  gen_random_uuid() as id,
  null::uuid as student_id,
  pc.title as project_title,
  ''::text as badges,
  false as signed_off
from project_cards pc
limit 5;
