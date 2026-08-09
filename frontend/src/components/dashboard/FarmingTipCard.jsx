import React from 'react';
import { Lightbulb, Calendar, CheckCircle } from 'lucide-react';

export const FarmingTipCard = () => {
  return (
    <div style={{
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      border: '1.5px solid var(--color-cream-border)',
      boxShadow: 'var(--shadow-sm)',
      backgroundColor: 'var(--color-white)',
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))'
    }}>
      {/* Left Photo */}
      <div style={{
        minHeight: '220px',
        background: `url('https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=800&q=80') center/cover no-repeat`,
        position: 'relative',
        padding: '1rem'
      }}>
        <span style={{
          backgroundColor: 'rgba(27, 77, 46, 0.85)',
          backdropFilter: 'blur(4px)',
          color: 'white',
          padding: '0.35rem 0.85rem',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.78rem',
          fontWeight: 700,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.35rem'
        }}>
          <Calendar size={14} /> Kharif Season Advisory
        </span>
      </div>

      {/* Right Content */}
      <div style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--color-mustard)' }}>
          <Lightbulb size={20} />
          <span style={{ fontSize: '0.82rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Daily Advisory
          </span>
        </div>

        <h3 style={{ fontSize: '1.25rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.75rem' }}>
          Today’s Farming Tip
        </h3>

        <p style={{ fontSize: '0.92rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.6, marginBottom: '1rem' }}>
          "During humid overcast days, inspect paddy field borders closely for early signs of leaf blast or stem borer. Ensure field drainage channels remain clear to prevent water stagnation around young root systems."
        </p>

        <div style={{ display: 'flex', gap: '1rem', fontSize: '0.8rem', color: 'var(--color-leaf-green)', fontWeight: 700 }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <CheckCircle size={14} /> Verified ICAR Guidance
          </span>
        </div>
      </div>
    </div>
  );
};
