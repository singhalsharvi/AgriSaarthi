import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const SchemeFilters = ({ onSearch, isLoading }) => {
  const { t } = useLanguage();
  const [location, setLocation] = useState('');
  const [annualIncome, setAnnualIncome] = useState('');
  const [gender, setGender] = useState('prefer_not_to_say');
  const [landholding, setLandholding] = useState('1.5');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({
      location: location.trim(),
      annualIncome,
      gender,
      landholding,
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
      {/* Banner */}
      <div style={{
        minHeight: '180px',
        background: `linear-gradient(to right, rgba(110, 71, 35, 0.9) 0%, rgba(110, 71, 35, 0.6) 100%), url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat`,
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
          🏛️ Direct Subsidies & Benefits
        </span>
        <h2 style={{ fontSize: '1.85rem', color: '#FFFFFF', margin: 0, fontWeight: 800 }}>
          {t('schemes.title')}
        </h2>
        <p style={{ fontSize: '1rem', color: 'rgba(255, 255, 255, 0.9)', margin: 0, marginTop: '0.25rem' }}>
          {t('schemes.subtitle')}
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{ padding: '2rem' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '1.25rem',
          marginBottom: '1.5rem'
        }}>
          <div>
            <label className="form-label">Farmer&apos;s Location</label>
            <input
              type="text"
              className="form-input"
              value={location}
              onChange={e => setLocation(e.target.value)}
              placeholder="Village/City, State (e.g. Meerut, Uttar Pradesh)"
              required
            />
          </div>

          <div>
            <label className="form-label">Annual Farmer Income (₹)</label>
            <input
              type="number"
              min="0"
              step="1"
              className="form-input"
              value={annualIncome}
              onChange={e => setAnnualIncome(e.target.value)}
              placeholder="e.g. 120000"
              required
            />
          </div>

          <div>
            <label className="form-label">Gender</label>
            <select className="form-select" value={gender} onChange={e => setGender(e.target.value)}>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="prefer_not_to_say">Prefer not to say</option>
            </select>
          </div>

          <div>
            <label className="form-label">Land Size (Hectares)</label>
            <input
              type="number"
              min="0"
              step="0.1"
              className="form-input"
              value={landholding}
              onChange={e => setLandholding(e.target.value)}
              placeholder="e.g. 1.5"
              required
            />
          </div>
        </div>

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
            fontSize: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
            boxShadow: 'var(--shadow-md)'
          }}
        >
          <Search size={20} />
          <span>{isLoading ? 'SEARCHING ELIGIBLE SCHEMES...' : t('schemes.findBtn')}</span>
        </button>
      </form>
    </div>
  );
};
