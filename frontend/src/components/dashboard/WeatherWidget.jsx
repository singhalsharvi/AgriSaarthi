import React from 'react';
import { CloudSun, Droplets, Wind, RefreshCw, Thermometer } from 'lucide-react';

export const WeatherWidget = ({ location = "Meerut, Uttar Pradesh" }) => {
  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      border: '1.5px solid var(--color-cream-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '1.75rem',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CloudSun size={24} color="var(--color-mustard)" />
          <h3 style={{ fontSize: '1.1rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
            Local Weather
          </h3>
        </div>
        <span style={{ fontSize: '0.78rem', color: 'var(--color-charcoal-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <RefreshCw size={12} /> Updated recently
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem', marginBottom: '1.25rem' }}>
        <span style={{ fontSize: '3rem', fontWeight: 800, color: 'var(--color-forest-green-dark)', lineHeight: 1 }}>
          28°C
        </span>
        <div>
          <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-charcoal)', display: 'block' }}>
            Partly Cloudy
          </span>
          <span style={{ fontSize: '0.85rem', color: 'var(--color-mitti-brown)' }}>
            📍 {location}
          </span>
        </div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '0.75rem',
        paddingTop: '1rem',
        borderTop: '1px solid var(--color-cream-border)'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Droplets size={18} color="var(--color-forest-green)" style={{ margin: '0 auto 0.25rem' }} />
          <span style={{ fontSize: '0.75rem', color: 'var(--color-charcoal-muted)', display: 'block' }}>Humidity</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>68%</span>
        </div>
        <div style={{ textAlign: 'center' }}>
          <Wind size={18} color="var(--color-forest-green)" style={{ margin: '0 auto 0.25rem' }} />
          <span style={{ fontSize: '0.75rem', color: 'var(--color-charcoal-muted)', display: 'block' }}>Precipitation</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>12 mm</span>
        </div>
        <div style={{ textAlign: 'center' }}>
          <Thermometer size={18} color="var(--color-forest-green)" style={{ margin: '0 auto 0.25rem' }} />
          <span style={{ fontSize: '0.75rem', color: 'var(--color-charcoal-muted)', display: 'block' }}>Soil Temp</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--color-charcoal)' }}>24°C</span>
        </div>
      </div>
    </div>
  );
};
