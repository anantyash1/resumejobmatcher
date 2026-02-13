import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadResume } from '../services/api';

const ResumeUploader = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                          'image/png', 'image/jpeg', 'image/jpg'];
      
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setMessage({ type: '', text: '' });
      } else {
        setMessage({ 
          type: 'error', 
          text: 'Please upload a PDF, DOC, DOCX, PNG, or JPG file' 
        });
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file first' });
      return;
    }

    setUploading(true);
    setMessage({ type: '', text: '' });

    try {
      const result = await uploadResume(file);
      setMessage({ 
        type: 'success', 
        text: `Resume uploaded successfully! Found ${result.skills.length} skills.` 
      });
      setFile(null);
      
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to upload resume' 
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-500 mb-4">Upload Your Resume</h2>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
        <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        
        <input
          type="file"
          id="resume-upload"
          className="hidden"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
        />
        
        <label
          htmlFor="resume-upload"
          className="cursor-pointer inline-block btn-secondary"
        >
          Choose File
        </label>
        
        {file && (
          <div className="mt-4 flex items-center justify-center space-x-2 text-gray-700">
            <FileText className="h-5 w-5" />
            <span>{file.name}</span>
          </div>
        )}
        
        <p className="text-sm text-gray-500 mt-2">
          PDF, DOC, DOCX, PNG, or JPG (Max 10MB)
        </p>
      </div>

      {file && (
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="btn-primary w-full mt-4"
        >
          {uploading ? 'Uploading...' : 'Upload & Process'}
        </button>
      )}

      {message.text && (
        <div className={`mt-4 p-4 rounded-lg flex items-center space-x-2 ${
          message.type === 'success' 
            ? 'bg-green-50 text-green-800' 
            : 'bg-red-50 text-red-800'
        }`}>
          {message.type === 'success' 
            ? <CheckCircle className="h-5 w-5" />
            : <AlertCircle className="h-5 w-5" />
          }
          <span>{message.text}</span>
        </div>
      )}
    </div>
  );
};

export default ResumeUploader;