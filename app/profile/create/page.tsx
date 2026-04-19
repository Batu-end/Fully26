'use client';

import React, { useCallback, useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';

import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

import { Upload, FileText, X, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function CreateProfilePage() {
  const router = useRouter();
  const supabase = createClient();

  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
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

  const removeFile = useCallback(() => {
    setFile(null);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      setError('Please upload your resume.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Get user + session
      const {
        data: { user },
      } = await supabase.auth.getUser();

      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!user || !session) {
        throw new Error('You must be signed in.');
      }

      // Prepare upload
      const formData = new FormData();
      formData.append('file', file);

      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

      // Send request
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
        const text = await response.text();
        console.error('Backend error:', text);
        throw new Error('Failed to upload resume.');
      }

      const result = await response.json();
      console.log('AI Backend Response:', result);

      // Success → go to dashboard
      router.push('/dashboard');
      router.refresh();
    } catch (err: any) {
      console.error('Submission error:', err);
      setError(err.message || 'Something went wrong.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='container max-w-2xl py-10'>
      <Card>
        <CardHeader>
          <CardTitle className='text-2xl'>Create Your Profile</CardTitle>
          <CardDescription>
            Upload your resume to generate your student profile.
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className='space-y-6'>
            <div className='space-y-2'>
              <Label>Resume (PDF)</Label>

              <div
                onDragOver={onDragOver}
                onDragLeave={onDragLeave}
                onDrop={onDrop}
                className={cn(
                  'relative border-2 border-dashed rounded-lg p-8 transition-colors flex flex-col items-center justify-center gap-4 cursor-pointer',
                  isDragging
                    ? 'border-primary bg-primary/5'
                    : 'border-muted-foreground/25 hover:border-primary/50',
                  file ? 'bg-muted/50' : 'bg-transparent',
                )}
                onClick={() =>
                  !file && document.getElementById('resume-upload')?.click()
                }
              >
                <input
                  id='resume-upload'
                  type='file'
                  accept='.pdf'
                  className='hidden'
                  onChange={onFileChange}
                />

                {file ? (
                  <div className='flex items-center gap-3 w-full max-w-xs p-3 bg-background rounded-md border shadow-sm'>
                    <FileText className='h-8 w-8 text-blue-500 shrink-0' />
                    <div className='flex-1 min-w-0'>
                      <p className='text-sm font-medium truncate'>
                        {file.name}
                      </p>
                      <p className='text-xs text-muted-foreground'>
                        {(file.size / 1024).toFixed(1)} KB
                      </p>
                    </div>

                    <Button
                      type='button'
                      variant='ghost'
                      size='icon'
                      className='h-8 w-8'
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
                    <div className='p-3 rounded-full bg-muted'>
                      <Upload className='h-6 w-6 text-muted-foreground' />
                    </div>
                    <div className='text-center'>
                      <p className='text-sm font-medium'>
                        Click or drag & drop to upload
                      </p>
                      <p className='text-xs text-muted-foreground'>
                        PDF only (max 10MB)
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {error && (
              <p className='text-sm text-destructive font-medium'>{error}</p>
            )}
          </CardContent>

          <CardFooter>
            <Button
              type='submit'
              className='w-full'
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                  Uploading...
                </>
              ) : (
                'Create Profile'
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
