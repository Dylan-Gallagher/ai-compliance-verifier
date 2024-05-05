import React from 'react';
import './RecommendationsCard.css'; 

function RecommendationCard({ recommendation }) {
  return (
    <div className="improvement-card">
      <p className="improvement-text">{recommendation}</p>
    </div>
  );
}

export default RecommendationCard