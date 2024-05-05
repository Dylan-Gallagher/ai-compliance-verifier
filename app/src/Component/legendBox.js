import React, { useState } from 'react';
import './legendBox.css'; 

//Main function to display categories legend box
const legendCategories = [
  // Start with SYS (Deep Blue)
  { label: 'SYS - System', color: '#001d6c', definitions: [] }, 

  // Blues
  { label: 'ACT - Action', color: '#00BFFF', definitions: [] }, // Bright Blue
  { label: 'ALG - Automated Process or Algorithm', color: '#005d5d', definitions: [] }, // Dark Teal

  // Greens
  { label: 'PRO - Process', color: '#76D7C4', definitions: [] }, // Light Green
  { label: 'DAT - Data', color: '#42be65', definitions: [] }, // Deep Green
  { label: 'SPA - Space', color: '#7FFF00', definitions: [] }, // Yellow-Green 

  // Yellows, Orange
  { label: 'STA - Standard', color: '#FFD700', definitions: [] }, // Gold
  { label: 'LOC - Location', color: '#FF8C00', definitions: [] }, // Orange

  // Reds, Pinks
  { label: 'HAR - Harm', color: '#B22222', definitions: [] }, // Brick Red
  { label: 'MAR - Marking', color: '#FF6347', definitions: [] }, // Coral 
  { label: 'ORG - Organisations', color: '#DC143C', definitions: [] }, // Deep Red
  { label: 'ETH - Ethical Concept', color: '#ff7eb6', definitions: [] }, // Light Pink
  { label: 'PER - Person', color: '#E040FB', definitions: [] }, // Vivid Pink

  // Miscellaneous
  { label: 'DOC - Documentation', color: '#8a3ffc', definitions: [] }, // Lavender
];

const LegendBox = () => {
  const [legendVisible, setLegendVisible] = useState(true);

  const toggleLegend = () => {
    setLegendVisible(!legendVisible); 
  };

  return (
    <div> 
      <button className="hide-legend-btn" onClick={toggleLegend}> 
        {legendVisible ? 'Hide Legend' : 'Show Legend'} 
      </button>

      {legendVisible && (  // Conditionally render the legend
        <div className="legend-container">
          <h2>Legend</h2>
          <ul>
            {legendCategories.map((category) => (
              <li key={category.label}>
                <span className="color-box" style={{ backgroundColor: category.color }}></span>
                {category.label} 
                <ul className="definitions"> 
                  {category.definitions.map(def => <li key={def}>{def}</li>)}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LegendBox;