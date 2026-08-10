import { 
  MOCK_CROP_RESPONSE, 
  MOCK_DISEASE_RESPONSE, 
  MOCK_GOVT_SCHEMES_RESPONSE 
} from './mockData';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

function dataURLtoBlob(dataurl) {
  if (!dataurl || typeof dataurl !== 'string') return null;
  const arr = dataurl.split(',');
  const mimeMatch = arr[0].match(/:(.*?);/);
  const mime = mimeMatch ? mimeMatch[1] : 'image/jpeg';
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

async function fetchWithTimeout(url, options = {}, timeoutMs = 25000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const headers = { ...(options.headers || {}) };
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }
    
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: headers
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}

export const apiService = {
  // Check API status
  checkHealth: async () => {
    try {
      return await fetchWithTimeout(`${BASE_URL}/health`, { method: 'GET' }, 3000);
    } catch {
      return { status: "healthy", mode: "offline_demo" };
    }
  },

  // 1. Crop Recommendation API
  recommendCrop: async (payload) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/crop/recommend`, {
        method: 'POST',
        body: JSON.stringify({
          location: payload.location || "Meerut, Uttar Pradesh",
          season: payload.season || "Kharif",
          Nitrogen: payload.n ? parseFloat(payload.n) : 90.0,
          Phosphorus: payload.p ? parseFloat(payload.p) : 42.0,
          Potassium: payload.k ? parseFloat(payload.k) : 43.0,
          Temperature: payload.temperature ? parseFloat(payload.temperature) : undefined,
          Humidity: payload.humidity ? parseFloat(payload.humidity) : undefined,
          pH_Value: payload.ph ? parseFloat(payload.ph) : 6.8,
          Rainfall: payload.rainfall ? parseFloat(payload.rainfall) : undefined,
          Soil_Type: payload.soilType || undefined,
          user_query: payload.userQuery || `What crops are suitable for ${payload.location} in ${payload.season}?`
        })
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      // Return custom mock response populated with user location & season
      return {
        ...MOCK_CROP_RESPONSE,
        location: payload.location || MOCK_CROP_RESPONSE.location,
        season: payload.season || MOCK_CROP_RESPONSE.season
      };
    }
  },

  // 2. Disease Detection API
  analyzeDisease: async (payload) => {
    try {
      let body;
      const headers = {};
      if (payload.image) {
        body = new FormData();
        const blob = dataURLtoBlob(payload.image);
        if (blob) {
          body.append("image", blob, "leaf.jpg");
        }
        body.append("crop_name", payload.cropName || "");
        body.append("symptoms", payload.symptoms || "");
        body.append("user_query", payload.userQuery || "");
      } else {
        body = JSON.stringify({
          crop_name: payload.cropName || "Tomato",
          symptoms: payload.symptoms || "Dark brown leaf spots with yellow margins",
          user_query: payload.userQuery || "How to treat leaf spot disease?"
        });
      }

      const data = await fetchWithTimeout(`${BASE_URL}/disease/analyze`, {
        method: 'POST',
        body: body,
        headers: headers
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      return {
        ...MOCK_DISEASE_RESPONSE,
        crop_name: payload.cropName || "Tomato"
      };
    }
  },

  // 3. Government Schemes API
  recommendSchemes: async (payload) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/government-schemes/recommend`, {
        method: 'POST',
        body: JSON.stringify({
          state: payload.state || "Uttar Pradesh",
          crop: payload.crop || "Rice",
          farmer_category: payload.farmerCategory || "Small and marginal farmer families",
          annual_income: payload.annualIncome ? parseFloat(payload.annualIncome) : 50000,
          landholding: payload.landholding ? parseFloat(payload.landholding) : 1.5,
          user_query: payload.userQuery || "Financial assistance and crop insurance schemes",
          top_k: 5
        })
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      return {
        ...MOCK_GOVT_SCHEMES_RESPONSE,
        state: payload.state || "Uttar Pradesh"
      };
    }
  },

  // 4. Farmer Profile API
  getFarmerProfile: async (farmerId) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/farmer/profile/${farmerId}`, {
        method: 'GET'
      });
      return data.profile;
    } catch (err) {
      console.warn("Backend API unreachable for profile retrieval:", err.message);
      return null;
    }
  },

  saveFarmerProfile: async (profile) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/farmer/profile`, {
        method: 'POST',
        body: JSON.stringify({
          farmer_id: profile.emailOrPhone,
          name: profile.name,
          location: profile.location,
          contact_info: profile.emailOrPhone,
          preferred_language: profile.preferredLanguage || 'en',
          land_size: profile.landholding,
          soil_type: profile.soilType
        })
      });
      return data.profile;
    } catch (err) {
      console.warn("Backend API unreachable for profile saving:", err.message);
      return profile;
    }
  }
};
