import React, { useState } from 'react';
   import { Document, Page, pdfjs } from 'react-pdf';
   import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
   import 'react-pdf/dist/esm/Page/TextLayer.css';

   // Set the worker for react-pdf
   pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

   const PDFViewer = ({ pdfFile }) => {
     const [numPages, setNumPages] = useState(null);

     const onDocumentLoadSuccess = ({ numPages }) => {
       setNumPages(numPages);
     };

     return (
       <div className="mt-4 border border-gray-300 p-2 max-h-96 overflow-auto">
         <Document file={pdfFile} onLoadSuccess={onDocumentLoadSuccess}>
           {Array.from(new Array(numPages), (el, index) => (
             <Page key={`page_${index + 1}`} pageNumber={index + 1} scale={1.0} />
           ))}
         </Document>
       </div>
     );
   };

   export default PDFViewer;