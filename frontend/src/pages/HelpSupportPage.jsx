import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Phone, MessageSquare } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const HelpSupportPage = () => {
  const { t } = useLanguage();
  const [openFaq, setOpenFaq] = useState(0);

  const faqs = [
    {
      q: 'How does Crop Recommendation work?',
      a: 'AgriSaarthi analyzes your district location, cropping season (Kharif, Rabi, Zaid), weather rainfall patterns, and soil parameters to recommend the top 3 crops with verified ICAR agricultural evidence.'
    },
    {
      q: 'How do I upload a plant image for disease detection?',
      a: 'Go to "Disease Detection", tap "Upload Plant Image" or "Take a Photo" using your smartphone camera. Select a clear, well-lit photo showing the affected leaves or lesions for accurate diagnosis.'
    },
    {
      q: 'How accurate is the disease detection feature?',
      a: 'Our disease detection system scans visual leaf symptoms against plant disease databases. If the confidence is below 50%, AgriSaarthi transparently alerts you with a Low Confidence warning.'
    },
    {
      q: 'How are government schemes selected for my farm?',
      a: 'Government schemes are matched based on your state, landholding size (Small/Marginal vs Large), crop selection, and farmer category. Direct links to official portals (PM-KISAN, PMFBY, KCC) are provided.'
    },
    {
      q: 'How can I change my application language?',
      a: 'Click "Choose Language" 🌐 at the bottom of the left sidebar or footer. You can switch between English, Hindi (हिन्दी), Bengali (বাংলা), Marathi (मराठी), and Kannada (ಕನ್ನಡ) anytime.'
    }
  ];

  return (
    <div className="page-container">
      {/* Header */}
      <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 3rem' }}>
        <span className="badge-desi" style={{ marginBottom: '0.5rem' }}>
          Help & Support
        </span>
        <h1 style={{ fontSize: '2.4rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
          {t('help.title')}
        </h1>
        <p style={{ fontSize: '1rem', color: 'var(--color-charcoal-muted)', marginTop: '0.5rem' }}>
          Find answers to common questions or reach out to Krishi helpline support.
        </p>
      </div>

      {/* Helpline Contact Card */}
      <div style={{
        backgroundColor: 'var(--color-leaf-light)',
        border: '1.5px solid var(--color-leaf-green)',
        borderRadius: 'var(--radius-lg)',
        padding: '2rem',
        marginBottom: '3rem',
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justify: 'space-between',
        gap: '1.5rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: '50%',
            backgroundColor: 'var(--color-forest-green)',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Phone size={24} />
          </div>
          <div>
            <h3 style={{ fontSize: '1.25rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
              Kisan Call Center (Toll-Free)
            </h3>
            <p style={{ fontSize: '0.95rem', color: 'var(--color-charcoal)', margin: 0, marginTop: '0.2rem' }}>
              Speak directly with official agricultural officers across India
            </p>
          </div>
        </div>

        <span style={{
          fontSize: '1.4rem',
          fontWeight: 800,
          color: 'var(--color-forest-green-dark)',
          backgroundColor: 'white',
          padding: '0.65rem 1.5rem',
          borderRadius: 'var(--radius-full)',
          border: '1px solid var(--color-leaf-green)'
        }}>
          📞 1800-180-1551
        </span>
      </div>

      {/* FAQ Accordion */}
      <div style={{ maxWidth: '800px', margin: '0 auto 3.5rem' }}>
        <h3 style={{ fontSize: '1.5rem', color: 'var(--color-forest-green-dark)', marginBottom: '1.5rem', fontWeight: 800 }}>
          {t('help.faqTitle')}
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div
                key={idx}
                style={{
                  backgroundColor: 'var(--color-white)',
                  border: '1.5px solid var(--color-cream-border)',
                  borderRadius: 'var(--radius-md)',
                  overflow: 'hidden',
                  boxShadow: 'var(--shadow-sm)'
                }}
              >
                <button
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  style={{
                    width: '100%',
                    padding: '1.25rem 1.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    justify: 'space-between',
                    textAlign: 'left',
                    fontWeight: 700,
                    fontSize: '1.05rem',
                    color: 'var(--color-forest-green-dark)'
                  }}
                >
                  <span>{faq.q}</span>
                  {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>

                {isOpen && (
                  <div style={{
                    padding: '0 1.5rem 1.25rem',
                    fontSize: '0.95rem',
                    color: 'var(--color-charcoal-muted)',
                    lineHeight: 1.6,
                    borderTop: '1px solid var(--color-cream-surface)'
                  }}>
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
