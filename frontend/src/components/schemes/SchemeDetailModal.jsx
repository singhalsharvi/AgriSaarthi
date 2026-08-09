import React from 'react';
import { X, ExternalLink, FileText, CheckCircle2 } from 'lucide-react';

export const SchemeDetailModal = ({ scheme, onClose }) => {
  if (!scheme) return null;

  const docs = scheme.documents || [
    'Aadhaar Card of Farmer',
    'Khatauni / Landholding Revenue Record',
    'Bank Passbook with IFSC Code',
    'Active Mobile Number linked to Aadhaar'
  ];

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
        maxWidth: '740px',
        maxHeight: '90vh',
        overflowY: 'auto',
        border: '1.5px solid var(--color-cream-border)',
        boxShadow: 'var(--shadow-lg)',
        padding: '2.5rem'
      }} onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{
          display: 'flex',
          alignItems: 'flex-start',
          justify: 'space-between',
          marginBottom: '1.5rem',
          paddingBottom: '1rem',
          borderBottom: '1px solid var(--color-cream-border)'
        }}>
          <div>
            <span className="badge-desi" style={{ marginBottom: '0.5rem' }}>
              🏛️ Government Scheme Overview
            </span>
            <h2 style={{ fontSize: '1.75rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
              {scheme.scheme_name}
            </h2>
          </div>

          <button
            onClick={onClose}
            style={{
              padding: '0.5rem',
              borderRadius: '50%',
              backgroundColor: 'var(--color-cream-surface)',
              color: 'var(--color-charcoal)'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Content Breakdown */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.4rem' }}>
              📌 Overview & Purpose
            </h4>
            <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.6, margin: 0 }}>
              {scheme.snippet}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.4rem' }}>
              🎁 Scheme Benefits
            </h4>
            <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.6, margin: 0 }}>
              {scheme.benefits || 'Financial cash transfers, credit subsidy or risk protection benefits.'}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.4rem' }}>
              🎯 Farmer Eligibility Criteria
            </h4>
            <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', lineHeight: 1.6, margin: 0 }}>
              {scheme.eligibility || 'Small and marginal farmers holding cultivable land records.'}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '1.05rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.65rem' }}>
              📄 Required Documents
            </h4>
            <div style={{
              backgroundColor: 'var(--color-cream-surface)',
              padding: '1.25rem',
              borderRadius: 'var(--radius-md)',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.65rem'
            }}>
              {docs.map((doc, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem', color: 'var(--color-charcoal)' }}>
                  <CheckCircle2 size={16} color="var(--color-forest-green)" />
                  <span>{doc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div style={{
          marginTop: '2rem',
          paddingTop: '1.25rem',
          borderTop: '1px solid var(--color-cream-border)',
          display: 'flex',
          justify: 'space-between',
          alignItems: 'center'
        }}>
          {scheme.official_website ? (
            <a
              href={scheme.official_website}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary"
            >
              <span>Apply / Official Portal</span>
              <ExternalLink size={18} />
            </a>
          ) : <div />}

          <button onClick={onClose} className="btn-secondary">
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
