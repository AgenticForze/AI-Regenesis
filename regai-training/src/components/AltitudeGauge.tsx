import React from 'react';
import styles from './AltitudeGauge.module.css';

/**
 * Signature hero element. The curriculum's core idea is dual-altitude
 * explanation (HL pass vs. deep-dive pass) and phases as a climb from
 * "what is AI" to frontier agentic research — so the hero renders that
 * literally as an instrument dial, FL00 (Phase 0) to FL18 (Phase 18),
 * with the two altitude bands (teal = HL cruise, amber = deep-dive) as
 * the only color statement on the page.
 */
export default function AltitudeGauge(): JSX.Element {
  const totalPhases = 19;
  const ticks = Array.from({length: totalPhases}, (_, i) => i);

  return (
    <div className={styles.gauge} role="img" aria-label="Curriculum altitude gauge, Phase 0 through Phase 18">
      <svg viewBox="0 0 640 220" className={styles.svg}>
        <line x1="20" y1="180" x2="620" y2="180" className={styles.baseline} />
        {ticks.map((i) => {
          const x = 20 + (i / (totalPhases - 1)) * 600;
          const isMajor = i % 3 === 0;
          const band = i <= 8 ? 'foundation' : i <= 13 ? 'practitioner' : 'advanced';
          return (
            <g key={i}>
              <line
                x1={x}
                y1={180}
                x2={x}
                y2={isMajor ? 150 : 165}
                className={`${styles.tick} ${styles[band]}`}
              />
              {isMajor && (
                <text x={x} y={200} textAnchor="middle" className={styles.tickLabel}>
                  FL{String(i).padStart(2, '0')}
                </text>
              )}
            </g>
          );
        })}
        <path
          d="M 20 180 Q 320 20 620 60"
          className={styles.climbPath}
          fill="none"
        />
        <circle cx="620" cy="60" r="6" className={styles.needleTip} />
      </svg>
      <div className={styles.legend}>
        <span className={styles.legendItem}><i className={styles.dotFoundation} /> Foundations (0–8)</span>
        <span className={styles.legendItem}><i className={styles.dotPractitioner} /> Practitioner (9–13)</span>
        <span className={styles.legendItem}><i className={styles.dotAdvanced} /> Advanced / Frontier (14–18)</span>
      </div>
    </div>
  );
}
