import React from 'react';
import { Home, Sprout, Stethoscope, Landmark, LayoutDashboard } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';

export const MobileBottomNav = ({ activeTab, setActiveTab }) => {
  const { t } = useLanguage();
  const { user } = useAuth();

  const items = [
    { id: 'home', label: t('nav.home'), icon: Home },
    { id: 'crop', label: 'Crop', icon: Sprout, badge: '🌾' },
    { id: 'disease', label: 'Health', icon: Stethoscope, badge: '🌿' },
    { id: 'schemes', label: 'Schemes', icon: Landmark, badge: '🏛️' },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: '📋' },
  ];

  return (
    <nav style={{
      height: 'var(--bottom-nav-height)',
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      backgroundColor: 'var(--color-white)',
      borderTop: '1px solid var(--color-cream-border)',
      display: 'none',
      alignItems: 'center',
      justifyContent: 'space-around',
      zIndex: 50,
      boxShadow: '0 -2px 10px rgba(0,0,0,0.05)'
    }} className="mobile-bottom-nav">
      {items.map(item => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              flex: 1,
              height: '100%',
              color: isActive ? 'var(--color-forest-green)' : 'var(--color-charcoal-muted)',
              fontWeight: isActive ? 700 : 500,
              fontSize: '0.72rem',
              gap: '0.15rem'
            }}
          >
            {item.badge ? (
              <span style={{ fontSize: '1.1rem', lineHeight: 1 }}>{item.badge}</span>
            ) : (
              <Icon size={18} />
            )}
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};
