import React, { useState } from 'react';
import { Menu, X, Globe, User, Sprout, Stethoscope, Landmark, Home, Grid, Info, HelpCircle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';

export const MobileHeader = ({ activeTab, setActiveTab }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { t, setIsLangModalOpen, currentLang, languages } = useLanguage();
  const { user } = useAuth();

  const currentLangObj = languages.find(l => l.code === currentLang) || languages[0];

  const handleNav = (tabId) => {
    setActiveTab(tabId);
    setIsOpen(false);
  };

  return (
    <>
      <header style={{
        height: 'var(--header-height-mobile)',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        backgroundColor: 'var(--color-white)',
        borderBottom: '1px solid var(--color-cream-border)',
        display: 'none',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 1.25rem',
        zIndex: 50,
        boxShadow: 'var(--shadow-sm)'
      }} className="mobile-header-bar">
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            backgroundColor: 'var(--color-leaf-light)',
            border: '1px solid var(--color-leaf-green)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-forest-green)'
          }}>
            🌾
          </div>
          <div>
            <h1 style={{ fontSize: '1.15rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
              AgriSaarthi
            </h1>
          </div>
        </div>

        {/* Right Action Icons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={() => setIsLangModalOpen(true)}
            style={{
              padding: '0.4rem 0.65rem',
              backgroundColor: 'var(--color-cream-surface)',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.8rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
              color: 'var(--color-forest-green)'
            }}
          >
            <Globe size={16} />
            <span>{currentLangObj.code.toUpperCase()}</span>
          </button>

          <button
            onClick={() => setIsOpen(!isOpen)}
            style={{ padding: '0.4rem', color: 'var(--color-charcoal)' }}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </header>

      {/* Mobile Drawer Menu */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: 'var(--header-height-mobile)',
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: 49,
          backdropFilter: 'blur(3px)'
        }} onClick={() => setIsOpen(false)}>
          <div style={{
            backgroundColor: 'var(--color-white)',
            width: '82%',
            maxWidth: '320px',
            height: '100%',
            padding: '1.5rem 1.25rem',
            display: 'flex',
            flexDirection: 'column',
            justify: 'space-between',
            boxShadow: 'var(--shadow-lg)'
          }} onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Navigation
              </p>
              
              <button onClick={() => handleNav('home')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <Home size={18} color="var(--color-forest-green)" /> {t('nav.home')}
              </button>
              <button onClick={() => handleNav('features')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <Grid size={18} color="var(--color-forest-green)" /> {t('nav.features')}
              </button>
              <button onClick={() => handleNav('about')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <Info size={18} color="var(--color-forest-green)" /> {t('nav.about')}
              </button>

              <div style={{ height: '1px', backgroundColor: 'var(--color-cream-border)', margin: '0.5rem 0' }} />

              <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Services
              </p>
              <button onClick={() => handleNav('crop')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <span>🌾</span> {t('nav.cropRec')}
              </button>
              <button onClick={() => handleNav('disease')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <span>🌿</span> {t('nav.diseaseDet')}
              </button>
              <button onClick={() => handleNav('schemes')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <span>🏛️</span> {t('nav.govtSchemes')}
              </button>
              <button onClick={() => handleNav('help')} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem', fontWeight: 600, color: 'var(--color-charcoal)' }}>
                <HelpCircle size={18} color="var(--color-forest-green)" /> {t('nav.help')}
              </button>
            </div>

            <div style={{ borderTop: '1px solid var(--color-cream-border)', paddingTop: '1rem' }}>
              <button
                onClick={() => handleNav(user ? 'dashboard' : 'signin')}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: 'var(--color-forest-green)',
                  color: 'white',
                  borderRadius: 'var(--radius-md)',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem'
                }}
              >
                <User size={18} />
                <span>{user ? user.name : t('nav.signIn')}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
