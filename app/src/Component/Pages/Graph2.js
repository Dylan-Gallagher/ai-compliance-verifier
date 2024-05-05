//This displays the knowledge graph for exploration purposes
import React from 'react';
import '../../App.css';
import KnowledgeGraph from '../KnowledgeGraphOnly';
import LegendBox from '../legendBox'; 

function Graph(){
  return (
    <div className="graph-container"> 
      <KnowledgeGraph />
      <LegendBox /> 
    </div>
  );
}

export default Graph;
