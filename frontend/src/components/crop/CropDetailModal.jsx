import React from 'react';
import { X, CheckCircle, Droplets, Thermometer, Layers, Sprout } from 'lucide-react';

export const CropDetailModal = ({ crop, onClose }) => {
  if (!crop) return null;

  const details = crop.details || {
    n: "80-120 kg/ha",
    p: "40-60 kg/ha",
    k: "40-60 kg/ha",
    water: "Moderate to High",
    irrigation: "Canal or Tubewell flooding",
    image: "https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=800&q=80"
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(26, 28, 25, 0.7)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1.25rem'
    }} onClick={onClose}>
      <div style={{
        backgroundColor: 'var(--color-white)',
        borderRadius: 'var(--radius-lg)',
        width: '100%',
        maxWidth: '720px',
        maxHeight: '90vh',
        overflowY: 'auto',
        border: '1.5px solid var(--color-cream-border)',
        boxShadow: 'var(--shadow-lg)'
      }} onClick={e => e.stopPropagation()}>
        {/* Large Crop Image Header */}
        <div style={{
          height: '240px',
          background: `url('${details.image}') center/cover no-repeat`,
          position: 'relative',
          padding: '1.5rem',
          display: 'flex',
          justify: 'space-between',
          alignItems: 'flex-start'
        }}>
          <span style={{
            backgroundColor: 'var(--color-forest-green)',
            color: 'white',
            padding: '0.4rem 1rem',
            borderRadius: 'var(--radius-full)',
            fontWeight: 800,
            fontSize: '0.85rem'
          }}>
            {crop.confidence} Suitability
          </span>

          <button
            onClick={onClose}
            style={{
              padding: '0.5rem',
              borderRadius: '50%',
              backgroundColor: 'rgba(0, 0, 0, 0.6)',
              color: 'white'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '2rem' }}>
          <h2 style={{ fontSize: '1.85rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.5rem' }}>
            {crop.crop}
          </h2>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal-muted)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
            {crop.reason}
          </p>

          {/* Grid Breakdown */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.25rem',
            marginBottom: '1.75rem'
          }}>
            <div style={{ backgroundColor: 'var(--color-cream-surface)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>NUTRIENT NEEDS (NPK)</span>
              <p style={{ margin: '0.25rem 0 0', fontWeight: 800, color: 'var(--color-forest-green-dark)', fontSize: '0.95rem' }}>
                N: {details.n}<br />
                P: {details.p}<br />
                K: {details.k}
              </p>
            </div>

            <div style={{ backgroundColor: 'var(--color-cream-surface)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>WATER REQUIREMENT</span>
              <p style={{ margin: '0.25rem 0 0', fontWeight: 800, color: 'var(--color-forest-green-dark)', fontSize: '0.95rem' }}>
                {details.water}
              </p>
            </div>

            <div style={{ backgroundColor: 'var(--color-cream-surface)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>RECOMMENDED IRRIGATION</span>
              <p style={{ margin: '0.25rem 0 0', fontWeight: 800, color: 'var(--color-forest-green-dark)', fontSize: '0.95rem' }}>
                {details.irrigation}
              </p>
            </div>
          </div>

          {/* Action */}
          <button
            onClick={onClose}
            style={{
              width: '100%',
              padding: '0.85rem',
              backgroundColor: 'var(--color-forest-green)',
              color: 'white',
              borderRadius: 'var(--radius-full)',
              fontWeight: 700
            }}
          >
            Close Details
          </button>
        </div>
      </div>
    </div>
  );
};
