import React from 'react';
import styles from './PrincipleCard.module.css';

interface PrincipleCardProps {
  number: string;
  name: string;
  description: string;
}

export default function PrincipleCard({number, name, description}: PrincipleCardProps): JSX.Element {
  return (
    <div className={styles.card}>
      <span className={styles.number}>{number}</span>
      <h3 className={styles.name}>{name}</h3>
      <p className={styles.description}>{description}</p>
    </div>
  );
}
