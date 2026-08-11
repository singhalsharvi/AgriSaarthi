import React from 'react';
import { HeroSection } from '../components/home/HeroSection';
import { FeatureStorySlider } from '../components/home/FeatureStorySlider';
import { DesiStoryJourney } from '../components/home/DesiStoryJourney';

export const HomePage = ({ onNavigate }) => {
  return (
    <div className="page-container">
      {/* 1. Large Real Photography Hero */}
      <HeroSection
        onGetStarted={() => onNavigate('signin')}
        onExploreFeatures={() => onNavigate('features')}
      />

      {/* 2. Storytelling Carousel Slider */}
      <FeatureStorySlider onSelectFeature={onNavigate} />

      {/* 3. From Soil to Decision Visual Story */}
      <DesiStoryJourney />

    </div>
  );
};
