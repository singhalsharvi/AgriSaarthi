import React from 'react';
import { Sparkles, Wheat } from 'lucide-react';

export const AgriSaarthiLogo = ({ compact = false, light = false }) => {
  const primary = light ? '#FFFFFF' : 'var(--color-forest-green-dark)';
  const secondary = light ? 'rgba(255, 255, 255, 0.78)' : 'var(--color-mitti-brown)';
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: compact ? '0.55rem' : '0.75rem' }}>
      <div style={{ width: compact ? '38px' : '48px', height: compact ? '38px' : '48px', borderRadius: compact ? '12px' : '15px', background: light ? 'linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.08))' : 'linear-gradient(145deg, var(--color-forest-green), #2D6A3F)', border: light ? '1px solid rgba(255,255,255,0.42)' : '1px solid rgba(18,54,31,0.2)', display: 'grid', placeItems: 'center', color: '#F7D46B', boxShadow: light ? '0 8px 18px rgba(0,0,0,0.18)' : '0 8px 18px rgba(27,77,46,0.2)', position: 'relative' }}>
        <Wheat size={compact ? 22 : 28} strokeWidth={2.4} />
        <Sparkles size={compact ? 10 : 12} strokeWidth={2.5} style={{ position: 'absolute', right: '4px', top: '4px', color: '#FFFFFF' }} />
      </div>
      <div>
        <div style={{ color: primary, fontWeight: 850, lineHeight: 1, fontSize: compact ? '1.1rem' : '1.45rem', letterSpacing: '-0.045em' }}>Agri<span style={{ color: light ? '#F7D46B' : 'var(--color-leaf-green)' }}>Saarthi</span></div>
        {!compact && <div style={{ color: secondary, fontSize: '0.66rem', fontWeight: 750, letterSpacing: '0.1em', textTransform: 'uppercase', marginTop: '0.34rem' }}>Your farm companion</div>}
      </div>
    </div>
  );
};
