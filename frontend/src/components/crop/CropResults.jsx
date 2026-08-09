import React, { useState } from 'react';
import { AlertTriangle, CheckCircle, Info, Sparkles, Droplets, Thermometer, ArrowRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { CropDetailModal } from './CropDetailModal';

export const CropResults = ({ data }) => {
  const { t } = useLanguage();
  const [selectedCrop, setSelectedCrop] = useState(null);

  if (!data) return null;

  const confidenceValue = parseFloat(data.ml_confidence || '0');
  const isLowConfidence = confidenceValue < 50;

  return (
    <div style={{ marginBottom: '3.5rem' }} className="animate-fade-in">
      {/* Top Banner Context */}
      <div style={{
        backgroundColor: 'var(--color-white)',
        border: '1.5px solid var(--color-cream-border)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.5rem 1.75rem',
        marginBottom: '2rem',
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justify: 'space-between',
        gap: '1rem',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <div>
          <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>
            ANALYSIS REPORT
          </span>
          <h2 style={{ fontSize: '1.5rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
            {t('crop.resultsTitle')}
          </h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--color-charcoal-muted)', margin: 0, marginTop: '0.2rem' }}>
            📍 {data.location} | 🗓️ Season: <strong>{data.season}</strong> | 🪴 Soil: <strong>{data.soil}</strong>
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <span className="badge-desi">
            🌡️ {data.weather?.temperature || 28}°C
          </span>
          <span className="badge-desi">
            💧 {data.weather?.humidity || 68}% Humidity
          </span>
          <span className="badge-mustard">
            Confidence: {data.ml_confidence}
          </span>
        </div>
      </div>

      {/* Low Confidence Alert Handling */}
      {isLowConfidence ? (
        <div style={{
          backgroundColor: 'var(--color-terracotta-light)',
          border: '1.5px solid var(--color-terracotta)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.75rem',
          marginBottom: '2rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem', color: 'var(--color-terracotta)' }}>
            <AlertTriangle size={22} />
            <h3 style={{ fontSize: '1.15rem', margin: 0, fontWeight: 800 }}>
              ⚠️ {t('crop.lowConfidence')}
            </h3>
          </div>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', marginBottom: '1rem' }}>
            {t('crop.lowConfidenceText')} We recommend double checking your soil testing parameters or speaking directly with your local Krishi Vigyan Kendra (KVK) officer.
          </p>
          <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.75rem' }}>
            {t('crop.kbTitle')}
          </h4>
        </div>
      ) : null}

      {/* Top 3 Crop Recommendation Cards */}
      <h3 style={{ fontSize: '1.3rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
        🥇 {t('crop.top3')}
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {data.recommended_crops?.map((item, idx) => {
          const isTopMatch = idx === 0;
          return (
            <div
              key={idx}
              style={{
                backgroundColor: 'var(--color-white)',
                borderRadius: 'var(--radius-lg)',
                border: isTopMatch ? '2px solid var(--color-forest-green)' : '1.5px solid var(--color-cream-border)',
                boxShadow: isTopMatch ? 'var(--shadow-md)' : 'var(--shadow-sm)',
                overflow: 'hidden',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))'
              }}
              className="desi-card"
            >
              {/* Left Photo & Badges */}
              <div style={{
                minHeight: '220px',
                background: `url('${item.details?.image || 'https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=800&q=80'}') center/cover no-repeat`,
                position: 'relative',
                padding: '1.25rem',
                display: 'flex',
                flexDirection: 'column',
                justify: 'space-between'
              }}>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <span style={{
                    backgroundColor: isTopMatch ? 'var(--color-forest-green)' : 'var(--color-mitti-brown)',
                    color: 'white',
                    padding: '0.4rem 0.85rem',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '0.8rem',
                    fontWeight: 800
                  }}>
                    #{idx + 1} Recommendation
                  </span>
                  <span style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    color: 'var(--color-forest-green-dark)',
                    padding: '0.4rem 0.85rem',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '0.8rem',
                    fontWeight: 800
                  }}>
                    {item.confidence} Match
                  </span>
                </div>

                <div style={{
                  backgroundColor: 'rgba(26, 28, 25, 0.8)',
                  backdropFilter: 'blur(4px)',
                  color: 'white',
                  padding: '0.65rem 0.85rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.8rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <CheckCircle size={15} color="var(--color-wheat-gold)" />
                  <span>Suitable Season, Soil & Climate Match</span>
                </div>
              </div>

              {/* Right Content */}
              <div style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <h4 style={{ fontSize: '1.5rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
                      {item.crop}
                    </h4>
                    <span style={{ fontSize: '0.78rem', color: 'var(--color-mitti-brown)', backgroundColor: 'var(--color-cream-surface)', padding: '0.2rem 0.6rem', borderRadius: '4px', fontWeight: 600 }}>
                      Source: {item.source}
                    </span>
                  </div>

                  <p style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.35rem' }}>
                    {t('crop.whyThisCrop')}
                  </p>
                  <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                    {item.reason}
                  </p>
                </div>

                <button
                  onClick={() => setSelectedCrop(item)}
                  style={{
                    backgroundColor: isTopMatch ? 'var(--color-forest-green)' : 'var(--color-cream-surface)',
                    color: isTopMatch ? 'white' : 'var(--color-forest-green-dark)',
                    border: isTopMatch ? 'none' : '1.5px solid var(--color-cream-border)',
                    padding: '0.85rem 1.5rem',
                    borderRadius: 'var(--radius-full)',
                    fontWeight: 700,
                    fontSize: '0.9rem',
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.2s ease',
                    width: 'fit-content'
                  }}
                >
                  <span>{t('crop.viewDetails')}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* AI Agricultural Advisory Summary */}
      {data.explanation && (
        <div style={{
          marginTop: '2.5rem',
          backgroundColor: 'var(--color-cream-surface)',
          border: '1.5px solid var(--color-cream-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.75rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem', color: 'var(--color-forest-green-dark)' }}>
            <Sparkles size={20} color="var(--color-mustard)" />
            <h4 style={{ fontSize: '1.15rem', margin: 0, fontWeight: 800 }}>
              🌾 ICAR Expert Summary & Advice
            </h4>
          </div>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.7, margin: 0 }}>
            {data.explanation}
          </p>
        </div>
      )}

      {/* Detailed Modal */}
      {selectedCrop && (
        <CropDetailModal crop={selectedCrop} onClose={() => setSelectedCrop(null)} />
      )}
    </div>
  );
};
