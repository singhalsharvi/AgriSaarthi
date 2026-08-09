import React, { useState } from 'react';
import { HeroSection } from '../components/home/HeroSection';
import { FeatureStorySlider } from '../components/home/FeatureStorySlider';
import { GetStartedFlow } from '../components/home/GetStartedFlow';
import { DesiStoryJourney } from '../components/home/DesiStoryJourney';

export const HomePage = ({ onNavigate }) => {
  const [isGetStartedOpen, setIsGetStartedOpen] = useState(false);

  return (
    <div className="page-container">
      {/* 1. Large Real Photography Hero */}
      <HeroSection
        onGetStarted={() => setIsGetStartedOpen(true)}
        onExploreFeatures={() => onNavigate('features')}
      />

      {/* 2. Storytelling Carousel Slider */}
      <FeatureStorySlider onSelectFeature={onNavigate} />

      {/* 3. From Soil to Decision Visual Story */}
      <DesiStoryJourney />

      {/* 4. Farmer Guided Option Flow */}
      <GetStartedFlow
        isOpen={isGetStartedOpen}
        onClose={() => setIsGetStartedOpen(false)}
        onSelectOption={onNavigate}
      />
    </div>
  );
};
