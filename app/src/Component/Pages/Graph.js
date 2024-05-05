// This is where the knowledge graph and user documenation highlighting feature is. There is a button to go to the compliance score 
import React from 'react';
import '../../App.css';
import KnowledgeGraph from '../KnowledgeGraph';
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
