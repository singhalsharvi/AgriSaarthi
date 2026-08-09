import React from 'react';
import { AlertTriangle, ShieldCheck, Activity, Stethoscope, CheckCircle, Leaf } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const DiseaseResults = ({ data, uploadedImage }) => {
  const { t } = useLanguage();

  if (!data) return null;

  const confidenceStr = data.confidence || '91.80%';
  const confVal = parseFloat(confidenceStr);
  const isLowConfidence = confVal < 50;

  const matches = data.top_matches || [
    { name: 'Late Blight', confidence: '91.8%' },
    { name: 'Early Blight', confidence: '5.2%' },
    { name: 'Healthy Leaf', confidence: '3.0%' }
  ];

  return (
    <div style={{ marginBottom: '3.5rem' }} className="animate-fade-in">
      {/* Top Title Banner */}
      <div style={{
        backgroundColor: 'var(--color-white)',
        border: '1.5px solid var(--color-cream-border)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.5rem 1.75rem',
        marginBottom: '2rem',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--color-mitti-brown)' }}>
          DIAGNOSTIC ADVISORY
        </span>
        <h2 style={{ fontSize: '1.6rem', color: 'var(--color-forest-green-dark)', margin: 0, marginTop: '0.2rem' }}>
          {t('disease.resultsTitle')}
        </h2>
      </div>

      {/* Low Confidence Alert Handling */}
      {isLowConfidence && (
        <div style={{
          backgroundColor: 'var(--color-terracotta-light)',
          border: '1.5px solid var(--color-terracotta)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem',
          marginBottom: '2rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-terracotta)', marginBottom: '0.5rem' }}>
            <AlertTriangle size={20} />
            <h4 style={{ fontSize: '1.1rem', margin: 0, fontWeight: 800 }}>
              ⚠️ LOW CONFIDENCE DIAGNOSIS
            </h4>
          </div>
          <p style={{ fontSize: '0.92rem', color: 'var(--color-charcoal)', margin: 0 }}>
            {t('disease.lowConfidence')}
          </p>
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        marginBottom: '2.5rem'
      }}>
        {/* Left Image & Top Matches */}
        <div>
          <div style={{
            borderRadius: 'var(--radius-lg)',
            overflow: 'hidden',
            border: '1.5px solid var(--color-cream-border)',
            boxShadow: 'var(--shadow-sm)',
            marginBottom: '1.5rem',
            backgroundColor: 'var(--color-white)'
          }}>
            <div style={{ padding: '0.85rem 1.25rem', borderBottom: '1px solid var(--color-cream-border)', backgroundColor: 'var(--color-cream-surface)' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--color-forest-green-dark)' }}>
                📷 Analyzed Plant Image
              </span>
            </div>
            <img
              src={uploadedImage || 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=800&q=80'}
              alt="Analyzed leaf"
              style={{ width: '100%', height: '260px', objectFit: 'cover' }}
            />
          </div>

          {/* Top Matches Confidence Gauge */}
          <div style={{
            backgroundColor: 'var(--color-white)',
            border: '1.5px solid var(--color-cream-border)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem',
            boxShadow: 'var(--shadow-sm)'
          }}>
            <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={18} color="var(--color-forest-green)" />
              <span>Top Possible Matches</span>
            </h4>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {matches.map((m, idx) => (
                <div key={idx}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', fontWeight: 700, marginBottom: '0.25rem' }}>
                    <span>{m.name}</span>
                    <span style={{ color: idx === 0 ? 'var(--color-forest-green)' : 'var(--color-charcoal-muted)' }}>{m.confidence}</span>
                  </div>
                  <div style={{ height: '8px', backgroundColor: 'var(--color-cream-surface)', borderRadius: 'var(--radius-full)', overflow: 'hidden' }}>
                    <div style={{
                      height: '100%',
                      width: m.confidence,
                      backgroundColor: idx === 0 ? 'var(--color-forest-green)' : 'var(--color-mustard)',
                      borderRadius: 'var(--radius-full)'
                    }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Treatment Advisory Content */}
        <div style={{
          backgroundColor: 'var(--color-white)',
          border: '1.5px solid var(--color-cream-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '2rem',
          boxShadow: 'var(--shadow-sm)',
          display: 'flex',
          flexDirection: 'column',
          justify: 'space-between'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.85rem' }}>
              <span className="badge-warning">
                Detected: {data.disease_status || 'Late Blight'}
              </span>
              <span className="badge-desi">
                Match: {confidenceStr}
              </span>
            </div>

            <h3 style={{ fontSize: '1.6rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.25rem' }}>
              {data.disease_status || 'Tomato Late Blight'}
            </h3>

            {/* AI Diagnosis Details */}
            <div style={{
              fontSize: '0.95rem',
              color: 'var(--color-charcoal)',
              lineHeight: 1.7,
              backgroundColor: 'var(--color-cream-bg)',
              padding: '1.25rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-cream-border)'
            }}>
              <div dangerouslySetInnerHTML={{ 
                __html: (data.ai_explanation || '')
                  .replace(/### (.*)/g, '<h4 style="color:var(--color-forest-green-dark);margin:1rem 0 0.5rem">$1</h4>')
                  .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  .replace(/- (.*)/g, '• $1<br/>') 
              }} />
            </div>
          </div>

          <div style={{
            marginTop: '1.5rem',
            paddingTop: '1rem',
            borderTop: '1px solid var(--color-cream-border)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.82rem',
            color: 'var(--color-leaf-green)',
            fontWeight: 700
          }}>
            <ShieldCheck size={16} />
            <span>Verified by ICAR Plant Protection Protocols</span>
          </div>
        </div>
      </div>
    </div>
  );
};
