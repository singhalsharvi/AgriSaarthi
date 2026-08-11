import React, { useState } from 'react';
import { CheckCircle2, UserCheck, ShieldCheck, Sprout } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { AgriSaarthiLogo } from '../components/brand/AgriSaarthiLogo';

export const SignInPage = ({ onNavigate }) => {
  const { signIn } = useAuth();
  const { t } = useLanguage();

  const [emailOrPhone, setEmailOrPhone] = useState('');
  const [password, setPassword] = useState('••••••••');
  const [rememberMe, setRememberMe] = useState(true);

  const completeSignIn = async (profile) => {
    await signIn(profile);
    onNavigate('dashboard');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await completeSignIn({
      name: 'Ramesh Kumar',
      emailOrPhone,
      location: 'Meerut, Uttar Pradesh'
    });
  };

  const continueWithDemo = async () => {
    await completeSignIn({
      name: 'Asha Patil (Demo)',
      emailOrPhone: 'demo.farmer@agrisaarthi.local',
      location: 'Nashik, Maharashtra',
      landholding: '3.0 Acres',
      soilType: 'Black Soil',
      isDemo: true
    });
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
          minHeight: '500px',
          background: `linear-gradient(135deg, rgba(10, 43, 24, 0.96) 0%, rgba(18, 54, 31, 0.76) 47%, rgba(10, 35, 20, 0.34) 100%), url('https://images.unsplash.com/photo-1592982537447-6f2a6a0e5c9f?auto=format&fit=crop&w=1400&q=85') center/cover no-repeat`,
          padding: '3rem 2.5rem',
          color: 'white',
          display: 'flex',
          flexDirection: 'column',
          justify: 'space-between'
        }}>
          <div>
            <AgriSaarthiLogo light />
            <div style={{ marginTop: '2.25rem', display: 'inline-flex', alignItems: 'center', gap: '0.45rem', color: '#F7D46B', fontSize: '0.78rem', fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              <Sprout size={15} /> Smart support for every season
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

          <div style={{ background: '#F1F8E9', border: '1px solid #C5E1A5', borderRadius: 'var(--radius-md)', padding: '1rem', marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-forest-green-dark)', fontWeight: 800, marginBottom: '0.35rem' }}>
              <Sprout size={18} /> Try AgriSaarthi with demo farm data
            </div>
            <p style={{ margin: '0 0 0.75rem', fontSize: '0.82rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.45 }}>
              Explore the dashboard and onboarding with a sample Nashik farmer profile. No real account or backend record is created.
            </p>
            <button type="button" onClick={continueWithDemo} style={{ width: '100%', padding: '0.75rem', border: '1px solid var(--color-forest-green)', borderRadius: 'var(--radius-full)', color: 'var(--color-forest-green)', fontWeight: 800, background: 'white' }}>
              Continue with Demo Farm
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.6rem', marginTop: '2rem' }}>
            {['Crop advice', 'Plant health', 'Schemes'].map(item => (
              <div key={item} style={{ padding: '0.65rem 0.5rem', border: '1px solid rgba(255,255,255,0.18)', background: 'rgba(255,255,255,0.1)', borderRadius: '10px', backdropFilter: 'blur(4px)', fontSize: '0.72rem', fontWeight: 700, textAlign: 'center' }}>
                <CheckCircle2 size={13} style={{ display: 'block', margin: '0 auto 0.3rem', color: '#F7D46B' }} />
                {item}
              </div>
            ))}
          </div>

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
                onClick={() => completeSignIn({ name: 'New Farmer', emailOrPhone, location: 'India' })}
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
