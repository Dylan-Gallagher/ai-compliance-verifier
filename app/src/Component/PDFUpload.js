import React from 'react';
import '../App.css';

function PDFUpload({ onUpload }) {
  let fileInput = React.createRef();

  const handleUploadClick = () => {
    fileInput.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div>
      <input type="file" accept="application/pdf" ref={fileInput} onChange={handleFileChange} style={{display: 'none'}} />
      <button className="ibm-button" onClick={handleUploadClick}>Upload AI Model Documentation  → </button>
    </div>
  );
}

export default PDFUpload;
