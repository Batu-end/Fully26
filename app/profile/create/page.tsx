'use client';

import React, { useCallback, useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';

import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';

import { Upload, FileText, X, Loader2 } from 'lucide-react';

export default function CreateProfilePage() {
  const router = useRouter();
  const supabase = createClient();

  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) return;

    if (droppedFile.type !== 'application/pdf') {
      setError('Please upload a PDF file.');
      return;
    }

    if (droppedFile.size > 10 * 1024 * 1024) {
      setError('File must be under 10MB.');
      return;
    }

    setFile(droppedFile);
    setError(null);
  }, []);

  const onFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    if (selectedFile.type !== 'application/pdf') {
      setError('Please upload a PDF file.');
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File must be under 10MB.');
      return;
    }

    setFile(selectedFile);
    setError(null);
  }, []);

  const removeFile = useCallback(() => setFile(null), []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      setError('Please upload your resume.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!user || !session) {
        throw new Error('You must be signed in.');
      }

      const formData = new FormData();
      formData.append('file', file);

      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

      const response = await fetch(
        `${backendUrl}/api/students/${user.id}/analyze-resume`,
        {
          method: 'POST',
          body: formData,
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        },
      );

      if (!response.ok) {
        throw new Error('Upload failed.');
      }

      await response.json();

      router.push('/dashboard');
      router.refresh();
    } catch (err) {
      setError('Something went wrong.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='min-h-screen w-full bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white flex items-center justify-center px-4'>
      {/* glow */}
      <div className='absolute w-[500px] h-[500px] bg-cyan-400/10 blur-[140px] rounded-full -z-10' />

      <div className='w-full max-w-2xl'>
        {/* HEADER */}
        <div className='text-center mb-10'>
          <h1 className='text-4xl font-bold'>
            Enter the Ocean Intelligence System 🌊
          </h1>

          <p className='text-blue-100/60 mt-3'>
            Upload your resume and we’ll build your AI-powered ocean profile.
          </p>
        </div>

        {/* CARD */}
        <form
          onSubmit={handleSubmit}
          className='rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-6 flex flex-col gap-6'
        >
          <div>
            <Label className='text-white/80'>Resume (PDF)</Label>

            {/* DROPZONE */}
            <div
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onDrop={onDrop}
              onClick={() =>
                !file && document.getElementById('resume-upload')?.click()
              }
              className={cn(
                'mt-3 border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center gap-4 cursor-pointer transition',
                isDragging
                  ? 'border-cyan-400 bg-cyan-400/10'
                  : 'border-white/15 hover:border-cyan-400/40',
                file && 'bg-white/5',
              )}
            >
              <input
                id='resume-upload'
                type='file'
                accept='.pdf'
                className='hidden'
                onChange={onFileChange}
              />

              {file ? (
                <div className='flex items-center gap-3 w-full max-w-sm'>
                  <FileText className='text-cyan-300' />

                  <div className='flex-1'>
                    <p className='text-sm font-medium truncate'>{file.name}</p>
                    <p className='text-xs text-blue-100/50'>
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>

                  <Button
                    type='button'
                    variant='ghost'
                    size='icon'
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile();
                    }}
                  >
                    <X className='h-4 w-4' />
                  </Button>
                </div>
              ) : (
                <>
                  <Upload className='text-cyan-300' />
                  <p className='text-sm text-blue-100/70 text-center'>
                    Click or drag & drop your resume
                  </p>
                  <p className='text-xs text-blue-100/40'>
                    PDF only • Max 10MB
                  </p>
                </>
              )}
            </div>
          </div>

          {error && <p className='text-sm text-red-400'>{error}</p>}

          {/* CTA */}
          <Button
            type='submit'
            disabled={isLoading}
            className='w-full bg-cyan-400 hover:bg-cyan-300 text-slate-900 font-semibold'
          >
            {isLoading ? (
              <>
                <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                Analyzing Resume...
              </>
            ) : (
              'Generate My Ocean Profile'
            )}
          </Button>

          {/* micro explanation */}
          <p className='text-xs text-blue-100/50 text-center'>
            We extract skills, experience, and match you to ocean opportunities.
          </p>
        </form>
      </div>
    </div>
  );
}
