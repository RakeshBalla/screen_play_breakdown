import React, { useRef, useState } from 'react';
   import { parseScript } from '../lib/parser';
   import { classifyElements } from '../lib/classifier';
   import { tagElements } from '../lib/tagger';
   import PDFViewer from './PDFViewer.jsx';

   const FileLoader = ({ onFileParsed }) => {
     const fileInputRef = useRef(null);
     const [pdfFile, setPdfFile] = useState(null);

     const handleFileChange = async (event) => {
       const file = event.target.files[0];
       if (!file) return;

       if (file.type === 'application/pdf') {
         setPdfFile(URL.createObjectURL(file));
         const formData = new FormData();
         formData.append('file', file);
         try {
           const response = await fetch('http://localhost:4000/parse-pdf', {
             method: 'POST',
             body: formData,
           });
           const { text, error } = await response.json();
           if (error) {
             console.error('Server error:', error);
             return;
           }
           const parsed = parseScript(text);
           const classified = classifyElements(parsed);
           const tagged = tagElements(classified);
           onFileParsed(tagged);
         } catch (error) {
           console.error('Error parsing PDF:', error);
         }
       } else if (file.type === 'text/plain') {
         const text = await file.text();
         const parsed = parseScript(text);
         const classified = classifyElements(parsed);
         const tagged = tagElements(classified);
         setPdfFile(null);
         onFileParsed(tagged);
       }
     };

     return (
       <div className="mb-4">
         <input
           type="file"
           accept=".txt,.pdf"
           ref={fileInputRef}
           onChange={handleFileChange}
           className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-blue-500 file:text-white hover:file:bg-blue-600"
         />
         {pdfFile && <PDFViewer pdfFile={pdfFile} />}
       </div>
     );
   };

   export default FileLoader;