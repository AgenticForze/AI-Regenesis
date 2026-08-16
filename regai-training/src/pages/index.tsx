import React from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import AltitudeGauge from '@site/src/components/AltitudeGauge';
import LearningPathCard from '@site/src/components/LearningPathCard';
import PrincipleCard from '@site/src/components/PrincipleCard';
import styles from './index.module.css';

const STATS = [
  {value: '19', label: 'Phases, FL00 → FL18'},
  {value: '165+', label: 'Chapters planned'},
  {value: '12', label: 'Use cases per concept'},
  {value: '3', label: 'Industries: Finance, Health, Telco'},
];

const PRINCIPLES = [
  {
    number: '01',
    name: 'Dual-Altitude Explanation',
    description: 'A plain-language pass and a rigorous deep-dive pass for every concept — read only what your role needs.',
  },
  {
    number: '02',
    name: 'Comparative Framing',
    description: "Every concept sits next to the two or three things people confuse it with, and a straight answer on which to use when.",
  },
  {
    number: '03',
    name: 'Domain-Grounded',
    description: 'Four worked use cases apiece in Finance, Healthcare, and Telecom — never toy examples.',
  },
  {
    number: '04',
    name: 'Architecture-First',
    description: 'Anything with moving parts gets a labeled reference architecture diagram, not just prose.',
  },
];

export default function Home(): JSX.Element {
  return (
    <Layout
      title="AI Foundations to Advanced Agentic AI"
      description="A GitHub-hosted knowledge base teaching AI from first principles to advanced Agentic AI, grounded in Finance, Healthcare, and Telecom use cases."
    >
      <header className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.eyebrow}>Nineteen phases · FL00 &rarr; FL18</p>
          <Heading as="h1" className={styles.title}>
            Every concept, two altitudes.
          </Heading>
          <p className={styles.subtitle}>
            RegAITraining teaches AI from first principles through advanced Agentic AI —
            a plain-language pass and a rigorous deep-dive pass for every concept, grounded
            in real Financial Services, Healthcare, and Telecom use cases instead of toy examples.
          </p>
          <div className={styles.heroCtas}>
            <a className={styles.ctaPrimary} href="/docs/orientation/0-1-welcome">
              Start Reading &rarr;
            </a>
            <a className={styles.ctaSecondary} href="/docs/orientation/0-3-ai-roles-in-the-market">
              Find Your Role
            </a>
          </div>
          <AltitudeGauge />
        </div>
      </header>

      <section className={styles.statsBar}>
        <div className={styles.statsInner}>
          {STATS.map((s) => (
            <div key={s.label} className={styles.stat}>
              <span className={styles.statValue}>{s.value}</span>
              <span className={styles.statLabel}>{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      <main className={styles.main}>
        <section className={styles.paths}>
          <p className={styles.sectionEyebrow}>Choose your path</p>
          <div className={styles.pathGrid}>
            <LearningPathCard
              name="Foundations Track"
              audience="New to AI"
              route="Phase 0 → 1 → 2 → 3 → 4 → 5 → (RAG or Agents)"
              href="/docs/orientation/0-2-learning-paths-personas"
              accent="teal"
            />
            <LearningPathCard
              name="Practitioner / Builder Track"
              audience="Some ML/GenAI experience"
              route="Phase 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 (Phase 13 optional)"
              href="/docs/orientation/0-2-learning-paths-personas"
              accent="amber"
            />
            <LearningPathCard
              name="Advanced / Architect Track"
              audience="Already building agentic systems"
              route="Phase 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17"
              href="/docs/orientation/0-2-learning-paths-personas"
              accent="ink"
            />
          </div>
        </section>

        <section className={styles.roles}>
          <div className={styles.rolesCard}>
            <p className={styles.sectionEyebrow}>New in v5</p>
            <Heading as="h2">Not sure which path fits your job?</Heading>
            <p>
              The AI Roles in the Market chapter maps all fifteen major AI/agentic job roles —
              from Data Scientist to Multi-Agent Systems Architect to AI Governance Specialist —
              to the exact phases and chapters that role needs, plus the certifications worth
              pursuing for it.
            </p>
            <a className={styles.rolesLink} href="/docs/orientation/0-3-ai-roles-in-the-market">
              Open the AI Roles Map &rarr;
            </a>
          </div>
        </section>

        <section className={styles.principlesSection}>
          <p className={styles.sectionEyebrow}>Why it's built this way</p>
          <div className={styles.principlesGrid}>
            {PRINCIPLES.map((p) => (
              <PrincipleCard key={p.number} {...p} />
            ))}
          </div>
          <div className={styles.principlesFooter}>
            <a href="/about">Read the full design philosophy &rarr;</a>
          </div>
        </section>

        <section className={styles.growth}>
          <div className={styles.growthCard}>
            <p className={styles.sectionEyebrow}>Continuously growing</p>
            <Heading as="h2">Content ships incrementally, not in one big launch</Heading>
            <p>
              Every merge to <code>main</code> deploys automatically. See what's shipped and
              what's next on the <a href="/roadmap">Roadmap</a>, or what changed and why in each
              curriculum revision on the <a href="/changelog">Changelog</a>.
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}

