import React, { useState } from 'react';
   import FileLoader from './components/FileLoader.jsx';
   import ScriptViewer from './components/ScriptViewer.jsx';
   import TagSidebar from './components/TagSidebar.jsx';
   import ExportButton from './components/ExportButton.jsx';
   import './App.css';

   const App = () => {
     const [scriptElements, setScriptElements] = useState([]);
     const [tags, setTags] = useState({
       CAST: { color: '#FF6B6B', visible: true },
       PROPS: { color: '#4ECDC4', visible: true },
       LOCATION: { color: '#45B7D1', visible: true },
     });

     const handleFileParsed = (elements) => {
       setScriptElements(elements);
     };

     const updateTags = (newTags) => {
       setTags(newTags);
     };

     return (
       <div className="flex h-screen">
         <div className="w-1/4 bg-gray-100 p-4">
           <FileLoader onFileParsed={handleFileParsed} />
           <TagSidebar tags={tags} updateTags={updateTags} />
           <ExportButton scriptElements={scriptElements} tags={tags} />
         </div>
         <div className="w-3/4 p-4 overflow-auto">
           <ScriptViewer scriptElements={scriptElements} tags={tags} />
         </div>
       </div>
     );
   };

   export default App;