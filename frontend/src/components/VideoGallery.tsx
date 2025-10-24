'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Loader2, Clock, CheckCircle, XCircle, Download } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Job {
  id: string;
  instruction: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  original_video_url?: string;
  edited_video_url?: string;
  error_message?: string;
}

export default function VideoGallery() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      setJobs(response.data);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();

    // Poll for updates every 10 seconds
    const interval = setInterval(fetchJobs, 10000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: Job['status']) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-400" />;
      case 'processing':
        return <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-400" />;
    }
  };

  const getStatusText = (status: Job['status']) => {
    switch (status) {
      case 'pending':
        return 'Waiting in queue';
      case 'processing':
        return 'Editing video...';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="w-8 h-8 text-purple-400 animate-spin" />
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p>No videos yet. Upload your first video to get started!</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold text-white mb-6">Your Videos</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="bg-white/10 backdrop-blur-lg rounded-lg p-6 shadow-xl"
          >
            {/* Status Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                {getStatusIcon(job.status)}
                <span className="text-gray-200 font-medium">
                  {getStatusText(job.status)}
                </span>
              </div>
              <span className="text-sm text-gray-400">
                {new Date(job.created_at).toLocaleDateString()}
              </span>
            </div>

            {/* Instruction */}
            <p className="text-white mb-4">
              <span className="text-gray-400">Instruction: </span>
              {job.instruction}
            </p>

            {/* Video Preview */}
            {job.status === 'completed' && job.edited_video_url && (
              <div className="space-y-3">
                <video
                  src={job.edited_video_url}
                  controls
                  className="w-full rounded-lg"
                />
                <a
                  href={job.edited_video_url}
                  download
                  className="flex items-center justify-center gap-2 w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download Edited Video
                </a>
              </div>
            )}

            {/* Original Video (for pending/processing) */}
            {(job.status === 'pending' || job.status === 'processing') && job.original_video_url && (
              <div>
                <p className="text-sm text-gray-400 mb-2">Original Video:</p>
                <video
                  src={job.original_video_url}
                  controls
                  className="w-full rounded-lg"
                />
              </div>
            )}

            {/* Error Message */}
            {job.status === 'failed' && job.error_message && (
              <div className="bg-red-400/10 border border-red-400/30 rounded-lg p-3">
                <p className="text-red-400 text-sm">{job.error_message}</p>
              </div>
            )}

            {/* Job ID */}
            <p className="text-xs text-gray-500 mt-3">Job ID: {job.id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
