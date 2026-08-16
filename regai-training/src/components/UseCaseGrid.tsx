import React, {useState} from 'react';
import styles from './UseCaseGrid.module.css';

export interface UseCase {
  title: string;
  problem: string;
  solution: string;
  risk: string;
}

interface UseCaseGridProps {
  finance: UseCase[];
  healthcare: UseCase[];
  telecom: UseCase[];
}

const DOMAINS: {key: keyof UseCaseGridProps; label: string; icon: string}[] = [
  {key: 'finance', label: 'Financial Services', icon: '\u25C8'},
  {key: 'healthcare', label: 'Healthcare', icon: '\u2724'},
  {key: 'telecom', label: 'Telecom', icon: '\u25C9'},
];

/**
 * Renders the Content Standard's mandatory 12 use cases (4 each for
 * Finance / Healthcare / Telecom) as a tabbed grid so a chapter page
 * doesn't turn into an unreadable wall of 12 stacked cards.
 */
export default function UseCaseGrid({finance, healthcare, telecom}: UseCaseGridProps): JSX.Element {
  const data: UseCaseGridProps = {finance, healthcare, telecom};
  const [active, setActive] = useState<keyof UseCaseGridProps>('finance');

  return (
    <div className={styles.wrapper}>
      <div className={styles.tabs} role="tablist" aria-label="Industry use cases">
        {DOMAINS.map((d) => (
          <button
            key={d.key}
            role="tab"
            aria-selected={active === d.key}
            className={active === d.key ? styles.tabActive : styles.tab}
            onClick={() => setActive(d.key)}
          >
            <span aria-hidden="true">{d.icon}</span> {d.label}
            <span className={styles.count}>{data[d.key]?.length ?? 0}</span>
          </button>
        ))}
      </div>
      <div className={styles.grid}>
        {(data[active] ?? []).map((uc, i) => (
          <article className={styles.card} key={i}>
            <h4 className={styles.cardTitle}>{uc.title}</h4>
            <p className={styles.label}>Business problem</p>
            <p>{uc.problem}</p>
            <p className={styles.label}>Solution sketch</p>
            <p>{uc.solution}</p>
            <p className={styles.riskLabel}>Watch for</p>
            <p className={styles.risk}>{uc.risk}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
