import React, { useState } from 'react';
import Graph from 'react-vis-network-graph';
import { edges, nodes } from './Data/finalData.js'; 
import './KnowledgeGraph.css';


export default function KnowledgeGraph() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [physicsOptions, setPhysicsOptions] = useState({
    enabled: true, 
    barnesHut: { 
      gravitationalConstant: -30000,
      centralGravity: 0.01,
      springLength: 75,
      avoidOverlap: 0.2,
      damping: 0.5,
    },
    stabilization: { iterations: 230 } 
  });

  const handlePhysicsChange = (option) => {
    setPhysicsOptions(option);
    setIsDropdownOpen(false); 
  };

  const options = {
    autoResize: true,
    groups: {
      ORG: { color: { background: '#DC143C' }}, 
      PER: { color: { background: '#E040FB' }}, 
      LOC: { color: { background: '#FF8C00' }}, 
      DAT: { color: { background: '#42be65' }}, 
      SYS: { color: { background: '#001d6c' }}, 
      ACT: { color: { background: '#00BFFF' }}, 
      SPA: { color: { background: '#7FFF00' }}, 
      STA: { color: { background: '#FFD700' }}, 
      ALG: { color: { background: '#005d5d' }}, 
      PRO: { color: { background: '#76D7C4' }}, 
      HAR: { color: { background: '#B22222' }}, 
      MAR: { color: { background: '#FF6347' }}, 
      DOC: { color: { background: '#8a3ffc' }}, 
      ETH: { color: { background: '#ff7eb6' }}  
  },
    nodes: {
      shape: 'dot', 
      scaling: {
        min: 5, 
        max: 40, 
        label: { 
          min: 7,  
          max: 25,  
          drawThreshold: 8, 
          maxVisible: 10000,
        },
        customScalingFunction: function (min, max, total, value) {
          if (max === min) {
            return 0.5; 
          } else {
            let scale = 1 / (max - min);
            return Math.max(0, Math.min(1, (value - min) * scale)); 
          }
        }
      },
      font: { 
        size: 5,  
        strokeWidth: 0.1,
        face: 'Tahoma',  
        color: 'black',  
      },
      shadow: false,
    },
    edges: {
      font: { 
        size: 6, 
        color: '#000000', 
        background: 'none',   
        strokeWidth: 0,       
      },
      width: 0.5, 
      color: {
        opacity: 1.0
      },
      hoverWidth: 0.55,
      selectionWidth: 0.55, 
      arrows: {
          to: { 
              enabled: true, 
              scaleFactor: 0.3,  
          },
      },
      chosen: { 
        edge: function(values, id, selected, hovering) {
          if (hovering) {
            values.width = 2;  
            values.color = '#ff8389'; 
          } else if (hovering) {
            values.opacity = 0.6; 
          }
      },
        label: function(values, id, selected, hovering) {
          if (hovering) { 
            values.color = '#000000';
            values.size *= 2.3;  
          }
        }
      
    },
    length: undefined,
    smooth: {
      type: 'dynamic',
      roundness: 0.5,
    }
    
  },
    
    layout: {
      improvedLayout: false,
      randomSeed: 4, 
      hierarchical: {
        enabled: false,
        direction: "LR", 
      },
    },
  physics: physicsOptions, 
  interaction: {
    navigationButtons: true,  
    tooltipDelay: 200,        
    hideEdgesOnDrag: true,    
    hideEdgesOnZoom: true,    
    hover: true,              
    hoverConnectedEdges: true,
    multiselect: true,   
    dragView: true       
  },
  height: '1000px',         
  };

  const data = { nodes: nodes, edges: edges }; 
  return (
    <div className="container">
      <Graph graph={data} options={options} />
        <div className="physics-controls"> 
          <button onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
            Physics Options
          </button>
          {isDropdownOpen && (
            <div className="dropdown-content">
              <button onClick={() => handlePhysicsChange({ enabled: true })}>
                Enable Physics
              </button>            
              <button onClick={() => handlePhysicsChange({ enabled: false })}>
                Disable Physics
              </button>
              <button onClick={() => handlePhysicsChange({ 
                  enabled: true,
                  barnesHut: {
                    gravitationalConstant: -60000,
                    centralGravity: 0.3,
                    springLength: 300,
                    avoidOverlap: 1,
                    damping: 1,
                  },
                  stabilization: { iterations: 2500 }
              })}>
                Strong Repulsion
              </button>
              <button onClick={() => handlePhysicsChange({ 
                  enabled: true,
                  barnesHut: {
                    gravitationalConstant: -30000,
                    centralGravity: 1,
                    springLength: 75,
                    avoidOverlap: 1,
                    damping: 1,
                  },
                  stabilization: { iterations: 2500 }
              })}>
                Barnes-Hut Layout 
              </button>
            </div>
          )}
        </div>
    </div>
  );
}
