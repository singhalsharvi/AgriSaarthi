import React from 'react';
import { 
  Home, 
  Grid, 
  Info, 
  Sprout, 
  Stethoscope, 
  Landmark, 
  HelpCircle, 
  Globe, 
  User, 
  LogOut,
  LayoutDashboard
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';
import { AgriSaarthiLogo } from '../brand/AgriSaarthiLogo';

export const DesktopSidebar = ({ activeTab, setActiveTab }) => {
  const { t, setIsLangModalOpen, currentLang, languages } = useLanguage();
  const { user, signOut } = useAuth();

  const currentLangObj = languages.find(l => l.code === currentLang) || languages[0];

  const navItemsMain = [
    { id: 'home', label: t('nav.home'), icon: Home },
    { id: 'features', label: t('nav.features'), icon: Grid },
    { id: 'about', label: t('nav.about'), icon: Info },
  ];

  const navItemsFeatures = [
    { id: 'crop', label: t('nav.cropRec'), icon: Sprout, badge: '🌾' },
    { id: 'disease', label: t('nav.diseaseDet'), icon: Stethoscope, badge: '🌿' },
    { id: 'schemes', label: t('nav.govtSchemes'), icon: Landmark, badge: '🏛️' },
    { id: 'dashboard', label: t('nav.dashboard'), icon: LayoutDashboard, badge: '📋' },
  ];

  return (
    <aside style={{
      width: 'var(--sidebar-width)',
      height: '100vh',
      position: 'fixed',
      top: 0,
      left: 0,
      backgroundColor: 'var(--color-white)',
      borderRight: '1px solid var(--color-cream-border)',
      display: 'flex',
      flexDirection: 'column',
      justify: 'space-between',
      zIndex: 40,
      boxShadow: 'var(--shadow-sm)'
    }} className="desktop-sidebar-container">
      {/* Brand Header */}
      <div>
        <div style={{
          padding: '1.5rem 1.5rem 1.25rem',
          borderBottom: '1px solid var(--color-cream-border)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.85rem'
        }}>
          <AgriSaarthiLogo />
        </div>

        {/* Main Navigation */}
        <div style={{ padding: '1.25rem 1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginBottom: '1.25rem' }}>
            {navItemsMain.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.85rem',
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    color: isActive ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal-muted)',
                    backgroundColor: isActive ? 'var(--color-leaf-light)' : 'transparent',
                    fontWeight: isActive ? 700 : 500,
                    fontSize: '0.92rem',
                    transition: 'all 0.2s ease',
                    textAlign: 'left'
                  }}
                >
                  <Icon size={19} color={isActive ? 'var(--color-forest-green)' : 'currentColor'} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div style={{
            height: '1px',
            backgroundColor: 'var(--color-cream-border)',
            margin: '0.5rem 0.5rem 1.25rem'
          }} />

          {/* Core Agricultural Features */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
            <span style={{
              fontSize: '0.72rem',
              fontWeight: 700,
              color: 'var(--color-mitti-brown)',
              letterSpacing: '0.06em',
              padding: '0 0.85rem 0.4rem',
              textTransform: 'uppercase'
            }}>
              Core Services
            </span>

            {navItemsFeatures.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    color: isActive ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal)',
                    backgroundColor: isActive ? 'var(--color-leaf-light)' : 'transparent',
                    borderLeft: isActive ? '3.5px solid var(--color-forest-green)' : '3.5px solid transparent',
                    fontWeight: isActive ? 700 : 500,
                    fontSize: '0.9rem',
                    transition: 'all 0.2s ease',
                    textAlign: 'left'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ fontSize: '1.1rem' }}>{item.badge}</span>
                    <span>{item.label}</span>
                  </div>
                </button>
              );
            })}
          </div>

          <div style={{
            height: '1px',
            backgroundColor: 'var(--color-cream-border)',
            margin: '1.25rem 0.5rem 1.25rem'
          }} />

          {/* Help & Support */}
          <button
            onClick={() => setActiveTab('help')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.85rem',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-md)',
              width: '100%',
              color: activeTab === 'help' ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal-muted)',
              backgroundColor: activeTab === 'help' ? 'var(--color-leaf-light)' : 'transparent',
              fontWeight: activeTab === 'help' ? 700 : 500,
              fontSize: '0.9rem',
              textAlign: 'left'
            }}
          >
            <HelpCircle size={19} color={activeTab === 'help' ? 'var(--color-forest-green)' : 'currentColor'} />
            <span>{t('nav.help')}</span>
          </button>
        </div>
      </div>

      {/* Footer Controls: Language & Sign In */}
      <div style={{
        padding: '1.25rem 1rem',
        borderTop: '1px solid var(--color-cream-border)',
        backgroundColor: 'var(--color-cream-bg)',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem'
      }}>
        {/* Language Button */}
        <button
          onClick={() => setIsLangModalOpen(true)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0.65rem 0.85rem',
            backgroundColor: 'var(--color-white)',
            border: '1.5px solid var(--color-cream-border)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--color-charcoal)',
            fontSize: '0.85rem',
            fontWeight: 600
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Globe size={18} color="var(--color-forest-green)" />
            <span>{currentLangObj.nativeName}</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--color-mitti-brown)', backgroundColor: 'var(--color-cream-surface)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
            🌐 Switch
          </span>
        </button>

        {/* Farmer Profile / Sign In */}
        {user ? (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0.65rem 0.85rem',
            backgroundColor: 'var(--color-leaf-light)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-leaf-green)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: 'var(--color-forest-green)',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.85rem',
                fontWeight: 700
              }}>
                {user.name.charAt(0)}
              </div>
              <div>
                <p style={{ margin: 0, fontSize: '0.85rem', fontWeight: 700, color: 'var(--color-forest-green-dark)' }}>
                  {user.name}
                </p>
                <p style={{ margin: 0, fontSize: '0.72rem', color: 'var(--color-charcoal-muted)' }}>
                  {user.location.split(',')[0]}
                </p>
              </div>
            </div>
            <button 
              onClick={signOut} 
              title="Sign Out"
              style={{ color: 'var(--color-terracotta)', padding: '0.3rem' }}
            >
              <LogOut size={17} />
            </button>
          </div>
        ) : (
          <button
            onClick={() => setActiveTab('signin')}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              padding: '0.75rem',
              backgroundColor: 'var(--color-forest-green)',
              color: 'var(--color-white)',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.9rem',
              fontWeight: 700,
              boxShadow: 'var(--shadow-sm)'
            }}
          >
            <User size={18} />
            <span>{t('nav.signIn')}</span>
          </button>
        )}
      </div>
    </aside>
  );
};
