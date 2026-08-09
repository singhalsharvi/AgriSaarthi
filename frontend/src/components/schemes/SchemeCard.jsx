import React from 'react';
import { ExternalLink, CheckCircle, FileText, ArrowRight, Shield } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const SchemeCard = ({ scheme, onViewDetails }) => {
  const { t } = useLanguage();

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      border: '1.5px solid var(--color-cream-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '2rem',
      boxShadow: 'var(--shadow-sm)',
      marginBottom: '1.5rem',
      display: 'flex',
      flexDirection: 'column',
      justify: 'space-between',
      position: 'relative'
    }} className="desi-card">
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <span style={{
            backgroundColor: 'var(--color-leaf-light)',
            color: 'var(--color-forest-green-dark)',
            padding: '0.35rem 0.85rem',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.78rem',
            fontWeight: 800,
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem'
          }}>
            <Shield size={14} /> Highly Relevant Scheme
          </span>

          <span style={{ fontSize: '0.78rem', color: 'var(--color-mitti-brown)', fontWeight: 600 }}>
            Source: {scheme.source_file || 'Ministry of Agriculture'}
          </span>
        </div>

        <h3 style={{ fontSize: '1.4rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.85rem', fontWeight: 800 }}>
          {scheme.scheme_name}
        </h3>

        <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
          {scheme.snippet}
        </p>

        {/* Benefits & Eligibility Summary */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '1rem',
          backgroundColor: 'var(--color-cream-surface)',
          padding: '1.1rem',
          borderRadius: 'var(--radius-md)',
          marginBottom: '1.5rem'
        }}>
          <div>
            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              🎁 Key Benefits
            </span>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.88rem', color: 'var(--color-charcoal)', fontWeight: 600 }}>
              {scheme.benefits || 'Financial cash transfers & input subsidies directly to bank account.'}
            </p>
          </div>

          <div>
            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--color-mitti-brown)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              📋 Eligibility Criteria
            </span>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.88rem', color: 'var(--color-charcoal)', fontWeight: 600 }}>
              {scheme.eligibility || 'Small and marginal farmers holding registered cultivable land.'}
            </p>
          </div>
        </div>
      </div>

      <div style={{
        display: 'flex',
        alignItems: 'center',
        justify: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        paddingTop: '1rem',
        borderTop: '1px solid var(--color-cream-border)'
      }}>
        <button
          onClick={() => onViewDetails(scheme)}
          style={{
            backgroundColor: 'var(--color-forest-green)',
            color: 'white',
            padding: '0.75rem 1.5rem',
            borderRadius: 'var(--radius-full)',
            fontWeight: 700,
            fontSize: '0.9rem',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <span>{t('schemes.viewDetails')}</span>
        </button>

        {scheme.official_website && (
          <a
            href={scheme.official_website}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              color: 'var(--color-mitti-brown)',
              fontWeight: 700,
              fontSize: '0.88rem'
            }}
          >
            <span>Official Portal</span>
            <ExternalLink size={15} />
          </a>
        )}
      </div>
    </div>
  );
};
