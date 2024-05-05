import React, { useEffect, useState } from 'react';
import './ComplianceScore.css';
import RecommendationCard from './RecommendationsCard'; 

//Main function to display the compliance score and recommendations
function ComplianceScore() {
  const [score, setScore] = useState(0); 
  const [improvements, setImprovements] = useState([]);

  useEffect(() => {
    const storedData = localStorage.getItem('rulesMiningData');
    if (storedData) {
      const rulesMiningData = JSON.parse(storedData);
      const [retrievedScore, improvementsArray] = rulesMiningData
      setScore(retrievedScore);
      setImprovements(improvementsArray);
    }
  }, []);
  
    return (
      <div>
      <div className="score-container">
          <div className="score">
            <div className="score-bar">
              <div className="placeholder">{progressBar(100)}</div>
              <div className="score-circle">{progressBar(score, true)}</div>
            </div>
            <div className="score-value">
              <div className="score-name">Score</div>
              <div className="score-number">{Math.round(score)}%</div>
            </div>
          </div>
      </div>
      <div className="text">
      <h2>Our Recommendations</h2>
          {improvements.map((improvement, index) => (
            <RecommendationCard key={index} recommendation={improvement} />
          ))}
      </div>
      </div>
    );
  }
  
  function progressBar(widthPerc, gradient = false) {
    const radius = 200; 
    const strokeWidth = 30; 
    const dashArray = (Math.PI * radius * widthPerc) / 100;
    const svgWidth = radius * 2 + strokeWidth; 
    const svgHeight = radius + strokeWidth;
  
    return (
      <svg width={svgWidth} height={svgHeight}>
        <circle
          cx={radius + (strokeWidth / 2)}
          cy={radius + (strokeWidth / 2)}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDashoffset={-1 * Math.PI * radius}
          strokeDasharray={`${dashArray} 10000`}
          stroke={gradient ? "url(#score-gradient)" : "#e5e5e5"}
        ></circle>
        {gradient && (
          <defs>
            <linearGradient id="score-gradient">
            <stop offset="0%" stopColor="#002c5d" /> 
            <stop offset="25%" stopColor="#007bff" /> 
            <stop offset="100%" stopColor="#b3d7ff" />
            </linearGradient>
          </defs>
        )}
      </svg>
    );
  }
  

  export default ComplianceScore;