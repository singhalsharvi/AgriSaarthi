import React from 'react';
import { ArrowRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const QuickActions = ({ onNavigate }) => {
  const { t } = useLanguage();

  const actions = [
    {
      id: 'crop',
      title: t('nav.cropRec'),
      desc: 'Analyze location & soil for top 3 crops',
      icon: '🌾',
      bg: 'var(--color-leaf-light)',
      border: 'var(--color-leaf-green)'
    },
    {
      id: 'disease',
      title: t('nav.diseaseDet'),
      desc: 'Upload plant photo for instant diagnosis',
      icon: '🌿',
      bg: 'var(--color-wheat-light)',
      border: 'var(--color-mustard)'
    },
    {
      id: 'schemes',
      title: t('nav.govtSchemes'),
      desc: 'Find eligible subsidies & financial aid',
      icon: '🏛️',
      bg: 'var(--color-mitti-light)',
      border: 'var(--color-mitti-brown)'
    }
  ];

  return (
    <div style={{ marginBottom: '2.5rem' }}>
      <h3 style={{ fontSize: '1.2rem', color: 'var(--color-forest-green-dark)', marginBottom: '1rem' }}>
        ⚡ Quick Actions
      </h3>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
        gap: '1.25rem'
      }}>
        {actions.map(act => (
          <div
            key={act.id}
            onClick={() => onNavigate(act.id)}
            style={{
              padding: '1.35rem',
              borderRadius: 'var(--radius-lg)',
              backgroundColor: 'var(--color-white)',
              border: `1.5px solid var(--color-cream-border)`,
              boxShadow: 'var(--shadow-sm)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              flexDirection: 'column',
              justify: 'space-between'
            }}
            className="desi-card"
          >
            <div>
              <div style={{
                width: '42px',
                height: '42px',
                borderRadius: '12px',
                backgroundColor: act.bg,
                border: `1px solid ${act.border}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.35rem',
                marginBottom: '1rem'
              }}>
                {act.icon}
              </div>
              <h4 style={{ fontSize: '1.1rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.35rem' }}>
                {act.title}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-charcoal-muted)', margin: 0, lineHeight: 1.5 }}>
                {act.desc}
              </p>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontSize: '0.85rem',
              fontWeight: 700,
              color: 'var(--color-forest-green)',
              marginTop: '1.25rem'
            }}>
              <span>Open Tool</span>
              <ArrowRight size={16} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
