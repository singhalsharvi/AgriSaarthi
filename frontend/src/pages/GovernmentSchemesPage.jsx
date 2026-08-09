import React, { useState } from 'react';
import { SchemeFilters } from '../components/schemes/SchemeFilters';
import { SchemeCard } from '../components/schemes/SchemeCard';
import { SchemeDetailModal } from '../components/schemes/SchemeDetailModal';
import { apiService } from '../api/client';
import { useLanguage } from '../context/LanguageContext';

export const GovernmentSchemesPage = () => {
  const { t } = useLanguage();
  const [isLoading, setIsLoading] = useState(false);
  const [schemes, setSchemes] = useState(null);
  const [selectedScheme, setSelectedScheme] = useState(null);

  const handleSearch = async (filters) => {
    setIsLoading(true);
    try {
      const res = await apiService.recommendSchemes(filters);
      setTimeout(() => {
        setSchemes(res);
        setIsLoading(false);
      }, 1500);
    } catch (err) {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <SchemeFilters onSearch={handleSearch} isLoading={isLoading} />

      {schemes && (
        <div style={{ marginBottom: '3.5rem' }} className="animate-fade-in">
          <div style={{
            backgroundColor: 'var(--color-white)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem 1.75rem',
            border: '1.5px solid var(--color-cream-border)',
            marginBottom: '1.75rem',
            boxShadow: 'var(--shadow-sm)'
          }}>
            <h3 style={{ fontSize: '1.4rem', color: 'var(--color-forest-green-dark)', margin: 0, fontWeight: 800 }}>
              {t('schemes.resultsTitle')} ({schemes.recommended_schemes?.length || 0})
            </h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--color-charcoal-muted)', margin: 0, marginTop: '0.2rem' }}>
              {schemes.ai_explanation}
            </p>
          </div>

          <div>
            {schemes.recommended_schemes?.map((item, idx) => (
              <SchemeCard
                key={idx}
                scheme={item}
                onViewDetails={setSelectedScheme}
              />
            ))}
          </div>
        </div>
      )}

      {selectedScheme && (
        <SchemeDetailModal
          scheme={selectedScheme}
          onClose={() => setSelectedScheme(null)}
        />
      )}
    </div>
  );
};
