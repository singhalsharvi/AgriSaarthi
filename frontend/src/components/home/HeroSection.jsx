import React from 'react';
import { ArrowRight, Compass, ShieldCheck } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { AgriSaarthiLogo } from '../brand/AgriSaarthiLogo';

export const HeroSection = ({ onGetStarted, onExploreFeatures }) => {
  const { t } = useLanguage();

  return (
    <section style={{
      position: 'relative',
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      marginBottom: '3.5rem',
      boxShadow: 'var(--shadow-earthy)',
      border: '1px solid var(--color-cream-border)'
    }}>
      {/* Background Hero Image */}
      <div style={{
        position: 'relative',
        minHeight: '540px',
        display: 'flex',
        alignItems: 'center',
        background: `linear-gradient(90deg, rgba(8, 38, 21, 0.96) 0%, rgba(18, 54, 31, 0.82) 45%, rgba(9, 31, 18, 0.28) 100%), url('https://images.unsplash.com/photo-1592982537447-6f2a6a0e5c9f?auto=format&fit=crop&w=1800&q=90') center/cover no-repeat`,
        padding: '3.5rem 3rem',
        color: 'var(--color-white)'
      }}>
        <div style={{ maxWidth: '680px', zIndex: 2 }}>
          <div style={{ marginBottom: '2.25rem' }}>
            <AgriSaarthiLogo light />
          </div>
          {/* Subdued Badge */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.45rem 1rem',
            backgroundColor: 'rgba(255, 255, 255, 0.15)',
            backdropFilter: 'blur(8px)',
            borderRadius: 'var(--radius-full)',
            border: '1px solid rgba(255, 255, 255, 0.25)',
            fontSize: '0.85rem',
            fontWeight: 600,
            color: 'var(--color-wheat-gold)',
            marginBottom: '1.5rem'
          }}>
            <ShieldCheck size={16} />
            <span>{t('hero.badge')}</span>
          </div>

          {/* Main Headline */}
          <h1 style={{
            fontSize: 'clamp(2.4rem, 5vw, 3.8rem)',
            fontWeight: 800,
            lineHeight: 1.15,
            color: '#FFFFFF',
            marginBottom: '1.25rem',
            letterSpacing: '-0.02em'
          }}>
            {t('hero.title')}
          </h1>

          {/* Subtitle */}
          <p style={{
            fontSize: '1.2rem',
            color: 'rgba(255, 255, 255, 0.92)',
            marginBottom: '2rem',
            lineHeight: 1.6,
            fontWeight: 400
          }}>
            {t('hero.subtitle')}
          </p>

          {/* CTAs */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
            <button
              onClick={onGetStarted}
              style={{
                backgroundColor: 'var(--color-wheat-gold)',
                color: 'var(--color-forest-green-dark)',
                padding: '1rem 2.25rem',
                borderRadius: 'var(--radius-full)',
                fontWeight: 800,
                fontSize: '1.05rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.65rem',
                boxShadow: '0 4px 20px rgba(229, 184, 66, 0.35)',
                transition: 'transform 0.2s ease'
              }}
            >
              <span>{t('hero.ctaPrimary')}</span>
              <ArrowRight size={20} />
            </button>

            <button
              onClick={onExploreFeatures}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.15)',
                color: '#FFFFFF',
                border: '1.5px solid rgba(255, 255, 255, 0.4)',
                backdropFilter: 'blur(6px)',
                padding: '1rem 2rem',
                borderRadius: 'var(--radius-full)',
                fontWeight: 700,
                fontSize: '1rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}
            >
              <Compass size={18} />
              <span>{t('hero.ctaSecondary')}</span>
            </button>
          </div>

          {/* Subtle Desi Phrase */}
          <div style={{
            marginTop: '2.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem',
            opacity: 0.95
          }}>
            <span style={{ fontSize: '1.25rem' }}>🌾</span>
            <span style={{
              fontSize: '0.95rem',
              fontWeight: 700,
              letterSpacing: '0.04em',
              color: 'var(--color-wheat-gold)'
            }}>
              "{t('brandPhrase')}"
            </span>
          </div>
        </div>
      </div>
    </section>
  );
};
