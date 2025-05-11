import React, { useState } from "react";
import "./Results.css";

const Results = () => {
  const [extractions, setExtractions] = useState([]);
  const [expandedExtractions, setExpandedExtractions] = useState({});

  const fetchExtractions = async () => {
    try {
      const response = await fetch("http://localhost:8000/extractions/");
      const data = await response.json();
      setExtractions(data);
    } catch (error) {
      console.error("Error fetching extractions:", error);
    }
  };

  const toggleExtraction = (extractionId) => {
    setExpandedExtractions((prev) => ({
      ...prev,
      [extractionId]: !prev[extractionId],
    }));
  };

  return (
    <div className="results-container">
      <button onClick={fetchExtractions} className="fetch-button">
        Fetch Extractions
      </button>

      {extractions.length > 0 && (
        <div className="extractions-list">
          {extractions.map((extraction) => (
            <div key={extraction.id} className="extraction-group">
              <div
                className="extraction-header"
                onClick={() => toggleExtraction(extraction.id)}
              >
                <h3>Extraction ID: {extraction.id}</h3>
              </div>

              {expandedExtractions[extraction.id] && (
                <table className="extractions-table">
                  <thead>
                    <tr>
                      <th>Item ID</th>
                      <th>Product Name</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {extraction.items.map((item) => (
                      <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.product_name}</td>
                        <td>${item.product_price}</td>
                        <td>{item.quantity}</td>
                        <td>
                          $
                          {(
                            parseFloat(item.product_price) *
                            parseInt(item.quantity)
                          ).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                    <tr className="total-row">
                      <td
                        colSpan="4"
                        style={{ textAlign: "right", fontWeight: "bold" }}
                      >
                        Total:
                      </td>
                      <td style={{ fontWeight: "bold" }}>
                        $
                        {extraction.items
                          .reduce((total, item) => {
                            return (
                              total +
                              parseFloat(item.product_price) *
                                parseInt(item.quantity)
                            );
                          }, 0)
                          .toFixed(2)}
                      </td>
                    </tr>
                  </tbody>
                </table>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Results;
