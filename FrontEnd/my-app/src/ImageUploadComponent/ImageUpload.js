import React, { useState } from 'react';
import './ImageUpload.css';

function ImageUpload() {
    const [selectedFiles, setSelectedFiles] = useState([]);

    const handleFileChange = (event) => {
        setSelectedFiles(event.target.files);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData();

        for (let i = 0; i < selectedFiles.length; i++) {
            formData.append('file', selectedFiles[i]);
        }
        // console.log('files', formData.getAll('files'));
        // console.log('selectedFiles', selectedFiles);

        formData.append('extractionId', '-O-9cEXgvSKGLfyMPmvW');

        // await new Promise(resolve => setTimeout(resolve, 5000));


        console.log('formData', formData);

        // formData.append('batchId', 'rYvGAqwk4kbS0OHJl4AzyuC3V');
        fetch('http://localhost:8000/files-upload/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    };

    async function postAddBatchResult(data) {
        const url = 'http://localhost:8000/get-batch-results/';
      
        try {
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            //   'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
          });
      
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
      
          const result = await response.json();
          console.log('Success:', result);
          console.log('AAAA', result.files)

          const itemsContainer = document.getElementById('items-container');
          result.items.forEach(item => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'item-row';
            itemDiv.innerHTML = `
            <div class="item-content">
              <div class="item-name"><p>Name: ${item.name}</p></div>
              <div class="item-details">
                <p>Quantity: ${item.quantity}</p>
                <p>Unit Price: ${item.unit_price}</p>
              </div>
            </div>
            `;
            itemsContainer.appendChild(itemDiv);
          });

          return result;
        } catch (error) {
          console.error('Error:', error);
        }
      }
      
      // Example usage:
      const data = {
        extraction_id: '-O-9cEXgvSKGLfyMPmvW',
        batch_id: 'rYvGAqwk4kbS0OHJl4AzyuC3V'
      };
      
    //   postAddBatchResult(data);

    return (
        <div><h1>Upload Images</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" multiple onChange={handleFileChange} />
                <button type="submit">Upload</button>
                <button type="button" onClick={() => postAddBatchResult(data)}>Post Batch Result</button>
                <div id="items-container"></div>
            </form>
        </div>
    );
}

export default ImageUpload;