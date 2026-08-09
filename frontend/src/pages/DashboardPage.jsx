import React from 'react';
import { WeatherWidget } from '../components/dashboard/WeatherWidget';
import { FarmSnapshot } from '../components/dashboard/FarmSnapshot';
import { QuickActions } from '../components/dashboard/QuickActions';
import { FarmingTipCard } from '../components/dashboard/FarmingTipCard';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { Clock, MapPin } from 'lucide-react';

export const DashboardPage = ({ onNavigate }) => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const farmerName = user ? user.name : 'Farmer';
  const farmerLoc = user ? user.location : 'Meerut, Uttar Pradesh';

  const recentActivities = [
    { title: 'Crop Recommendation', desc: 'Rice (Paddy) recommended for Kharif season (92% match)', date: 'Today' },
    { title: 'Disease Detection', desc: 'Tomato leaf analyzed — possible Late Blight diagnosed', date: 'Yesterday' },
    { title: 'Government Scheme', desc: 'PM-KISAN eligibility criteria checked', date: '3 days ago' },
  ];

  return (
    <div className="page-container">
      {/* Header */}
      <div style={{
        backgroundColor: 'var(--color-white)',
        border: '1.5px solid var(--color-cream-border)',
        borderRadius: 'var(--radius-lg)',
        padding: '2rem',
        marginBottom: '2.5rem',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justify: 'space-between',
        gap: '1.5rem'
      }}>
        <div>
          <span className="badge-desi" style={{ marginBottom: '0.4rem' }}>
            📋 Digital Farm Notebook
          </span>
          <h1 style={{ fontSize: '2.2rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
            Namaste, {farmerName} 👋
          </h1>
          <p style={{ fontSize: '1.05rem', color: 'var(--color-charcoal-muted)', margin: 0, marginTop: '0.2rem' }}>
            {t('dashboard.subheading')}
          </p>
        </div>

        <div style={{
          backgroundColor: 'var(--color-cream-surface)',
          border: '1px solid var(--color-cream-border)',
          padding: '0.85rem 1.25rem',
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.65rem'
        }}>
          <MapPin size={20} color="var(--color-forest-green)" />
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-mitti-brown)', display: 'block' }}>
              CURRENT FARM LOCATION
            </span>
            <span style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--color-forest-green-dark)' }}>
              {farmerLoc}
            </span>
          </div>
        </div>
      </div>

      {/* Grid: Weather + Farm Snapshot */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: '2rem',
        marginBottom: '2.5rem'
      }}>
        <WeatherWidget location={farmerLoc} />
        <FarmSnapshot location={farmerLoc} season="Kharif" />
      </div>

      {/* Quick Actions */}
      <QuickActions onNavigate={onNavigate} />

      {/* Today's Farming Tip */}
      <div style={{ marginBottom: '2.5rem' }}>
        <FarmingTipCard />
      </div>

      {/* Recent Activity Feed */}
      <div style={{
        backgroundColor: 'var(--color-white)',
        border: '1.5px solid var(--color-cream-border)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.75rem',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <h3 style={{ fontSize: '1.15rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Clock size={18} color="var(--color-mitti-brown)" />
          <span>Recent Activity</span>
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {recentActivities.map((act, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                justify: 'space-between',
                padding: '0.85rem 1.1rem',
                backgroundColor: 'var(--color-cream-surface)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-cream-border)'
              }}
            >
              <div>
                <span style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--color-forest-green-dark)', display: 'block' }}>
                  {act.title}
                </span>
                <span style={{ fontSize: '0.85rem', color: 'var(--color-charcoal-muted)' }}>
                  {act.desc}
                </span>
              </div>
              <span style={{ fontSize: '0.78rem', color: 'var(--color-mitti-brown)', fontWeight: 600 }}>
                {act.date}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
