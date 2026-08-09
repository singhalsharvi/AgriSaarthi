import React from 'react';
import { X, Check } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const LanguageModal = () => {
  const { 
    isLangModalOpen, 
    setIsLangModalOpen, 
    languages, 
    currentLang, 
    changeLanguage,
    t 
  } = useLanguage();

  if (!isLangModalOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(26, 28, 25, 0.65)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1.25rem'
    }} onClick={() => setIsLangModalOpen(false)}>
      <div style={{
        backgroundColor: 'var(--color-white)',
        borderRadius: 'var(--radius-lg)',
        width: '100%',
        maxWidth: '520px',
        padding: '2rem',
        boxShadow: 'var(--shadow-lg)',
        border: '1.5px solid var(--color-cream-border)',
        position: 'relative'
      }} onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '1.5rem',
          paddingBottom: '1rem',
          borderBottom: '1px solid var(--color-cream-border)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '1.75rem' }}>🌐</span>
            <div>
              <h2 style={{ fontSize: '1.35rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
                {t('nav.language')}
              </h2>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-charcoal-muted)', margin: 0 }}>
                Select your preferred language / अपनी भाषा चुनें
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsLangModalOpen(false)}
            style={{
              padding: '0.5rem',
              color: 'var(--color-charcoal-muted)',
              borderRadius: '50%',
              backgroundColor: 'var(--color-cream-surface)'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* 5 Equal Language Buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {languages.map(lang => {
            const isSelected = currentLang === lang.code;
            return (
              <button
                key={lang.code}
                onClick={() => {
                  changeLanguage(lang.code);
                  setIsLangModalOpen(false);
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '1rem 1.25rem',
                  borderRadius: 'var(--radius-md)',
                  border: isSelected 
                    ? '2px solid var(--color-forest-green)' 
                    : '1.5px solid var(--color-cream-border)',
                  backgroundColor: isSelected 
                    ? 'var(--color-leaf-light)' 
                    : 'var(--color-white)',
                  transition: 'all 0.2s ease',
                  textAlign: 'left'
                }}
              >
                <div>
                  <span style={{
                    fontSize: '1.15rem',
                    fontWeight: 700,
                    color: isSelected ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal)',
                    display: 'block',
                    marginBottom: '0.15rem'
                  }}>
                    {lang.nativeName}
                  </span>
                  <span style={{
                    fontSize: '0.85rem',
                    color: isSelected ? 'var(--color-forest-green)' : 'var(--color-charcoal-muted)'
                  }}>
                    {lang.name}
                  </span>
                </div>

                {isSelected && (
                  <div style={{
                    width: '28px',
                    height: '28px',
                    borderRadius: '50%',
                    backgroundColor: 'var(--color-forest-green)',
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Check size={16} strokeWidth={3} />
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Note */}
        <div style={{
          marginTop: '1.5rem',
          padding: '0.85rem',
          backgroundColor: 'var(--color-cream-surface)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
          fontSize: '0.8rem',
          color: 'var(--color-mitti-brown)',
          fontWeight: 600
        }}>
          💡 English is default. Switch anytime from sidebar or footer.
        </div>
      </div>
    </div>
  );
};
