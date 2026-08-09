import React, { useState, useEffect } from 'react';
import { CheckCircle2, Loader2, Search } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const ScannerState = () => {
  const { t } = useLanguage();
  const [step, setStep] = useState(0);

  const steps = [
    t('disease.step1'),
    t('disease.step2'),
    t('disease.step3'),
    t('disease.step4')
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setStep(prev => (prev < steps.length ? prev + 1 : prev));
    }, 600);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      border: '1.5px solid var(--color-cream-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '3rem 2rem',
      textAlign: 'center',
      boxShadow: 'var(--shadow-md)',
      marginBottom: '2.5rem'
    }} className="animate-fade-in">
      <div style={{
        width: '64px',
        height: '64px',
        borderRadius: '50%',
        backgroundColor: 'var(--color-leaf-light)',
        border: '2px solid var(--color-leaf-green)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto 1.25rem',
        color: 'var(--color-forest-green)'
      }}>
        <Search size={30} className="animate-pulse-subtle" />
      </div>

      <h3 style={{ fontSize: '1.35rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.5rem', fontWeight: 800 }}>
        Looking closely at your plant...
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--color-charcoal-muted)', marginBottom: '2rem' }}>
        Scanning leaf texture, lesion patterns & pathogen characteristics...
      </p>

      <div style={{
        maxWidth: '380px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        textAlign: 'left'
      }}>
        {steps.map((st, idx) => {
          const isDone = idx < step;
          const isCurrent = idx === step;
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.85rem',
                padding: '0.65rem 1rem',
                borderRadius: 'var(--radius-md)',
                backgroundColor: isDone ? 'var(--color-leaf-light)' : 'var(--color-cream-surface)',
                border: isDone ? '1px solid var(--color-leaf-green)' : '1px solid var(--color-cream-border)'
              }}
            >
              {isDone ? (
                <CheckCircle2 size={18} color="var(--color-forest-green)" />
              ) : isCurrent ? (
                <Loader2 size={18} color="var(--color-mustard)" className="animate-pulse-subtle" />
              ) : (
                <div style={{ width: '18px', height: '18px', borderRadius: '50%', border: '2px solid var(--color-cream-border)' }} />
              )}
              <span style={{ fontSize: '0.88rem', fontWeight: isDone || isCurrent ? 700 : 500, color: isDone ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal-muted)' }}>
                {st}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
