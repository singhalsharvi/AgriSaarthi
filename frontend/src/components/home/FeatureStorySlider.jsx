import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const FeatureStorySlider = ({ onSelectFeature }) => {
  const { t } = useLanguage();
  const [currentIndex, setCurrentIndex] = useState(0);

  const slides = [
    {
      id: 'crop',
      badge: '🌾 CROP SELECTION',
      title: t('slider.slide1.title'),
      text: t('slider.slide1.text'),
      cta: t('slider.slide1.cta'),
      image: 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=1200&q=80',
      farmerTag: 'Paddy & Wheat Fields, Punjab'
    },
    {
      id: 'features',
      badge: '🚜 MODERN FARMING',
      title: t('slider.slide2.title'),
      text: t('slider.slide2.text'),
      cta: t('slider.slide2.cta'),
      image: 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=1200&q=80',
      farmerTag: 'Mechanized Tillage, Haryana'
    },
    {
      id: 'disease',
      badge: '🌿 PLANT PROTECTION',
      title: t('slider.slide3.title'),
      text: t('slider.slide3.text'),
      cta: t('slider.slide3.cta'),
      image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=1200&q=80',
      farmerTag: 'Vegetable Crop Inspection, Maharashtra'
    },
    {
      id: 'schemes',
      badge: '🏛️ GOVERNMENT BENEFIT',
      title: t('slider.slide4.title'),
      text: t('slider.slide4.text'),
      cta: t('slider.slide4.cta'),
      image: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1200&q=80',
      farmerTag: 'Krishi Kendra Support, Madhya Pradesh'
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex(prev => (prev + 1) % slides.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [slides.length]);

  const prevSlide = () => setCurrentIndex((currentIndex - 1 + slides.length) % slides.length);
  const nextSlide = () => setCurrentIndex((currentIndex + 1) % slides.length);

  const slide = slides[currentIndex];

  return (
    <div style={{ marginBottom: '4rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', color: 'var(--color-forest-green-dark)', margin: 0 }}>
            Agricultural Storytelling
          </h2>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-mitti-brown)', margin: 0 }}>
            Discover how AgriSaarthi transforms daily farm decisions across India
          </p>
        </div>

        {/* Carousel Controls */}
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={prevSlide}
            style={{
              padding: '0.65rem',
              borderRadius: '50%',
              backgroundColor: 'var(--color-white)',
              border: '1.5px solid var(--color-cream-border)',
              color: 'var(--color-forest-green)',
              boxShadow: 'var(--shadow-sm)'
            }}
          >
            <ChevronLeft size={20} />
          </button>
          <button
            onClick={nextSlide}
            style={{
              padding: '0.65rem',
              borderRadius: '50%',
              backgroundColor: 'var(--color-white)',
              border: '1.5px solid var(--color-cream-border)',
              color: 'var(--color-forest-green)',
              boxShadow: 'var(--shadow-sm)'
            }}
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>

      {/* Main Slide Card */}
      <div style={{
        position: 'relative',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        border: '1.5px solid var(--color-cream-border)',
        boxShadow: 'var(--shadow-md)',
        minHeight: '380px',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        backgroundColor: 'var(--color-white)'
      }}>
        {/* Left Story Content */}
        <div style={{
          padding: '3rem 2.5rem',
          display: 'flex',
          flexDirection: 'column',
          justify: 'center'
        }}>
          <span style={{
            display: 'inline-block',
            fontSize: '0.82rem',
            fontWeight: 700,
            color: 'var(--color-forest-green)',
            backgroundColor: 'var(--color-leaf-light)',
            padding: '0.4rem 0.85rem',
            borderRadius: 'var(--radius-full)',
            width: 'fit-content',
            marginBottom: '1rem'
          }}>
            {slide.badge}
          </span>

          <h3 style={{
            fontSize: '2rem',
            color: 'var(--color-forest-green-dark)',
            marginBottom: '0.85rem',
            lineHeight: 1.2
          }}>
            {slide.title}
          </h3>

          <p style={{
            fontSize: '1.05rem',
            color: 'var(--color-charcoal-muted)',
            marginBottom: '2rem',
            lineHeight: 1.6
          }}>
            {slide.text}
          </p>

          <div>
            <button
              onClick={() => onSelectFeature(slide.id)}
              style={{
                backgroundColor: 'var(--color-forest-green)',
                color: 'white',
                padding: '0.85rem 1.75rem',
                borderRadius: 'var(--radius-full)',
                fontWeight: 700,
                fontSize: '0.95rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                boxShadow: 'var(--shadow-sm)'
              }}
            >
              <span>{slide.cta}</span>
            </button>
          </div>
        </div>

        {/* Right Image */}
        <div style={{
          position: 'relative',
          minHeight: '320px',
          background: `url('${slide.image}') center/cover no-repeat`
        }}>
          <div style={{
            position: 'absolute',
            bottom: '1rem',
            right: '1rem',
            backgroundColor: 'rgba(26, 28, 25, 0.75)',
            backdropFilter: 'blur(4px)',
            color: 'white',
            padding: '0.4rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.75rem',
            fontWeight: 600
          }}>
            📍 {slide.farmerTag}
          </div>
        </div>
      </div>

      {/* Slide Indicators */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginTop: '1.25rem' }}>
        {slides.map((s, idx) => (
          <button
            key={s.id}
            onClick={() => setCurrentIndex(idx)}
            style={{
              width: idx === currentIndex ? '32px' : '10px',
              height: '10px',
              borderRadius: 'var(--radius-full)',
              backgroundColor: idx === currentIndex ? 'var(--color-forest-green)' : 'var(--color-cream-border)',
              transition: 'all 0.3s ease'
            }}
          />
        ))}
      </div>
    </div>
  );
};
