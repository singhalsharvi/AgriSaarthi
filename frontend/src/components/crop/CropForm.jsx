import React, { useState } from 'react';
import { MapPin, Navigation, Sliders, Sparkles } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const CropForm = ({ onSubmit, isLoading }) => {
  const { t } = useLanguage();
  const [location, setLocation] = useState('Meerut, Uttar Pradesh');
  const [season, setSeason] = useState('Kharif');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [n, setN] = useState('90');
  const [p, setP] = useState('42');
  const [k, setK] = useState('43');
  const [ph, setPh] = useState('6.8');
  const [isLocating, setIsLocating] = useState(false);

  const handleUseLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        // Reverse geocoded mock location representation
        setLocation("Mandya, Karnataka");
        setIsLocating(false);
      },
      (err) => {
        setLocation("Meerut, Uttar Pradesh");
        setIsLocating(false);
      }
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      location,
      season,
      n,
      p,
      k,
      ph
    });
  };

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      borderRadius: 'var(--radius-lg)',
      border: '1.5px solid var(--color-cream-border)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      marginBottom: '2.5rem'
    }}>
      {/* Crop Field Header Banner */}
      <div style={{
        minHeight: '180px',
        background: `linear-gradient(to right, rgba(27, 77, 46, 0.9) 0%, rgba(27, 77, 46, 0.6) 100%), url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat`,
        padding: '2.25rem 2rem',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        justify: 'center'
      }}>
        <span style={{
          backgroundColor: 'rgba(255, 255, 255, 0.2)',
          backdropFilter: 'blur(4px)',
          color: 'var(--color-wheat-gold)',
          padding: '0.35rem 0.85rem',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.8rem',
          fontWeight: 700,
          width: 'fit-content',
          marginBottom: '0.5rem'
        }}>
          🌾 Smart Recommendation Engine
        </span>
        <h2 style={{ fontSize: '1.85rem', color: '#FFFFFF', margin: 0, fontWeight: 800 }}>
          {t('crop.title')}
        </h2>
        <p style={{ fontSize: '1rem', color: 'rgba(255, 255, 255, 0.9)', margin: 0, marginTop: '0.25rem' }}>
          {t('crop.subtitle')}
        </p>
      </div>

      {/* Form Area */}
      <form onSubmit={handleSubmit} style={{ padding: '2rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
          {/* Location Input */}
          <div className="form-group">
            <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <MapPin size={16} color="var(--color-forest-green)" />
              <span>{t('crop.locationLabel')}</span>
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                className="form-input"
                value={location}
                onChange={e => setLocation(e.target.value)}
                placeholder={t('crop.locationPlaceholder')}
                required
              />
              <button
                type="button"
                onClick={handleUseLocation}
                disabled={isLocating}
                style={{
                  whiteSpace: 'nowrap',
                  padding: '0.85rem 1rem',
                  backgroundColor: 'var(--color-cream-surface)',
                  border: '1.5px solid var(--color-cream-border)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--color-forest-green-dark)',
                  fontWeight: 700,
                  fontSize: '0.85rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.35rem'
                }}
              >
                <Navigation size={15} />
                <span>{isLocating ? 'Locating...' : t('crop.useMyLocation')}</span>
              </button>
            </div>
            <span style={{ fontSize: '0.78rem', color: 'var(--color-charcoal-muted)', marginTop: '0.25rem' }}>
              Village, City or District (e.g. Meerut, UP or Mandya, KA)
            </span>
          </div>

          {/* Season Selector Buttons */}
          <div className="form-group">
            <label className="form-label">
              {t('crop.seasonLabel')}
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem' }}>
              {['Kharif', 'Rabi', 'Zaid'].map(s => (
                <button
                  type="button"
                  key={s}
                  onClick={() => setSeason(s)}
                  style={{
                    padding: '0.85rem',
                    borderRadius: 'var(--radius-md)',
                    border: season === s ? '2px solid var(--color-forest-green)' : '1.5px solid var(--color-cream-border)',
                    backgroundColor: season === s ? 'var(--color-leaf-light)' : 'var(--color-white)',
                    color: season === s ? 'var(--color-forest-green-dark)' : 'var(--color-charcoal)',
                    fontWeight: season === s ? 800 : 600,
                    fontSize: '0.92rem',
                    textAlign: 'center',
                    transition: 'all 0.2s ease'
                  }}
                >
                  {s === 'Kharif' && '🌧️ Kharif'}
                  {s === 'Rabi' && '❄️ Rabi'}
                  {s === 'Zaid' && '☀️ Zaid'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Optional Advanced Soil Parameters Toggle */}
        <div style={{ marginBottom: '1.75rem' }}>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            style={{
              fontSize: '0.88rem',
              fontWeight: 700,
              color: 'var(--color-mitti-brown)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
          >
            <Sliders size={16} />
            <span>{showAdvanced ? 'Hide Optional Soil Parameters ▲' : 'Add Optional Soil Test Parameters (NPK / pH) ▼'}</span>
          </button>

          {showAdvanced && (
            <div style={{
              marginTop: '1rem',
              padding: '1.25rem',
              backgroundColor: 'var(--color-cream-surface)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-cream-border)',
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
              gap: '1rem'
            }}>
              <div>
                <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>Nitrogen (N)</label>
                <input type="number" className="form-input" value={n} onChange={e => setN(e.target.value)} placeholder="90" />
              </div>
              <div>
                <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>Phosphorus (P)</label>
                <input type="number" className="form-input" value={p} onChange={e => setP(e.target.value)} placeholder="42" />
              </div>
              <div>
                <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>Potassium (K)</label>
                <input type="number" className="form-input" value={k} onChange={e => setK(e.target.value)} placeholder="43" />
              </div>
              <div>
                <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>Soil pH</label>
                <input type="number" step="0.1" className="form-input" value={ph} onChange={e => setPh(e.target.value)} placeholder="6.8" />
              </div>
            </div>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '1.1rem',
            backgroundColor: 'var(--color-forest-green)',
            color: 'white',
            borderRadius: 'var(--radius-full)',
            fontWeight: 800,
            fontSize: '1.05rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.65rem',
            boxShadow: 'var(--shadow-md)'
          }}
        >
          <Sparkles size={20} color="var(--color-wheat-gold)" />
          <span>{isLoading ? 'ANALYZING FARM CONDITIONS...' : t('crop.analyzeBtn')}</span>
        </button>
      </form>
    </div>
  );
};
