import React, { useState } from 'react';
import { Lock, Mail, UserCheck, ShieldCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

export const SignInPage = ({ onNavigate }) => {
  const { signIn } = useAuth();
  const { t } = useLanguage();

  const [emailOrPhone, setEmailOrPhone] = useState('ramesh.farmer@agrisaarthi.in');
  const [password, setPassword] = useState('••••••••');
  const [rememberMe, setRememberMe] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    signIn({
      name: 'Ramesh Kumar',
      emailOrPhone,
      location: 'Meerut, Uttar Pradesh'
    });
    onNavigate('dashboard');
  };

  return (
    <div className="page-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '80vh' }}>
      <div style={{
        width: '100%',
        maxWidth: '960px',
        backgroundColor: 'var(--color-white)',
        borderRadius: 'var(--radius-lg)',
        border: '1.5px solid var(--color-cream-border)',
        boxShadow: 'var(--shadow-lg)',
        overflow: 'hidden',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))'
      }} className="desi-card">
        {/* Left Side — Real Indian Farm Photo */}
        <div style={{
          minHeight: '380px',
          background: `linear-gradient(to bottom, rgba(18, 54, 31, 0.7) 0%, rgba(18, 54, 31, 0.95) 100%), url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1000&q=80') center/cover no-repeat`,
          padding: '3rem 2.5rem',
          color: 'white',
          display: 'flex',
          flexDirection: 'column',
          justify: 'space-between'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1.5rem' }}>
              <span style={{ fontSize: '1.75rem' }}>🌾</span>
              <span style={{ fontSize: '1.5rem', fontWeight: 800 }}>AgriSaarthi</span>
            </div>
            <h2 style={{ fontSize: '2rem', color: '#FFFFFF', fontWeight: 800, lineHeight: 1.2, marginBottom: '0.85rem' }}>
              Welcome back to your Digital Farm Companion.
            </h2>
            <p style={{ fontSize: '0.95rem', color: 'rgba(255, 255, 255, 0.88)', lineHeight: 1.6 }}>
              Access saved crop recommendations, weather alerts, plant disease histories & government subsidies.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.82rem', color: 'var(--color-wheat-gold)', fontWeight: 700 }}>
            <ShieldCheck size={16} />
            <span>Secure & Trusted Indian Agriculture Platform</span>
          </div>
        </div>

        {/* Right Side — Login Form */}
        <div style={{ padding: '3rem 2.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h2 style={{ fontSize: '1.75rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.35rem', fontWeight: 800 }}>
            {t('signin.title')}
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--color-charcoal-muted)', marginBottom: '2rem' }}>
            {t('signin.subtitle')}
          </p>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">{t('signin.emailLabel')}</label>
              <div style={{ position: 'relative' }}>
                <input
                  type="text"
                  className="form-input"
                  value={emailOrPhone}
                  onChange={e => setEmailOrPhone(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: '1.5rem' }}>
              <label className="form-label">{t('signin.passwordLabel')}</label>
              <input
                type="password"
                className="form-input"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem', fontSize: '0.88rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--color-charcoal)' }}>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={e => setRememberMe(e.target.checked)}
                  style={{ width: '16px', height: '16px', accentColor: 'var(--color-forest-green)' }}
                />
                <span>{t('signin.rememberMe')}</span>
              </label>

              <span style={{ color: 'var(--color-forest-green)', fontWeight: 700, cursor: 'pointer' }}>
                Forgot Password?
              </span>
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '1.1rem',
                backgroundColor: 'var(--color-forest-green)',
                color: 'white',
                borderRadius: 'var(--radius-full)',
                fontWeight: 800,
                fontSize: '1rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                boxShadow: 'var(--shadow-md)',
                marginBottom: '1.25rem'
              }}
            >
              <UserCheck size={20} />
              <span>{t('signin.submit')}</span>
            </button>

            <div style={{ textAlign: 'center', fontSize: '0.9rem', color: 'var(--color-charcoal-muted)' }}>
              Don't have an account?{' '}
              <button
                type="button"
                onClick={handleSubmit}
                style={{ color: 'var(--color-forest-green)', fontWeight: 800 }}
              >
                {t('signin.createAccount')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
