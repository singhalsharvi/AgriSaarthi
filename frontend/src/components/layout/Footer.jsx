import React from 'react';
import { useLanguage } from '../../context/LanguageContext';

export const Footer = ({ setActiveTab }) => {
  const { t, changeLanguage, languages } = useLanguage();

  return (
    <footer style={{
      backgroundColor: 'var(--color-cream-surface)',
      borderTop: '1px solid var(--color-cream-border)',
      padding: '3.5rem 2.5rem 2.5rem',
      marginTop: 'auto'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '2.5rem',
        marginBottom: '2.5rem'
      }}>
        {/* Brand Column */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
            <span style={{ fontSize: '1.75rem' }}>🌾</span>
            <h3 style={{ fontSize: '1.4rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
              AgriSaarthi
            </h3>
          </div>
          <p style={{ color: 'var(--color-charcoal-muted)', fontSize: '0.92rem', marginBottom: '1rem', lineHeight: 1.6 }}>
            "Technology for Every Farmer."<br />
            Built with real Indian farmers in mind — empowering crop choices, plant health & government benefit access.
          </p>
          <p style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>
            Apni Fasal. Apna Faisla.
          </p>
        </div>

        {/* Core Services Links */}
        <div>
          <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
            Core Services
          </h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            <li>
              <button onClick={() => setActiveTab('crop')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                🌾 Crop Recommendation
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('disease')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                🌿 Plant Disease Detection
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('schemes')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                🏛️ Government Schemes
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('dashboard')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                📋 Farmer Dashboard
              </button>
            </li>
          </ul>
        </div>

        {/* Quick Links */}
        <div>
          <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
            Platform
          </h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            <li>
              <button onClick={() => setActiveTab('home')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                Home
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('features')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                Features
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('about')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                About Us
              </button>
            </li>
            <li>
              <button onClick={() => setActiveTab('help')} style={{ color: 'var(--color-charcoal)', fontSize: '0.9rem' }}>
                Help & FAQs
              </button>
            </li>
          </ul>
        </div>

        {/* Equal 5 Languages */}
        <div>
          <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
            🌐 Select Language
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {languages.map(lang => (
              <button
                key={lang.code}
                onClick={() => changeLanguage(lang.code)}
                style={{
                  padding: '0.4rem 0.75rem',
                  backgroundColor: 'var(--color-white)',
                  border: '1px solid var(--color-cream-border)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  color: 'var(--color-forest-green)'
                }}
              >
                {lang.nativeName}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        paddingTop: '1.5rem',
        borderTop: '1px solid var(--color-cream-border)',
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justify: 'space-between',
        gap: '1rem',
        fontSize: '0.82rem',
        color: 'var(--color-charcoal-muted)'
      }}>
        <p>© 2026 AgriSaarthi — Empowering Indian Agriculture. All rights reserved.</p>
        <div style={{ display: 'flex', gap: '1.25rem' }}>
          <span>Privacy Policy</span>
          <span>Terms of Service</span>
          <span>Krishi Helpline: 1800-180-1551</span>
        </div>
      </div>
    </footer>
  );
};
