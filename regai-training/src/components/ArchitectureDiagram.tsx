import React from 'react';
import Mermaid from '@theme/Mermaid';
import styles from './ArchitectureDiagram.module.css';

export interface ArchComponent {
  name: string;
  responsibility: string;
}

interface ArchitectureDiagramProps {
  mermaid: string;
  components: ArchComponent[];
  title?: string;
}

/**
 * The Content Standard's "Reference Architecture" section (Section 2, item
 * 5): a labeled diagram plus an explicit component-responsibility list, so
 * the diagram never has to stand alone without prose explaining each box.
 */
export default function ArchitectureDiagram({mermaid, components, title}: ArchitectureDiagramProps): JSX.Element {
  return (
    <div className={styles.wrapper}>
      {title ? <p className={styles.title}>{title}</p> : null}
      <div className={styles.diagram}>
        <Mermaid value={mermaid} />
      </div>
      <dl className={styles.responsibilities}>
        {components.map((c) => (
          <div key={c.name} className={styles.row}>
            <dt>{c.name}</dt>
            <dd>{c.responsibility}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
