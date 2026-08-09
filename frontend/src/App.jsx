import React, { useState } from 'react';
import { LanguageProvider } from './context/LanguageContext';
import { AuthProvider } from './context/AuthContext';

import { DesktopSidebar } from './components/layout/DesktopSidebar';
import { MobileHeader } from './components/layout/MobileHeader';
import { MobileBottomNav } from './components/layout/MobileBottomNav';
import { LanguageModal } from './components/layout/LanguageModal';
import { Footer } from './components/layout/Footer';

import { HomePage } from './pages/HomePage';
import { FeaturesPage } from './pages/FeaturesPage';
import { CropRecommendationPage } from './pages/CropRecommendationPage';
import { DiseaseDetectionPage } from './pages/DiseaseDetectionPage';
import { GovernmentSchemesPage } from './pages/GovernmentSchemesPage';
import { DashboardPage } from './pages/DashboardPage';
import { AboutUsPage } from './pages/AboutUsPage';
import { HelpSupportPage } from './pages/HelpSupportPage';
import { SignInPage } from './pages/SignInPage';

import './styles/global.css';

export function AppContent() {
  const [activeTab, setActiveTab] = useState('home');

  const renderCurrentPage = () => {
    switch (activeTab) {
      case 'home':
        return <HomePage onNavigate={setActiveTab} />;
      case 'features':
        return <FeaturesPage onNavigate={setActiveTab} />;
      case 'crop':
        return <CropRecommendationPage />;
      case 'disease':
        return <DiseaseDetectionPage />;
      case 'schemes':
        return <GovernmentSchemesPage />;
      case 'dashboard':
        return <DashboardPage onNavigate={setActiveTab} />;
      case 'about':
        return <AboutUsPage />;
      case 'help':
        return <HelpSupportPage />;
      case 'signin':
        return <SignInPage onNavigate={setActiveTab} />;
      default:
        return <HomePage onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="app-container">
      {/* Desktop Left Sidebar */}
      <DesktopSidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Mobile Top Header */}
      <MobileHeader activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Viewport */}
      <main className="main-content">
        {renderCurrentPage()}
        <Footer setActiveTab={setActiveTab} />
      </main>

      {/* Mobile Bottom Navigation */}
      <MobileBottomNav activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Equal 5-Language Selector Modal */}
      <LanguageModal />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <AppContent />
      </LanguageProvider>
    </AuthProvider>
  );
}
