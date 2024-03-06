// src/components/FileUpload.jsx
import React, { useState } from 'react';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('videoFile', file);

      const response = await fetch('/api', { // Make requests to the proxied URL
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // Handle the response as needed
  //     const data = await response.json();
  //     console.log(data);
  //   } catch (error) {
  //     console.error('Error uploading file:', error);
  //   }

    const data = await response.json();
      // Assuming the response contains the compressed file path
      const compressedFilePath = data.compressed_file_path;
      const fileUrl = `/api/uploads/${encodeURIComponent(compressedFilePath)}`;
      console.log(fileUrl);
      // Handle the file URL as needed
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };



  return (
    <div>
      <h1>File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUpload;




// // src/components/FileUpload.jsx
// import React, { useState } from 'react';

// const FileUpload = () => {
//   const [file, setFile] = useState(null);

//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     setFile(selectedFile);
//   };

//   const handleUpload = async () => {
//     try {
//       const formData = new FormData();
//       formData.append('file', file);

//       const response = await fetch('http://localhost:5000/uploads', {
//         method: 'POST',
//         body: formData,
//       });

//       // Handle the response as needed
//       const data = await response.json();
//       console.log(data);
//     } catch (error) {
//       console.error('Error uploading file:', error);
//     }
//   };

//   return (
//     <div>
//       <h1>File Upload</h1>
//       <input type="file" onChange={handleFileChange} />
//       <button onClick={handleUpload}>Upload</button>
//     </div>
//   );
// };

// export default FileUpload;
