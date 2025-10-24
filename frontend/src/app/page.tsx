'use client';

import { useState } from 'react';
import VideoUpload from '@/components/VideoUpload';
import VideoGallery from '@/components/VideoGallery';

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUploadComplete = () => {
    // Refresh the gallery when a new video is uploaded
    setRefreshKey(prev => prev + 1);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            Editto AI Video Editor
          </h1>
          <p className="text-xl text-gray-300">
            Edit your videos with simple text instructions
          </p>
        </div>

        {/* Upload Section */}
        <div className="mb-12">
          <VideoUpload onUploadComplete={handleUploadComplete} />
        </div>

        {/* Gallery Section */}
        <div>
          <VideoGallery key={refreshKey} />
        </div>
      </div>
    </main>
  );
}
