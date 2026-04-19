'use client';

import { motion, useReducedMotion } from 'framer-motion';
import {
  ArrowRight,
  FileText,
  Loader2,
  Radar,
  ScanSearch,
  Sparkles,
  Upload,
  Waves,
  X,
} from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import React, { useCallback, useState } from 'react';

import {
  MetricChip,
  PanelEyebrow,
  PremiumPanel,
} from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { ThemeSwitcher } from '@/components/theme-switcher';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { createClient } from '@/lib/supabase/client';
import { cn } from '@/lib/utils';

const transitionEase = [0.16, 1, 0.3, 1] as const;

export default function CreateProfilePage() {
  const router = useRouter();
  const supabase = createClient();
  const prefersReducedMotion = useReducedMotion();

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
    } catch {
      setError('Something went wrong.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className='hero-stage relative min-h-screen overflow-hidden text-white'>
      <OceanCanvas variant='hero' />
      <div className='hero-vignette absolute inset-0' />

      <div className='hero-content-shell mx-auto flex min-h-screen w-full max-w-7xl flex-col px-5 py-8 md:px-8 md:py-10'>
        <motion.div
          animate={{ opacity: 1, y: 0 }}
          initial={prefersReducedMotion ? false : { opacity: 0, y: 16 }}
          transition={{ duration: 0.9, ease: transitionEase }}
          className='site-nav flex items-center justify-between rounded-[1.8rem] border border-white/10 px-5 py-4'
        >
          <Link
            href='/'
            className='group flex items-center gap-3'
          >
            <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/20 bg-cyan-300/10 shadow-[0_0_32px_rgba(90,245,255,0.12)]'>
              <Waves className='h-5 w-5 text-cyan-100' />
            </div>
            <div>
              <div className='text-xs uppercase tracking-[0.3em] text-cyan-100/48'>
                DeepScholar
              </div>
              <div className='text-sm text-white/84 group-hover:text-cyan-100'>
                Immersive intake sequence
              </div>
            </div>
          </Link>

          <div className='flex items-center gap-3'>
            <ThemeSwitcher />
            <Link
              href='/dashboard'
              className='rounded-full border border-white/12 bg-white/[0.05] px-4 py-2 text-sm text-white/84 backdrop-blur-xl transition hover:border-cyan-200/25 hover:bg-white/[0.08] hover:text-white'
            >
              Mission control
            </Link>
          </div>
        </motion.div>

        <div className='grid flex-1 items-center gap-10 py-10 lg:grid-cols-[0.92fr_1.08fr] lg:gap-14'>
          <motion.section
            animate={{ opacity: 1, x: 0 }}
            initial={prefersReducedMotion ? false : { opacity: 0, x: -22 }}
            transition={{ duration: 1.05, ease: transitionEase, delay: 0.08 }}
            className='max-w-2xl'
          >
            <div className='hero-copy-panel rounded-[2rem] p-6 md:p-7'>
              <PanelEyebrow>Bioluminescent profile intake</PanelEyebrow>
              <h1 className='ocean-title mt-6 text-5xl font-semibold leading-[0.92] md:text-7xl'>
                Enter a premium deep-sea research interface.
              </h1>
              <p className='ocean-copy mt-6 max-w-xl text-lg leading-8 md:text-xl'>
                Upload your resume and let the platform establish the first
                layer of profile signal inside a living ocean-tech environment
                built to feel calm, elite, and unforgettable.
              </p>

              <div className='mt-8 flex flex-wrap gap-3'>
                <MetricChip label='Environment' value='Live abyss scene' />
                <MetricChip label='Input' value='PDF resume upload' />
                <MetricChip label='Output' value='Profile signal foundation' />
              </div>
            </div>

            <div className='mt-6 grid gap-4 md:grid-cols-2'>
              <motion.div
                animate={{ opacity: 1, y: 0 }}
                initial={prefersReducedMotion ? false : { opacity: 0, y: 20 }}
                transition={{ duration: 0.95, ease: transitionEase, delay: 0.18 }}
              >
                <PremiumPanel className='min-h-[12.5rem]'>
                  <div className='flex items-center gap-3 text-cyan-100/82'>
                    <ScanSearch className='h-5 w-5' />
                    <span className='text-[0.68rem] uppercase tracking-[0.26em]'>
                      Parse profile
                    </span>
                  </div>
                  <p className='mt-4 text-sm leading-7 text-white/74'>
                    The intake pass establishes a structured read on your
                    background so the next product surfaces can prioritize fit,
                    signal, and direction with more clarity.
                  </p>
                </PremiumPanel>
              </motion.div>

              <motion.div
                animate={{ opacity: 1, y: 0 }}
                initial={prefersReducedMotion ? false : { opacity: 0, y: 20 }}
                transition={{ duration: 0.95, ease: transitionEase, delay: 0.26 }}
              >
                <PremiumPanel className='min-h-[12.5rem]'>
                  <div className='flex items-center gap-3 text-cyan-100/82'>
                    <Radar className='h-5 w-5' />
                    <span className='text-[0.68rem] uppercase tracking-[0.26em]'>
                      Next surface
                    </span>
                  </div>
                  <p className='mt-4 text-sm leading-7 text-white/74'>
                    Once uploaded, the flow moves directly into mission control
                    so the opportunity radar, fit analysis, and writing support
                    can carry the second act of the demo.
                  </p>
                </PremiumPanel>
              </motion.div>
            </div>
          </motion.section>

          <motion.aside
            animate={{ opacity: 1, x: 0 }}
            initial={prefersReducedMotion ? false : { opacity: 0, x: 24 }}
            transition={{ duration: 1.05, ease: transitionEase, delay: 0.14 }}
            className='mx-auto w-full max-w-2xl'
          >
            <PremiumPanel tone='bright' className='overflow-hidden'>
              <div className='flex items-start justify-between gap-4'>
                <div>
                  <PanelEyebrow>Resume upload</PanelEyebrow>
                  <h2 className='mt-5 text-3xl font-semibold text-white md:text-[2.15rem]'>
                    Build the first layer of ocean profile intelligence.
                  </h2>
                </div>
                <div className='hidden rounded-full border border-cyan-200/16 bg-cyan-300/10 p-3 text-cyan-100 md:block'>
                  <Sparkles className='h-5 w-5' />
                </div>
              </div>

              <form
                onSubmit={handleSubmit}
                className='mt-8 flex flex-col gap-6'
              >
                <div>
                  <Label className='text-sm uppercase tracking-[0.22em] text-cyan-100/60'>
                    Resume / PDF
                  </Label>

                  <div
                    onDragOver={onDragOver}
                    onDragLeave={onDragLeave}
                    onDrop={onDrop}
                    onClick={() =>
                      !file && document.getElementById('resume-upload')?.click()
                    }
                    className={cn(
                      'mt-4 cursor-pointer rounded-[1.9rem] border-2 border-dashed p-8 transition duration-300 md:p-10',
                      isDragging
                        ? 'border-cyan-300 bg-cyan-300/10 shadow-[0_0_0_1px_rgba(128,248,255,0.25),0_0_40px_rgba(86,241,255,0.12)]'
                        : 'border-white/12 bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.025))] hover:border-cyan-200/26 hover:bg-white/[0.07]',
                      file && 'border-cyan-200/20 bg-white/[0.07]',
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
                      <div className='flex flex-col gap-5 sm:flex-row sm:items-center'>
                        <div className='hero-glow-ring flex h-16 w-16 items-center justify-center rounded-[1.6rem] border border-cyan-200/14 bg-cyan-300/10'>
                          <FileText className='h-7 w-7 text-cyan-100' />
                        </div>

                        <div className='min-w-0 flex-1'>
                          <p className='truncate text-base font-medium text-white'>
                            {file.name}
                          </p>
                          <p className='mt-1 text-sm text-blue-50/56'>
                            {(file.size / 1024).toFixed(1)} KB uploaded and ready
                            for parsing
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
                          className='rounded-full border border-white/10 bg-white/[0.04] text-white/80 hover:bg-white/[0.08] hover:text-white'
                        >
                          <X className='h-4 w-4' />
                        </Button>
                      </div>
                    ) : (
                      <div className='flex flex-col items-center gap-5 text-center'>
                        <div className='hero-glow-ring flex h-16 w-16 items-center justify-center rounded-[1.7rem] border border-cyan-200/18 bg-cyan-300/10'>
                          <Upload className='h-7 w-7 text-cyan-100' />
                        </div>
                        <div>
                          <p className='text-xl font-medium text-white'>
                            Drop your resume into the abyss
                          </p>
                          <p className='mt-2 text-sm leading-7 text-blue-50/62'>
                            Click or drag and drop a PDF to initiate the premium
                            intake sequence.
                          </p>
                        </div>
                        <p className='text-xs uppercase tracking-[0.24em] text-cyan-100/42'>
                          PDF only / up to 10 MB
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {error ? (
                  <div className='rounded-2xl border border-red-400/20 bg-red-400/8 px-4 py-3 text-sm text-red-200'>
                    {error}
                  </div>
                ) : null}

                <div className='grid gap-3 md:grid-cols-[1fr_auto] md:items-center'>
                  <Button
                    type='submit'
                    disabled={isLoading}
                    className='h-12 rounded-full bg-cyan-300 text-slate-950 shadow-[0_18px_38px_rgba(99,245,255,0.24)] transition hover:bg-cyan-200'
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                        Parsing resume
                      </>
                    ) : (
                      'Generate my ocean profile'
                    )}
                  </Button>

                  <div className='inline-flex items-center gap-2 text-sm text-cyan-100/68'>
                    <ArrowRight className='h-4 w-4' />
                    Dashboard follows next
                  </div>
                </div>

                <div className='rounded-[1.45rem] border border-white/10 bg-white/[0.035] px-4 py-4 text-sm leading-7 text-blue-50/58'>
                  Your upload flow and backend contract remain unchanged in this
                  pass. Phase 1 focuses entirely on the atmosphere, staging, and
                  premium visual presentation around the existing intake logic.
                </div>
              </form>
            </PremiumPanel>
          </motion.aside>
        </div>
      </div>
    </main>
  );
}
