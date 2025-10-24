'use client';

import { useState } from 'react';
import axios from 'axios';
import { Upload, Loader2, CheckCircle, XCircle } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface VideoUploadProps {
  onUploadComplete?: () => void;
}

export default function VideoUpload({ onUploadComplete }: VideoUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [instruction, setInstruction] = useState('');
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus('idle');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file || !instruction.trim()) {
      setStatus('error');
      setMessage('Please select a video and provide instructions');
      return;
    }

    setUploading(true);
    setStatus('idle');
    setMessage('');

    const formData = new FormData();
    formData.append('video', file);
    formData.append('instruction', instruction);

    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setStatus('success');
      setMessage(`Video uploaded successfully! Job ID: ${response.data.job_id}`);
      setFile(null);
      setInstruction('');

      // Reset file input
      const fileInput = document.getElementById('video-file') as HTMLInputElement;
      if (fileInput) fileInput.value = '';

      // Notify parent component
      if (onUploadComplete) {
        onUploadComplete();
      }
    } catch (error) {
      setStatus('error');
      if (axios.isAxiosError(error)) {
        setMessage(error.response?.data?.detail || 'Failed to upload video');
      } else {
        setMessage('An unexpected error occurred');
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white/10 backdrop-blur-lg rounded-lg p-8 shadow-xl">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload */}
        <div>
          <label htmlFor="video-file" className="block text-sm font-medium text-gray-200 mb-2">
            Upload Video
          </label>
          <div className="relative">
            <input
              id="video-file"
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-300
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-purple-600 file:text-white
                hover:file:bg-purple-700
                file:cursor-pointer cursor-pointer"
            />
          </div>
          {file && (
            <p className="mt-2 text-sm text-gray-300">
              Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          )}
        </div>

        {/* Instruction Input */}
        <div>
          <label htmlFor="instruction" className="block text-sm font-medium text-gray-200 mb-2">
            Editing Instructions
          </label>
          <textarea
            id="instruction"
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder="e.g., Make the sky sunset colors, Add a vintage film effect, Change the background to a beach..."
            rows={4}
            className="w-full px-4 py-2 bg-white/5 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={uploading || !file || !instruction.trim()}
          className="w-full flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          {uploading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Uploading...
            </>
          ) : (
            <>
              <Upload className="w-5 h-5" />
              Upload & Edit Video
            </>
          )}
        </button>

        {/* Status Messages */}
        {status === 'success' && (
          <div className="flex items-center gap-2 text-green-400 bg-green-400/10 p-4 rounded-lg">
            <CheckCircle className="w-5 h-5" />
            <p>{message}</p>
          </div>
        )}

        {status === 'error' && (
          <div className="flex items-center gap-2 text-red-400 bg-red-400/10 p-4 rounded-lg">
            <XCircle className="w-5 h-5" />
            <p>{message}</p>
          </div>
        )}
      </form>
    </div>
  );
}
