import React, { createContext, useContext, useState, useEffect } from 'react';
import en from '../translations/en.json';
import hi from '../translations/hi.json';
import bn from '../translations/bn.json';
import mr from '../translations/mr.json';
import kn from '../translations/kn.json';

const translationsMap = {
  en,
  hi,
  bn,
  mr,
  kn
};

export const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' }
];

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [currentLang, setCurrentLang] = useState(() => {
    return localStorage.getItem('agri_lang') || 'en';
  });

  const [isLangModalOpen, setIsLangModalOpen] = useState(false);

  useEffect(() => {
    localStorage.setItem('agri_lang', currentLang);
    document.documentElement.lang = currentLang;
    
    // Add indicative script font class to body
    document.body.className = `lang-${currentLang}`;
  }, [currentLang]);

  const changeLanguage = (langCode) => {
    if (translationsMap[langCode]) {
      setCurrentLang(langCode);
    }
  };

  const t = (keyPath) => {
    const keys = keyPath.split('.');
    let current = translationsMap[currentLang] || translationsMap.en;
    
    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // Fallback to English if translation key is missing
        let fallback = translationsMap.en;
        for (const fk of keys) {
          if (fallback && fallback[fk] !== undefined) {
            fallback = fallback[fk];
          } else {
            return keyPath;
          }
        }
        return fallback;
      }
    }
    return current;
  };

  return (
    <LanguageContext.Provider value={{ 
      currentLang, 
      changeLanguage, 
      t, 
      languages: LANGUAGES,
      isLangModalOpen,
      setIsLangModalOpen
    }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
