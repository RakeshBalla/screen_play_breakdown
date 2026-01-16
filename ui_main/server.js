const express = require('express');
   const path = require('path');
   const pdfParse = require('pdf-parse');
   const multer = require('multer');
   const app = express();
   const port = 4000;

   app.use(express.static(path.join(__dirname, 'public')));
   app.use(express.static(path.join(__dirname, 'src')));

   // Log requests for debugging
   app.use((req, res, next) => {
     console.log(`Request for: ${req.url}`);
     next();
   });

   // Handle module requests for client-side ES modules
   app.get('*.js', (req, res, next) => {
     res.set('Content-Type', 'application/javascript');
     next();
   });

   // Handle file uploads
   const upload = multer({ storage: multer.memoryStorage() });

   // API endpoint for PDF parsing
   app.post('/parse-pdf', upload.single('file'), async (req, res) => {
     try {
       const pdfBuffer = req.file.buffer;
       const data = await pdfParse(pdfBuffer);
       res.json({ text: data.text });
     } catch (error) {
       console.error('PDF parsing error:', error);
       res.status(500).json({ error: 'Failed to parse PDF' });
     }
   });

   app.listen(port, () => {
     console.log(`Server running at http://localhost:${port}`);
   });