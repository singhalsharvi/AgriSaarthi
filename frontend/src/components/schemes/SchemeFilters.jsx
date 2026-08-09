import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const SchemeFilters = ({ onSearch, isLoading }) => {
  const { t } = useLanguage();
  const [state, setState] = useState('Uttar Pradesh');
  const [crop, setCrop] = useState('Rice');
  const [landholding, setLandholding] = useState('1.5');
  const [category, setCategory] = useState('Small and marginal farmer families');

  const indianStates = [
    'Uttar Pradesh', 'Punjab', 'Haryana', 'Karnataka', 'Maharashtra', 
    'West Bengal', 'Madhya Pradesh', 'Bihar', 'Rajasthan', 'Tamil Nadu', 'Gujarat'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({
      state,
      crop,
      landholding,
      farmerCategory: category
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
            <label className="form-label">State</label>
            <select className="form-select" value={state} onChange={e => setState(e.target.value)}>
              {indianStates.map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="form-label">Crop Type</label>
            <input
              type="text"
              className="form-input"
              value={crop}
              onChange={e => setCrop(e.target.value)}
              placeholder="e.g. Rice, Wheat, Sugarcane"
            />
          </div>

          <div>
            <label className="form-label">Landholding (Acres/Ha)</label>
            <input
              type="number"
              step="0.1"
              className="form-input"
              value={landholding}
              onChange={e => setLandholding(e.target.value)}
              placeholder="e.g. 1.5"
            />
          </div>

          <div>
            <label className="form-label">Farmer Category</label>
            <select className="form-select" value={category} onChange={e => setCategory(e.target.value)}>
              <option value="Small and marginal farmer families">Small & Marginal (&lt;2 Ha)</option>
              <option value="Medium farmer">Medium Farmer (2-5 Ha)</option>
              <option value="Large landholding farmer">Large Landholding (&gt;5 Ha)</option>
              <option value="Tenant farmer / Sharecropper">Tenant Farmer / Sharecropper</option>
            </select>
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
