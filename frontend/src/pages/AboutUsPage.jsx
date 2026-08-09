import React from 'react';
import { Heart, Sprout, Users, Shield, Award } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const AboutUsPage = () => {
  const { t } = useLanguage();

  return (
    <div className="page-container">
      {/* Banner */}
      <div style={{
        position: 'relative',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        minHeight: '360px',
        background: `linear-gradient(to right, rgba(18, 54, 31, 0.92) 0%, rgba(18, 54, 31, 0.7) 100%), url('https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat`,
        padding: '4rem 3rem',
        color: 'white',
        marginBottom: '3.5rem',
        boxShadow: 'var(--shadow-earthy)'
      }}>
        <div style={{ maxWidth: '680px' }}>
          <span style={{
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(4px)',
            color: 'var(--color-wheat-gold)',
            padding: '0.4rem 1rem',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.82rem',
            fontWeight: 700,
            display: 'inline-block',
            marginBottom: '1rem'
          }}>
            Human Story & Mission
          </span>

          <h1 style={{ fontSize: '2.8rem', color: '#FFFFFF', fontWeight: 800, lineHeight: 1.15, marginBottom: '1.25rem' }}>
            Built For The People Who Grow Our Food.
          </h1>

          <p style={{ fontSize: '1.15rem', color: 'rgba(255, 255, 255, 0.9)', lineHeight: 1.6, margin: 0 }}>
            AgriSaarthi was created with a simple, powerful belief: digital technology should honor the dignity, wisdom, and daily reality of Indian farmers.
          </p>
        </div>
      </div>

      {/* Story Sections */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        marginBottom: '3.5rem'
      }}>
        <div className="desi-card" style={{ padding: '2rem' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: 'var(--color-leaf-light)', color: 'var(--color-forest-green)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <Sprout size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.75rem' }}>
            Why We Built AgriSaarthi
          </h3>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.6 }}>
            Across India's villages, agricultural choices are often forced under uncertainty — changing monsoon patterns, unverified pesticides, and complex subsidy rules. AgriSaarthi bridges traditional field wisdom with verified agricultural science.
          </p>
        </div>

        <div className="desi-card" style={{ padding: '2rem' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: 'var(--color-wheat-light)', color: 'var(--color-mitti-brown)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <Heart size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.75rem' }}>
            Technology With a Human Purpose
          </h3>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.6 }}>
            We build invisible technology. Instead of overwhelming farmers with technical jargon or futuristic dashboards, AgriSaarthi presents clear, actionable recommendations in native Indian languages.
          </p>
        </div>

        <div className="desi-card" style={{ padding: '2rem' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: 'var(--color-mitti-light)', color: 'var(--color-forest-green)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <Users size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.75rem' }}>
            Supporting Indian Farmers
          </h3>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.6 }}>
            From paddy farmers in Mandya to wheat growers in Meerut, AgriSaarthi stands alongside farmers as their trustworthy digital companion — every step of the season.
          </p>
        </div>
      </div>
    </div>
  );
};
