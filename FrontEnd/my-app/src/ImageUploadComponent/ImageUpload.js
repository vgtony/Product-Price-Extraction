import React, { useState } from "react";
import "./ImageUpload.css";

function ImageUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  // const [extractionId, setExtractionId] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    const formData = new FormData();

    // Append the image file
    if (selectedFiles.length > 0) {
      formData.append("image", selectedFiles[0]);
    }

    try {
      // Send to your Django API endpoint
      const response = await fetch("http://127.0.0.1:8000/extractions/", {
        method: "POST",
        body: formData,
      });

      console.log(response);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Upload successful:", data);
      setResults(data);
      // setExtractionId(data.extractionId);

      // After successful upload, you can check results
      // if (data.extractionId) {
      //   await checkResults(data.extractionId);
      // }
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setLoading(false);
    }
  };

  // const checkResults = async (id) => {
  //   // Wait a bit for processing to complete
  //   await new Promise((resolve) => setTimeout(resolve, 5000));

  //   try {
  //     const response = await fetch(
  //       `http://localhost:8000/extractions/${id}/results/`,
  //       {
  //         method: "GET",
  //       }
  //     );

  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }

  //     const data = await response.json();
  //     console.log("Results:", data);
  //     setResults(data);
  //   } catch (error) {
  //     console.error("Error fetching results:", error);
  //   }
  // };

  return (
    <div>
      <h1>Upload Images</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button type="submit" disabled={loading || !selectedFiles.length}>
          {loading ? "Processing..." : "Upload and Process"}
        </button>
      </form>

      {loading && <p>Processing your image...</p>}

      {results && (
        <div className="results-container">
          <h2>Results</h2>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
