import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Component/Pages/Home';
import Graph from './Component/Pages/Graph';
import Navbar from './Component/NavBar'; 
import LegendBox from './Component/legendBox';
import About from './Component/Pages/About';
import ComplianceScore from './Component/Pages/Compliance';
import Graph2 from './Component/Pages/Graph2';
import './App.css';

function App() {
  const [uploadSuccess, setUploadSuccess] = useState(false);     // State variable to track upload success

  const handleUploadSuccess = () => {    // Function to handle upload success
    setUploadSuccess(true);
  };

  // Render the application
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' element={<Home onUploadSuccess={handleUploadSuccess} />} />
        <Route 
          path='/knowledge-graph' 
          element={
            <Graph uploadSuccess={uploadSuccess}>
              <LegendBox /> 
            </Graph>
          } 
        />
        <Route path='/about' element={<About />} />
        <Route path='/compliance' element={<ComplianceScore />} />
        <Route path='/graph' element={<Graph2 />} />
      </Routes>
    </Router>
  );
}

export default App;
