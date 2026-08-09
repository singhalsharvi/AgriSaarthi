import React from 'react';
import { useLanguage } from '../../context/LanguageContext';

export const DesiStoryJourney = () => {
  const { t } = useLanguage();

  const steps = [
    { icon: '🌱', label: t('journey.step1'), desc: 'Soil & field parameters' },
    { icon: '🌦️', label: t('journey.step2'), desc: 'Rainfall & humidity' },
    { icon: '🌾', label: t('journey.step3'), desc: 'Optimized crop match' },
    { icon: '🌿', label: t('journey.step4'), desc: 'Early disease protection' },
    { icon: '🏛️', label: t('journey.step5'), desc: 'Subsidies & schemes' },
  ];

  return (
    <section style={{
      padding: '3rem 2rem',
      backgroundColor: 'var(--color-cream-surface)',
      borderRadius: 'var(--radius-lg)',
      border: '1.5px solid var(--color-cream-border)',
      marginBottom: '3.5rem'
    }}>
      <div style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto 2.5rem' }}>
        <span style={{
          fontSize: '0.8rem',
          fontWeight: 700,
          color: 'var(--color-mitti-brown)',
          textTransform: 'uppercase',
          letterSpacing: '0.06em'
        }}>
          Agricultural Workflow
        </span>
        <h2 style={{ fontSize: '2rem', color: 'var(--color-forest-green-dark)', marginTop: '0.35rem' }}>
          {t('journey.title')}
        </h2>
        <p style={{ color: 'var(--color-charcoal-muted)', fontSize: '0.95rem' }}>
          A transparent, step-by-step journey designed around the real Indian farmer's seasonal calendar.
        </p>
      </div>

      {/* Visual Journey Bar */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '1.25rem',
        position: 'relative'
      }}>
        {steps.map((step, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: 'var(--color-white)',
              padding: '1.5rem 1rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-cream-border)',
              textAlign: 'center',
              boxShadow: 'var(--shadow-sm)',
              position: 'relative'
            }}
          >
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              backgroundColor: 'var(--color-leaf-light)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              margin: '0 auto 1rem'
            }}>
              {step.icon}
            </div>

            <h3 style={{ fontSize: '0.95rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.35rem', fontWeight: 800 }}>
              {step.label}
            </h3>

            <p style={{ fontSize: '0.8rem', color: 'var(--color-charcoal-muted)', margin: 0 }}>
              {step.desc}
            </p>

            <span style={{
              position: 'absolute',
              top: '0.5rem',
              right: '0.75rem',
              fontSize: '0.7rem',
              fontWeight: 800,
              color: 'var(--color-mitti-brown)',
              opacity: 0.5
            }}>
              0{idx + 1}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
};
