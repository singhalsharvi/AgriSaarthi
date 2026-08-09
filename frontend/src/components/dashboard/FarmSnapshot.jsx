import React from 'react';
import { MapPin, Calendar, Layers, Thermometer, Droplets, CloudRain } from 'lucide-react';

export const FarmSnapshot = ({ location = "Meerut, UP", season = "Kharif" }) => {
  const metrics = [
    { label: 'Location', value: location, icon: MapPin },
    { label: 'Planning Season', value: season, icon: Calendar },
    { label: 'Primary Soil', value: 'Alluvial Loam', icon: Layers },
    { label: 'Avg Temp', value: '28.5 °C', icon: Thermometer },
    { label: 'Air Humidity', value: '68%', icon: Droplets },
    { label: 'Est. Rainfall', value: '1050 mm', icon: CloudRain },
  ];

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      border: '1.5px solid var(--color-cream-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '1.75rem',
      boxShadow: 'var(--shadow-sm)',
      marginBottom: '2rem'
    }}>
      <h3 style={{ fontSize: '1.1rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
        📋 Farm Snapshot
      </h3>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
        gap: '1rem'
      }}>
        {metrics.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div
              key={idx}
              style={{
                backgroundColor: 'var(--color-cream-surface)',
                padding: '1rem',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-cream-border)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--color-mitti-brown)', marginBottom: '0.25rem' }}>
                <Icon size={16} />
                <span style={{ fontSize: '0.78rem', fontWeight: 600 }}>{m.label}</span>
              </div>
              <span style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-forest-green-dark)' }}>
                {m.value}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
