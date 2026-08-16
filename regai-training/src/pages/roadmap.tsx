import React from 'react';
import Layout from '@theme/Layout';
import PageHeader from '@site/src/components/PageHeader';
import styles from './roadmap.module.css';

type Status = 'shipped' | 'in-progress' | 'planned';

interface Milestone {
  id: string;
  scope: string;
  deliverable: string;
  status: Status;
}

const MILESTONES: Milestone[] = [
  {
    id: 'M0',
    scope: 'Repo & site scaffold',
    deliverable:
      "Docusaurus site live with Phase 0 content (incl. the AI Roles map, 0.3), all 19 phase shells, both chapter templates, CI/CD, and the site's design system.",
    status: 'shipped',
  },
  {
    id: 'M1',
    scope: 'Phases 1–2',
    deliverable: 'AI/ML + Deep Learning foundations fully written to Content Standard.',
    status: 'in-progress',
  },
  {id: 'M2', scope: 'Phases 3–4', deliverable: 'NLP/LLM + Generative AI foundations.', status: 'planned'},
  {
    id: 'M3',
    scope: 'Phase 5',
    deliverable: 'Prompting, incl. structured-output/constrained-decoding chapter (5.4).',
    status: 'planned',
  },
  {
    id: 'M4',
    scope: 'Phase 6',
    deliverable: 'RAG & Knowledge Systems, incl. semantic caching (6.7) and OKF (6.10).',
    status: 'planned',
  },
  {id: 'M5', scope: 'Phase 7', deliverable: 'Fine-Tuning & Alignment.', status: 'planned'},
  {
    id: 'M6',
    scope: 'Phase 8',
    deliverable:
      'Agent Foundations, incl. context-engineering (8.6) and Conversational & Agent UX Design (8.9).',
    status: 'planned',
  },
  {
    id: 'M7',
    scope: 'Phases 9–12',
    deliverable:
      'Framework landscape survey, Architectures (incl. hybrid orchestration 10.4, sandboxing 10.5), Multi-Agent, deep framework/protocol dives — the flagship agentic core.',
    status: 'planned',
  },
  {
    id: 'M8',
    scope: 'Phase 13',
    deliverable:
      'Advanced Infrastructure Track (Build-Your-Own-LLM/SLM), incl. synthetic data (13.7) and inference optimization (13.10).',
    status: 'planned',
  },
  {id: 'M9', scope: 'Phase 14', deliverable: 'Hyperscaler platform foundations.', status: 'planned'},
  {
    id: 'M10',
    scope: 'Phase 15',
    deliverable:
      'Enterprise AgentOps/Governance, incl. expanded evaluation (15.2), identity/OAuth (15.5), gateway/router (15.6), and AI Product Strategy (15.11).',
    status: 'planned',
  },
  {
    id: 'M11',
    scope: 'Phase 16',
    deliverable: 'Finance/Health/Telco domain deep dives, incl. quant backtesting and TM Forum/network-slicing use cases.',
    status: 'planned',
  },
  {
    id: 'M12',
    scope: 'Phases 17–18',
    deliverable: 'Frontier topics + Capstones; open contribution process goes live.',
    status: 'planned',
  },
];

const STATUS_LABEL: Record<Status, string> = {
  shipped: 'Shipped',
  'in-progress': 'In progress',
  planned: 'Planned',
};

export default function Roadmap(): JSX.Element {
  return (
    <Layout
      title="Roadmap"
      description="Build milestones for the RegAITraining curriculum, M0 through M12."
    >
      <div className={styles.container}>
        <PageHeader
          eyebrow="Build Roadmap"
          title="Thirteen milestones, shipping incrementally"
          subtitle="The site is public and growing from M0 onward — not held back for a big launch. Each milestone ships as a deployed increment."
        />

        <ol className={styles.timeline}>
          {MILESTONES.map((m) => (
            <li key={m.id} className={styles.item}>
              <div className={styles.marker}>
                <span className={`${styles.dot} ${styles[m.status]}`} />
                {m.id !== 'M12' && <span className={styles.line} />}
              </div>
              <div className={styles.content}>
                <div className={styles.rowHead}>
                  <span className={styles.id}>{m.id}</span>
                  <span className={styles.scope}>{m.scope}</span>
                  <span className={`${styles.badge} ${styles[`badge-${m.status}`]}`}>
                    {STATUS_LABEL[m.status]}
                  </span>
                </div>
                <p className={styles.deliverable}>{m.deliverable}</p>
              </div>
            </li>
          ))}
        </ol>

        <p className={styles.note}>
          Note: M6/M7 are sequential and uninterrupted (no infrastructure detour) — Phase 13 was
          deliberately moved after the core agentic phases so the main Practitioner flow
          (Prompting → RAG → Fine-Tuning → Agents) stays unbroken. See{' '}
          <a href="/changelog">the changelog</a> for the reasoning.
        </p>
      </div>
    </Layout>
  );
}
