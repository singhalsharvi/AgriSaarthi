import React, { useState, useEffect } from 'react';
import { CheckCircle2, Loader2 } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const CropAnalysisState = () => {
  const { t } = useLanguage();
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    t('crop.step1'),
    t('crop.step2'),
    t('crop.step3'),
    t('crop.step4')
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep(prev => (prev < steps.length ? prev + 1 : prev));
    }, 700);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      border: '1.5px solid var(--color-cream-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '2.5rem 2rem',
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
        <Loader2 size={32} className="animate-pulse-subtle" />
      </div>

      <h3 style={{ fontSize: '1.4rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.5rem', fontWeight: 800 }}>
        {t('crop.analyzing')}
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--color-charcoal-muted)', marginBottom: '2rem' }}>
        Evaluating weather history, seasonal rainfall & regional soil profiles...
      </p>

      {/* Jargon-Free Step Checklist */}
      <div style={{
        maxWidth: '420px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.85rem',
        textAlign: 'left'
      }}>
        {steps.map((st, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;
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
                border: isDone ? '1px solid var(--color-leaf-green)' : '1px solid var(--color-cream-border)',
                transition: 'all 0.3s ease'
              }}
            >
              {isDone ? (
                <CheckCircle2 size={20} color="var(--color-forest-green)" />
              ) : isCurrent ? (
                <Loader2 size={20} color="var(--color-mustard)" className="animate-pulse-subtle" />
              ) : (
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', border: '2px solid var(--color-cream-border)' }} />
              )}
              <span style={{
                fontSize: '0.9rem',
                fontWeight: isDone || isCurrent ? 700 : 500,
                color: isDone ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal-muted)'
              }}>
                {st}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
