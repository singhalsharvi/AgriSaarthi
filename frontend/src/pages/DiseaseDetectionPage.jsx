import React, { useState } from 'react';
import { ImageUploader } from '../components/disease/ImageUploader';
import { ScannerState } from '../components/disease/ScannerState';
import { DiseaseResults } from '../components/disease/DiseaseResults';
import { apiService } from '../api/client';

export const DiseaseDetectionPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleAnalyze = async (formData) => {
    setIsLoading(true);
    setResults(null);
    setUploadedImage(formData.image);

    try {
      const res = await apiService.analyzeDisease(formData);
      setTimeout(() => {
        setResults(res);
        setIsLoading(false);
      }, 2200);
    } catch (err) {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <ImageUploader onAnalyze={handleAnalyze} isLoading={isLoading} />

      {isLoading && <ScannerState />}

      {results && !isLoading && (
        <DiseaseResults data={results} uploadedImage={uploadedImage} />
      )}
    </div>
  );
};
