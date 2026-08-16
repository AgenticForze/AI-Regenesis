import React from 'react';
import Layout from '@theme/Layout';
import PageHeader from '@site/src/components/PageHeader';
import styles from './changelog.module.css';

interface Entry {
  version: string;
  date: string;
  title: string;
  points: string[];
}

const ENTRIES: Entry[] = [
  {
    version: 'v5',
    date: 'Aug 14, 2026',
    title: 'AI Roles chapter added',
    points: [
      'New Chapter 0.3, "AI Roles in the Market" — maps the ~15 major AI/agentic job roles to core curriculum paths and recommended certifications, added to Phase 0.',
      'The role-mapping exercise surfaced two genuine content gaps, closed with two new chapters: 8.9 Conversational & Agent UX Design (Agent Foundations) and 15.11 AI Product Strategy (Enterprise phase).',
      'A few other role-adjacent needs (deep data engineering, academic ML research methodology) were deliberately scoped out — see the AI Roles chapter for the reasoning.',
      'Certifications in the new role-mapping table were verified against current 2026 provider documentation rather than assumed from training knowledge.',
    ],
  },
  {
    version: 'v4',
    date: 'Aug 14, 2026',
    title: 'Second judge-LLM pass, targeted fixes (no renumbering)',
    points: [
      'Ch 15.2 expanded: Evals as CI/CD Quality Gates — flakiness management for non-deterministic trajectory tests, synthetic dataset sampling for CI, cost-capped regression testing.',
      'Ch 10.3 expanded: Agent State Versioning & In-Flight Migration for long-running persistent agent state.',
      'Ch 7.5 ↔ 13.7 cross-linked: Task-Specific Tool-Calling Distillation — training small, fast SLMs for high-frequency micro-agent steps.',
      'Phase flow reviewed and confirmed correct: no phases moved or renumbered in v4.',
    ],
  },
  {
    version: 'v3',
    date: 'Aug 14, 2026',
    title: 'Judge-LLM critique integrated',
    points: [
      'Moved "Building Your Own Language Models" from Phase 8 to Phase 13, relabeled an Advanced Infrastructure Track, so the main Practitioner flow (Prompting → RAG → Fine-Tuning → Agents) runs uninterrupted.',
      'Added 13 new chapters and expanded 4 existing ones across Phases 5, 6, 8, 10, 13, 15, and 16 — structured-output enforcement, hybrid orchestration, agent sandboxing, context engineering, semantic caching, synthetic data generation, inference optimization, LLM gateway/router patterns, multi-layered agent evaluation, agent identity/OAuth, and Telecom/Finance use-case gaps.',
      'Curriculum still runs Phase 0 through Phase 18 (chapter count grew from ~150 to ~165+ pages; phase count unchanged at 19).',
    ],
  },
];

export default function Changelog(): JSX.Element {
  return (
    <Layout title="Changelog" description="Curriculum revision history — v3, v4, and v5 review passes.">
      <div className={styles.container}>
        <PageHeader
          eyebrow="Changelog"
          title="How the curriculum has been revised"
          subtitle="Periodic judge-LLM review passes catch production-pattern gaps before they become blind spots. Each pass is logged here with what changed and why."
        />

        <div className={styles.list}>
          {ENTRIES.map((e) => (
            <article key={e.version} className={styles.entry}>
              <div className={styles.entryHead}>
                <span className={styles.version}>{e.version}</span>
                <h2 className={styles.title}>{e.title}</h2>
                <span className={styles.date}>{e.date}</span>
              </div>
              <ul className={styles.points}>
                {e.points.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>

        <p className={styles.note}>
          Full gap-to-resolution traceability tables for v3 and v5 live alongside the curriculum
          plan in the repo. See <a href="/roadmap">the Roadmap</a> for what ships next.
        </p>
      </div>
    </Layout>
  );
}
