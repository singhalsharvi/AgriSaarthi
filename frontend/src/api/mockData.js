export const MOCK_CROP_RESPONSE = {
  location: "Meerut, Uttar Pradesh",
  season: "Kharif",
  soil: "Alluvial Soil (Loam), pH: 6.8",
  weather: {
    temperature: 28.5,
    humidity: 68.0,
    precipitation: 12.0,
    annual_rainfall_estimate: 1050.0
  },
  ml_confidence: "92.40%",
  recommendation_source: "ML Model + ICAR Agricultural RAG",
  recommended_crops: [
    {
      crop: "Rice (Paddy)",
      reason: "Optimal rainfall (1050mm) and high humidity (68%) match local Alluvial soil characteristics during Kharif season.",
      confidence: "92.40%",
      source: "ML Prediction",
      details: {
        n: "80-120 kg/ha",
        p: "40-60 kg/ha",
        k: "40-60 kg/ha",
        water: "High (1200-1500 mm total requirement)",
        irrigation: "Canal or tubewell flooded field technique",
        image: "https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=800&q=80"
      }
    },
    {
      crop: "Maize (Corn)",
      reason: "Well-drained loam soil with moderate temperature (28°C) provides excellent root establishment and grain formation.",
      confidence: "87.15%",
      source: "ML Prediction",
      details: {
        n: "120-150 kg/ha",
        p: "60-75 kg/ha",
        k: "40-50 kg/ha",
        water: "Moderate (500-800 mm)",
        irrigation: "Furrow irrigation at critical tasseling stage",
        image: "https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=800&q=80"
      }
    },
    {
      crop: "Sugarcane",
      reason: "High temperature tolerance and fertile river plain soil support high sucrose yield per hectare in western UP belt.",
      confidence: "81.90%",
      source: "ICAR Regional Advisory",
      details: {
        n: "150-250 kg/ha",
        p: "60-90 kg/ha",
        k: "60-90 kg/ha",
        water: "High (1500-2500 mm)",
        irrigation: "Drip or alternate furrow irrigation",
        image: "https://images.unsplash.com/photo-1601593346740-925612772716?auto=format&fit=crop&w=800&q=80"
      }
    }
  ],
  warning: null,
  explanation: "Based on soil and weather parameters in Meerut district, Rice and Maize are the most suitable crops for the Kharif season. High soil organic nitrogen and favorable precipitation support maximum yield."
};

export const MOCK_DISEASE_RESPONSE = {
  status: "success",
  disease_status: "Tomato — Late Blight (Phytophthora infestans)",
  confidence: "91.80%",
  top_matches: [
    { name: "Late Blight", confidence: "91.8%" },
    { name: "Early Blight", confidence: "5.2%" },
    { name: "Healthy Leaf", confidence: "3.0%" }
  ],
  ai_explanation: `### Diagnosis: Late Blight (Tomato)
**Confidence**: 91.8%

#### Symptoms Observed:
- Large, water-soaked dark brown spots near leaf margins.
- White fungal growth on the underside of infected leaves during moist weather.
- Rapid wilting and collapse of foliage.

#### Causes:
Late blight is caused by the oomycete *Phytophthora infestans*. It thrives under cool, wet weather with relative humidity above 85% and temperatures between 15°C and 22°C.

#### Recommended Organic & Chemical Remedies:
1. **Immediate Spray**: Apply Copper Oxychloride (3g/liter water) or Mancozeb 75 WP (2g/liter water) immediately.
2. **Systemic Fungicide**: In severe cases, spray Metalaxyl 8% + Mancozeb 64% WP at 2g/liter of water.
3. **Field Hygiene**: Remove and burn severely affected leaves to prevent sporangia from spreading through wind/rain drops.
4. **Air Circulation**: Avoid overhead sprinkler irrigation and increase plant spacing for airflow.`
};

export const MOCK_GOVT_SCHEMES_RESPONSE = {
  status: "success",
  eligible_schemes: [
    "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
    "Kisan Credit Card (KCC) Scheme",
    "Paramparagat Krishi Vikas Yojana (PKVY)",
    "Sub-Mission on Agricultural Mechanization (SMAM)"
  ],
  recommended_schemes: [
    {
      scheme_name: "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
      official_website: "https://pmkisan.gov.in",
      source_file: "Ministry of Agriculture & Farmers Welfare",
      distance: 0.0512,
      snippet: "Provides income support of ₹6,000 per year to all landholding farmer families across India in three equal installments of ₹2,000 transferred directly to bank accounts.",
      benefits: "Direct financial support of ₹6,000 per year in 3 installments.",
      eligibility: "Small and marginal farmers holding cultivable land in India.",
      documents: ["Aadhaar Card", "Landholding Ownership Papers", "Bank Passbook with IFSC"]
    },
    {
      scheme_name: "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
      official_website: "https://pmfby.gov.in",
      source_file: "Department of Agriculture",
      distance: 0.0834,
      snippet: "Comprehensive crop insurance scheme providing financial coverage against non-preventable natural risks like drought, flood, pests & plant disease outbreaks.",
      benefits: "Low farmer premium (1.5% Rabi, 2% Kharif) with full crop loss claim payout.",
      eligibility: "Farmers growing notified crops in notified areas including sharecroppers.",
      documents: ["Sowing Certificate", "Khasra/Khatauni Land Record", "Bank Details"]
    },
    {
      scheme_name: "Kisan Credit Card (KCC) Subsidy Scheme",
      official_website: "https://kcc.gov.in",
      source_file: "NABARD & RBI",
      distance: 0.1120,
      snippet: "Provides timely institutional credit to farmers for agricultural needs, seeds, fertilizers, and equipment at a low interest rate of 4% per annum.",
      benefits: "Subsidized interest rate at 4% per annum up to credit limit of ₹3 Lakhs.",
      eligibility: "All farmers, tenant farmers, and self-help groups.",
      documents: ["Application Form", "Land Identity Proof", "Aadhaar Card"]
    }
  ],
  ai_explanation: "Based on your landholding (2.5 Acres) and state profile in Uttar Pradesh, you qualify for top priority government schemes including PM-KISAN direct income transfer and PMFBY crop insurance against weather uncertainties."
};
