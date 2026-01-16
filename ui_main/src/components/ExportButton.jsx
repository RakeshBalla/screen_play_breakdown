import React from 'react';
import { exportToCSV, exportToPDF } from '../lib/exporter';

const ExportButton = ({ scriptElements, tags }) => {
  const handleExportCSV = () => {
    exportToCSV(scriptElements, tags);
  };

  const handleExportPDF = () => {
    exportToPDF(scriptElements, tags);
  };

  return (
    <div className="space-y-2 mt-4">
      <button
        onClick={handleExportCSV}
        className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
      >
        Export to CSV
      </button>
      <button
        onClick={handleExportPDF}
        className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
      >
        Export to PDF
      </button>
    </div>
  );
};

export default ExportButton;