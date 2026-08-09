import React from 'react';
import { ArrowRight, Sprout, Stethoscope, Landmark } from 'lucide-react';

export const FeaturesPage = ({ onNavigate }) => {
  const featureEditorial = [
    {
      id: 'crop',
      title: 'Know What To Grow',
      subtitle: 'Crop Recommendation System',
      text: 'Get tailored recommendations based on your local village, season, weather patterns and soil parameters. Designed to minimize climate risk and optimize seasonal yield.',
      image: 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=1200&q=80',
      cta: 'Get Crop Recommendation →',
      icon: '🌾'
    },
    {
      id: 'disease',
      title: "Know Your Crop’s Health",
      subtitle: 'Plant Disease Detection',
      text: 'Upload a plant leaf photo and diagnose possible fungal, bacterial or pest infections. Get step-by-step ICAR verified organic and chemical treatment advice.',
      image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=1200&q=80',
      cta: 'Check Plant Health →',
      icon: '🌿'
    },
    {
      id: 'schemes',
      title: 'Know Your Benefits',
      subtitle: 'Government Subsidies & Schemes',
      text: 'Discover central and state government schemes relevant to your landholding and crop choices. Includes eligibility criteria, document checklists & direct links.',
      image: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1200&q=80',
      cta: 'Find Schemes →',
      icon: '🏛️'
    }
  ];

  return (
    <div className="page-container">
      {/* Header */}
      <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 3rem' }}>
        <span className="badge-desi" style={{ marginBottom: '0.5rem' }}>
          AgriSaarthi Tools
        </span>
        <h1 style={{ fontSize: '2.4rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
          Tools Built Around Your Farm
        </h1>
        <p style={{ fontSize: '1.05rem', color: 'var(--color-charcoal-muted)', marginTop: '0.5rem' }}>
          Empowering real Indian farmers with science-backed recommendations, instant plant diagnosis & transparent government support.
        </p>
      </div>

      {/* 3 Editorial Layout Sections */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem', marginBottom: '3.5rem' }}>
        {featureEditorial.map((item, idx) => {
          const isEven = idx % 2 === 0;
          return (
            <div
              key={item.id}
              style={{
                backgroundColor: 'var(--color-white)',
                borderRadius: 'var(--radius-lg)',
                border: '1.5px solid var(--color-cream-border)',
                boxShadow: 'var(--shadow-sm)',
                overflow: 'hidden',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))'
              }}
              className="desi-card"
            >
              {/* Image Side */}
              <div style={{
                order: isEven ? 1 : 2,
                minHeight: '340px',
                background: `url('${item.image}') center/cover no-repeat`,
                position: 'relative'
              }} />

              {/* Text Side */}
              <div style={{
                order: isEven ? 2 : 1,
                padding: '3rem 2.5rem',
                display: 'flex',
                flexDirection: 'column',
                justify: 'center'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                  <span style={{ fontSize: '1.5rem' }}>{item.icon}</span>
                  <span style={{ fontSize: '0.85rem', fontWeight: 800, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    {item.subtitle}
                  </span>
                </div>

                <h2 style={{ fontSize: '2.1rem', color: 'var(--color-forest-green-dark)', marginBottom: '1rem', fontWeight: 800 }}>
                  {item.title}
                </h2>

                <p style={{ fontSize: '1.05rem', color: 'var(--color-charcoal-muted)', lineHeight: 1.6, marginBottom: '2rem' }}>
                  {item.text}
                </p>

                <div>
                  <button
                    onClick={() => onNavigate(item.id)}
                    style={{
                      backgroundColor: 'var(--color-forest-green)',
                      color: 'white',
                      padding: '0.9rem 2rem',
                      borderRadius: 'var(--radius-full)',
                      fontWeight: 700,
                      fontSize: '0.95rem',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      boxShadow: 'var(--shadow-sm)'
                    }}
                  >
                    <span>{item.cta}</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
