import React from 'react';
import Layout from '@theme/Layout';
import PageHeader from '@site/src/components/PageHeader';
import PrincipleCard from '@site/src/components/PrincipleCard';
import styles from './about.module.css';

const PRINCIPLES = [
  {
    number: '01',
    name: 'Dual-Altitude Explanation',
    description:
      "Every concept chapter opens with an intuition-first explanation a non-specialist can follow, then descends into the mechanics — math where it matters, architecture diagrams, code where useful — for readers who need to build or defend the concept technically.",
  },
  {
    number: '02',
    name: 'Comparative Framing',
    description:
      "Concepts are rarely taught in isolation. Each chapter places its subject next to the two or three things people confuse it with (RAG vs. fine-tuning, agent vs. workflow, LangGraph vs. CrewAI) and gives a straight answer on when to use which.",
  },
  {
    number: '03',
    name: 'Domain-Grounded, Not Toy-Grounded',
    description:
      'Every applicable chapter carries four worked use cases apiece in Financial Services, Healthcare, and Telecom — twelve per concept — so a learner in any of those industries can see the concept solving a problem that looks like their job.',
  },
  {
    number: '04',
    name: 'Architecture-First for Anything Systems-Level',
    description:
      'Wherever a concept has moving parts — RAG pipelines, agent loops, multi-agent topologies, enterprise agent platforms — the chapter includes a labeled reference architecture diagram, not just prose.',
  },
];

export default function About(): JSX.Element {
  return (
    <Layout
      title="About"
      description="Why RegAITraining is built the way it is — design philosophy, content standard, and how the site stays honest as it grows."
    >
      <div className={styles.container}>
        <PageHeader
          eyebrow="Design Philosophy"
          title="Why this site is built the way it is"
          subtitle="Four principles run through all nineteen phases. They're not decoration — every review pass (v3, v4, v5) exists to close gaps against these four things, not to add pages for their own sake."
        />

        <div className={styles.grid}>
          {PRINCIPLES.map((p) => (
            <PrincipleCard key={p.number} {...p} />
          ))}
        </div>

        <section className={styles.section}>
          <h2>The chapter contract</h2>
          <p>
            To keep quality consistent as dozens of contributors add chapters over time, every
            concept-level chapter follows the same seven-section template — TL;DR, High-Level
            Explanation, Deep-Dive Explanation, Comparison &amp; Related Concepts, Reference
            Architecture, Industry Use Cases, and Check Your Understanding. A chapter isn't done
            until all seven are filled in. Two phases (9 and 14) intentionally use a lighter
            four-section landscape template instead — see{' '}
            <a href="/docs/orientation/0-6-content-standard-explained">
              0.6 The Content Standard, Explained
            </a>{' '}
            for the full breakdown of why.
          </p>
        </section>

        <section className={styles.section}>
          <h2>How the site stays honest as it grows</h2>
          <p>
            This is a continuously growing knowledge base, not a fixed course — new chapters start
            from a GitHub issue, get written against the shared template, and go live the moment
            they merge. There's no "big launch" being held back. Periodic judge-LLM review passes
            (the process behind v3, v4, and v5 of the curriculum) are run quarterly to catch new
            production patterns before they become content gaps — see the{' '}
            <a href="/changelog">Changelog</a> for what each pass found and fixed, and the{' '}
            <a href="/roadmap">Roadmap</a> for what ships next.
          </p>
        </section>

        <section className={styles.section}>
          <h2>Built with</h2>
          <p>
            Docusaurus 3 (React + MDX) for versioned docs and MDX-embeddable components; Mermaid
            for architecture diagrams authored as version-controlled text; GitHub Actions for
            build/deploy on every merge to <code>main</code>. See{' '}
            <a href="https://github.com/regai-training/regai-training">the GitHub repo</a> for the
            full stack and contribution workflow.
          </p>
        </section>
      </div>
    </Layout>
  );
}
