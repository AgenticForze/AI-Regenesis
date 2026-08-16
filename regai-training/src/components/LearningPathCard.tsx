import React from 'react';
import Link from '@docusaurus/Link';
import styles from './LearningPathCard.module.css';

interface LearningPathCardProps {
  name: string;
  audience: string;
  route: string;
  href: string;
  accent?: 'teal' | 'amber' | 'ink';
}

export default function LearningPathCard({
  name,
  audience,
  route,
  href,
  accent = 'teal',
}: LearningPathCardProps): JSX.Element {
  return (
    <Link to={href} className={`${styles.card} ${styles[accent]}`}>
      <p className={styles.audience}>{audience}</p>
      <h3 className={styles.name}>{name}</h3>
      <p className={styles.route}>{route}</p>
      <span className={styles.cta}>Start this path &rarr;</span>
    </Link>
  );
}
