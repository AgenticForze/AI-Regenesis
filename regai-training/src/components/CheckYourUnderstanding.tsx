import React, {useState} from 'react';
import styles from './CheckYourUnderstanding.module.css';

export interface CheckQuestion {
  question: string;
  answer: string;
}

interface CheckYourUnderstandingProps {
  questions: CheckQuestion[];
  /** Optional link into the capstone repo for a hands-on exercise */
  exerciseUrl?: string;
  exerciseLabel?: string;
}

export default function CheckYourUnderstanding({
  questions,
  exerciseUrl,
  exerciseLabel,
}: CheckYourUnderstandingProps): JSX.Element {
  const [open, setOpen] = useState<Record<number, boolean>>({});

  return (
    <div className={styles.wrapper}>
      <ol className={styles.list}>
        {questions.map((q, i) => (
          <li key={i} className={styles.item}>
            <button
              className={styles.questionBtn}
              onClick={() => setOpen((o) => ({...o, [i]: !o[i]}))}
              aria-expanded={!!open[i]}
            >
              <span>{q.question}</span>
              <span className={styles.chevron}>{open[i] ? '\u2212' : '+'}</span>
            </button>
            {open[i] ? <p className={styles.answer}>{q.answer}</p> : null}
          </li>
        ))}
      </ol>
      {exerciseUrl ? (
        <a className={styles.exercise} href={exerciseUrl}>
          Hands-on exercise: {exerciseLabel ?? 'try it in the capstone repo'} &rarr;
        </a>
      ) : null}
    </div>
  );
}
