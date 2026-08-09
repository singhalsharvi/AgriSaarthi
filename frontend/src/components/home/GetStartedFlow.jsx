import React from 'react';
import { X, ArrowRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const GetStartedFlow = ({ isOpen, onClose, onSelectOption }) => {
  const { t } = useLanguage();

  if (!isOpen) return null;

  const options = [
    {
      id: 'crop',
      icon: '🌾',
      title: t('getStarted.opt1'),
      desc: 'Find the best crops suited to your soil, weather, season and location.',
      image: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=600&q=80',
      badge: 'Crop Recommendation'
    },
    {
      id: 'disease',
      icon: '🌿',
      title: t('getStarted.opt2'),
      desc: 'Upload a plant leaf photo and diagnose possible crop diseases & cures.',
      image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=600&q=80',
      badge: 'Plant Health'
    },
    {
      id: 'schemes',
      icon: '🏛️',
      title: t('getStarted.opt3'),
      desc: 'Discover government subsidies, insurance schemes and financial support.',
      image: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=600&q=80',
      badge: 'Government Schemes'
    }
  ];

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(26, 28, 25, 0.7)',
      backdropFilter: 'blur(5px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1.25rem'
    }} onClick={onClose}>
      <div style={{
        backgroundColor: 'var(--color-white)',
        borderRadius: 'var(--radius-lg)',
        width: '100%',
        maxWidth: '840px',
        padding: '2.5rem',
        boxShadow: 'var(--shadow-lg)',
        border: '1.5px solid var(--color-cream-border)',
        maxHeight: '90vh',
        overflowY: 'auto'
      }} onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          marginBottom: '2rem'
        }}>
          <div>
            <span style={{
              fontSize: '0.8rem',
              fontWeight: 700,
              color: 'var(--color-forest-green)',
              backgroundColor: 'var(--color-leaf-light)',
              padding: '0.35rem 0.75rem',
              borderRadius: 'var(--radius-full)'
            }}>
              Farmer Guided Flow
            </span>
            <h2 style={{ fontSize: '1.75rem', color: 'var(--color-forest-green-dark)', marginTop: '0.5rem', margin: '0.5rem 0 0.25rem' }}>
              {t('getStarted.title')}
            </h2>
            <p style={{ color: 'var(--color-charcoal-muted)', margin: 0 }}>
              {t('getStarted.subtitle')}
            </p>
          </div>

          <button
            onClick={onClose}
            style={{
              padding: '0.5rem',
              borderRadius: '50%',
              backgroundColor: 'var(--color-cream-surface)',
              color: 'var(--color-charcoal)'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* 3 Large Photo Options */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '1.5rem'
        }}>
          {options.map(opt => (
            <div
              key={opt.id}
              onClick={() => {
                onSelectOption(opt.id);
                onClose();
              }}
              style={{
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                border: '1.5px solid var(--color-cream-border)',
                backgroundColor: 'var(--color-white)',
                cursor: 'pointer',
                transition: 'all 0.25s ease',
                boxShadow: 'var(--shadow-sm)',
                display: 'flex',
                flexDirection: 'column'
              }}
              className="desi-card"
            >
              <div style={{
                height: '150px',
                background: `url('${opt.image}') center/cover no-repeat`,
                position: 'relative',
                padding: '0.85rem'
              }}>
                <span style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(4px)',
                  color: 'var(--color-forest-green-dark)',
                  padding: '0.3rem 0.75rem',
                  borderRadius: 'var(--radius-full)',
                  fontSize: '0.75rem',
                  fontWeight: 700
                }}>
                  {opt.badge}
                </span>
              </div>

              <div style={{ padding: '1.25rem', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '1.5rem' }}>{opt.icon}</span>
                    <h3 style={{ fontSize: '1.1rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
                      {opt.title}
                    </h3>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    {opt.desc}
                  </p>
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  fontSize: '0.88rem',
                  fontWeight: 700,
                  color: 'var(--color-forest-green)'
                }}>
                  <span>Proceed</span>
                  <ArrowRight size={16} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
