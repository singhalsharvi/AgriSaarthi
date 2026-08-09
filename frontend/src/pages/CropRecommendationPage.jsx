import React, { useState } from 'react';
import { CropForm } from '../components/crop/CropForm';
import { CropAnalysisState } from '../components/crop/CropAnalysisState';
import { CropResults } from '../components/crop/CropResults';
import { apiService } from '../api/client';

export const CropRecommendationPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (formData) => {
    setIsLoading(true);
    setResults(null);
    setError(null);

    try {
      // Execute analysis API call
      const res = await apiService.recommendCrop(formData);
      // Give realistic step feel
      setTimeout(() => {
        setResults(res);
        setIsLoading(false);
      }, 2500);
    } catch (err) {
      setError("Unable to process crop analysis right now. Please try again.");
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      {/* Input Form */}
      <CropForm onSubmit={handleAnalyze} isLoading={isLoading} />

      {/* Loading Step Animation */}
      {isLoading && <CropAnalysisState />}

      {/* Error Handling */}
      {error && (
        <div style={{
          backgroundColor: 'var(--color-terracotta-light)',
          border: '1.5px solid var(--color-terracotta)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem',
          color: 'var(--color-terracotta)',
          marginBottom: '2rem'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* Output Results */}
      {results && !isLoading && <CropResults data={results} />}
    </div>
  );
};
