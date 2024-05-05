//Homepage where a user can go directly and see the knowledge graph or upload their AI model documentation
import React, { useState } from 'react';
import '../../App.css';
import PDFUpload from '../PDFUpload';
import { useNavigate } from 'react-router-dom';
import leftImage from '../Images/home.png';
import Modal from '../Modal';

function Home({ onUploadSuccess }) {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalFields, setModalFields] = useState([]); 
  const [modalContent, setModalContent] = useState('');

  const handlePDFUpload = (file) => {
    let formData = new FormData();
    formData.append('file', file);

    fetch(`${process.env.REACT_APP_API_URL}/upload`, {
      method: 'POST',
      body: formData
    })
      .then(response => response.json().then(data => ({ status: response.status, body: data })))
      .then(res => {
        if (res.status !== 200) {
          if (res.body.empty_fields) {
            setModalFields(res.body.empty_fields); 
            setIsModalOpen(true); // Open the modal
          } else {
            // Handle other errors
            setModalFields([]);
            setIsModalOpen(true);
            setModalContent(`There was a problem with the file upload. ${res.body.error}`);
          }
        } else {
          // Success case remains unchanged
          const { factsheet_data, rules_mining_data } = res.body;
          localStorage.setItem('factsheetData', JSON.stringify(factsheet_data));
          localStorage.setItem('rulesMiningData', JSON.stringify(rules_mining_data));
          onUploadSuccess();
          navigate("/knowledge-graph");
        }
      })
      .catch(error => {
        console.log('There was a problem with the fetch operation: ' + error.message);
        setIsModalOpen(true);
        setModalFields([]); // Ensure fields are cleared for non-field errors
        setModalContent('There was an error processing your request.');
      });
  };

  const goToKnowledgeGraph = () => {
    navigate("/graph");
  };

  return (
    <div className="home">
      <div className="home-content">
        <div className="home-image-container">
          <img src={leftImage} alt="AI Concept" className="home-image" />
        </div>
        <div className="home-text">
          <h1>Creating Trustworthy and Ethical AI</h1>
          <p>Test your AI model to see if it is compliant with the EU AI Act</p>
          <div className="button-container">
          <PDFUpload onUpload={handlePDFUpload} />
          <button className="ibm-button" onClick={goToKnowledgeGraph}>See Knowledge Graph   → </button>
        </div>
        </div>
      </div>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <p>The factsheet uploaded does not follow the structure required.</p>
        {modalFields.length > 0 && (
          <>
            <p>Missing or empty fields:</p>
            <ul>
              {modalFields.map((field, index) => (
                <li key={index}>{field}</li>
              ))}
            </ul>
          </>
        )}
        {modalFields.length === 0 && <p>{modalContent}</p>}
      </Modal>
    </div>
  );
}

export default Home;
