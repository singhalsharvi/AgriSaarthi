import React, { useState } from 'react';
import { ImageUploader } from '../components/disease/ImageUploader';
import { ScannerState } from '../components/disease/ScannerState';
import { DiseaseResults } from '../components/disease/DiseaseResults';
import { apiService } from '../api/client';

export const DiseaseDetectionPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async (formData) => {
    setIsLoading(true);
    setResults(null);
    setError('');
    setUploadedImage(formData.previewUrl);

    try {
      const res = await apiService.analyzeDisease(formData);
      setResults(res);
    } catch (err) {
      setError(err.message || 'Disease analysis could not be completed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <ImageUploader onAnalyze={handleAnalyze} isLoading={isLoading} />

      {isLoading && <ScannerState />}

      {error && !isLoading && (
        <div role="alert" style={{ marginBottom: '2rem', padding: '1rem 1.25rem', borderRadius: 'var(--radius-md)', background: 'var(--color-terracotta-light)', color: 'var(--color-terracotta)', border: '1px solid var(--color-terracotta)' }}>
          {error}
        </div>
      )}

      {results && !isLoading && (
        <DiseaseResults data={results} uploadedImage={uploadedImage} />
      )}
    </div>
  );
};
