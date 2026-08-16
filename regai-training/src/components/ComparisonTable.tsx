import React from 'react';
import styles from './ComparisonTable.module.css';

export interface ComparisonRow {
  aspect: string;
  values: string[];
  /** Marks the row that most often decides which option to reach for */
  decisive?: boolean;
}

interface ComparisonTableProps {
  /** Column headers, e.g. ["RAG", "Fine-Tuning", "Prompting"] */
  columns: string[];
  rows: ComparisonRow[];
  caption?: string;
}

/**
 * The Content Standard's mandatory "Comparison & Related Concepts" table
 * (Section 2, item 4) — contrasts a concept with 2-4 adjacent ones.
 */
export default function ComparisonTable({columns, rows, caption}: ComparisonTableProps): JSX.Element {
  return (
    <figure className={styles.figure}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.aspectHeader}>Aspect</th>
            {columns.map((c) => (
              <th key={c}>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.aspect} className={row.decisive ? styles.decisiveRow : undefined}>
              <th scope="row" className={styles.aspectCell}>
                {row.decisive ? <span className={styles.pin} title="Usually the deciding factor">&#9670;</span> : null}
                {row.aspect}
              </th>
              {row.values.map((v, i) => (
                <td key={i}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {caption ? <figcaption className={styles.caption}>{caption}</figcaption> : null}
    </figure>
  );
}
