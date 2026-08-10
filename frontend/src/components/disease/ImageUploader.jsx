import React, { useState, useRef } from 'react';
import { Camera, Upload, Image as ImageIcon, X } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const ImageUploader = ({ onAnalyze, isLoading }) => {
  const { t } = useLanguage();
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [uploadError, setUploadError] = useState('');
  // Do not pre-fill a crop or symptoms: those values can make a user believe
  // the diagnosis was supplied by the model when it was only a default.
  const [cropName, setCropName] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      setUploadError('Please select a JPG, PNG, or WEBP image.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setUploadError('Please select an image smaller than 10 MB.');
      return;
    }
    setUploadError('');
    setImageFile(file);
    const reader = new FileReader();
    reader.onloadend = () => setSelectedImage(reader.result);
    reader.readAsDataURL(file);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!imageFile) {
      setUploadError('Upload a clear plant-leaf image before starting analysis.');
      return;
    }
    onAnalyze({
      cropName,
      symptoms,
      imageFile,
      previewUrl: selectedImage
    });
  };

  return (
    <div style={{
      backgroundColor: 'var(--color-white)',
      borderRadius: 'var(--radius-lg)',
      border: '1.5px solid var(--color-cream-border)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      marginBottom: '2.5rem'
    }}>
      {/* Plant Health Header Banner */}
      <div style={{
        minHeight: '180px',
        background: `linear-gradient(to right, rgba(18, 54, 31, 0.9) 0%, rgba(18, 54, 31, 0.6) 100%), url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat`,
        padding: '2.25rem 2rem',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        justify: 'center'
      }}>
        <span style={{
          backgroundColor: 'rgba(255, 255, 255, 0.2)',
          backdropFilter: 'blur(4px)',
          color: 'var(--color-wheat-gold)',
          padding: '0.35rem 0.85rem',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.8rem',
          fontWeight: 700,
          width: 'fit-content',
          marginBottom: '0.5rem'
        }}>
          🌿 Visual Crop Diagnostics
        </span>
        <h2 style={{ fontSize: '1.85rem', color: '#FFFFFF', margin: 0, fontWeight: 800 }}>
          {t('disease.title')}
        </h2>
        <p style={{ fontSize: '1rem', color: 'rgba(255, 255, 255, 0.9)', margin: 0, marginTop: '0.25rem' }}>
          {t('disease.subtitle')}
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{ padding: '2rem' }}>
        {/* Upload Dropzone */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label className="form-label" style={{ marginBottom: '0.5rem', display: 'block' }}>
            📷 {t('disease.uploadArea')}
          </label>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/png, image/jpeg, image/jpg"
            style={{ display: 'none' }}
          />

          <input
            type="file"
            ref={cameraInputRef}
            onChange={handleFileChange}
            accept="image/*"
            capture="environment"
            style={{ display: 'none' }}
          />

          {selectedImage ? (
            <div style={{
              position: 'relative',
              borderRadius: 'var(--radius-md)',
              overflow: 'hidden',
              maxHeight: '320px',
              border: '2px solid var(--color-leaf-green)'
            }}>
              <img src={selectedImage} alt="Uploaded leaf" style={{ width: '100%', height: '320px', objectFit: 'cover' }} />
              <button
                type="button"
                onClick={() => {
                  setSelectedImage(null);
                  setImageFile(null);
                  setUploadError('');
                  if (fileInputRef.current) fileInputRef.current.value = '';
                  if (cameraInputRef.current) cameraInputRef.current.value = '';
                }}
                style={{
                  position: 'absolute',
                  top: '0.75rem',
                  right: '0.75rem',
                  backgroundColor: 'rgba(0,0,0,0.7)',
                  color: 'white',
                  padding: '0.5rem',
                  borderRadius: '50%'
                }}
              >
                <X size={18} />
              </button>
            </div>
          ) : (
            <div
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: '2.5px dashed var(--color-cream-border)',
                borderRadius: 'var(--radius-lg)',
                padding: '3rem 1.5rem',
                textAlign: 'center',
                backgroundColor: 'var(--color-cream-surface)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                backgroundColor: 'var(--color-white)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                color: 'var(--color-forest-green)',
                boxShadow: 'var(--shadow-sm)'
              }}>
                <Upload size={28} />
              </div>

              <h4 style={{ fontSize: '1.1rem', color: 'var(--color-forest-green-dark)', marginBottom: '0.35rem' }}>
                {t('disease.dragDrop')}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-charcoal-muted)', margin: 0 }}>
                Supported Formats: JPG, JPEG, PNG (Mobile camera supported)
              </p>
            </div>
          )}
          {uploadError && (
            <p role="alert" style={{ color: 'var(--color-terracotta)', margin: '0.6rem 0 0', fontSize: '0.9rem' }}>
              {uploadError}
            </p>
          )}
        </div>

        {/* Crop Name & Symptoms Text */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem', marginBottom: '1.75rem' }}>
          <div>
            <label className="form-label">Crop Name (Optional)</label>
            <input
              type="text"
              className="form-input"
              value={cropName}
              onChange={e => setCropName(e.target.value)}
              placeholder="e.g. Tomato, Wheat, Rice"
            />
          </div>

          <div>
            <label className="form-label">Observed Symptoms (Optional)</label>
            <input
              type="text"
              className="form-input"
              value={symptoms}
              onChange={e => setSymptoms(e.target.value)}
              placeholder="e.g. Yellowing leaf edges, dark spots"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button
            type="submit"
            disabled={isLoading}
            style={{
              flex: 1,
              minWidth: '200px',
              padding: '1.1rem',
              backgroundColor: 'var(--color-forest-green)',
              color: 'white',
              borderRadius: 'var(--radius-full)',
              fontWeight: 800,
              fontSize: '1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              boxShadow: 'var(--shadow-md)'
            }}
          >
            <ImageIcon size={20} />
            <span>{isLoading ? 'ANALYZING PLANT...' : t('disease.analyzeBtn')}</span>
          </button>

          <button
            type="button"
            onClick={() => cameraInputRef.current?.click()}
            style={{
              padding: '1.1rem 1.75rem',
              backgroundColor: 'var(--color-cream-surface)',
              border: '1.5px solid var(--color-cream-border)',
              borderRadius: 'var(--radius-full)',
              color: 'var(--color-mitti-brown)',
              fontWeight: 700,
              fontSize: '0.95rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Camera size={20} />
            <span>{t('disease.takePhoto')}</span>
          </button>
        </div>
      </form>
    </div>
  );
};
