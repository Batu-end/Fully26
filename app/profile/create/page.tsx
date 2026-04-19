'use client';

import React, { useCallback, useState } from 'react';
import { FileText, Loader2, Upload, X } from 'lucide-react';

import {
  backendFormRequest,
  backendJsonRequest,
  getSignedInUserId,
} from '@/lib/backend-api';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

type StepKey =
  | 'parseProfile'
  | 'extractOpportunity'
  | 'analyzeFit'
  | 'generatePositioning'
  | 'generateDraft'
  | 'legacyUpload';

interface StudentEvidence {
  label: string;
  detail: string;
  source_type:
    | 'activity'
    | 'coursework'
    | 'work'
    | 'leadership'
    | 'award'
    | 'project'
    | 'essay'
    | 'self-report'
    | 'other';
}

interface StudentProfile {
  name: string;
  school: string;
  major: string;
  gpa: number | null;
  student_type: string;
  graduation_year: string;
  activities: string[];
  work_experience: string[];
  leadership_signals: string[];
  awards: string[];
  skills: string[];
  interests: string[];
  financial_need_flag: boolean;
  identity_flags_opt_in: string[];
  core_story_themes: string[];
  evidence_bank: StudentEvidence[];
  career_goals: string[];
}

interface OpportunityRequirement {
  requirement: string;
  category:
    | 'academic'
    | 'citizenship'
    | 'location'
    | 'experience'
    | 'skills'
    | 'materials'
    | 'timing'
    | 'other';
  strictness: 'required' | 'preferred' | 'unclear';
  notes: string;
}

interface OpportunityEstimatedEffort {
  time_hours_low: number;
  time_hours_high: number;
  writing_load: 'none' | 'short-response' | 'essay-heavy';
  effort_level: 'low' | 'medium' | 'high';
}

interface OpportunityIntelligence {
  title: string;
  provider: string;
  opportunity_type:
    | 'scholarship'
    | 'internship'
    | 'fellowship'
    | 'research'
    | 'lab'
    | 'grant'
    | 'field'
    | 'other';
  amount_or_stipend: string;
  deadline: string;
  location: string;
  raw_theme: string;
  hard_requirements: OpportunityRequirement[];
  soft_preferences: string[];
  essay_themes: string[];
  required_materials: string[];
  estimated_effort: OpportunityEstimatedEffort;
  red_flags: string[];
  opportunity_cluster: string;
}

interface FitAnalysis {
  eligible: boolean | null;
  hard_filter_failures: string[];
  fit_signals: string[];
  fit_gaps: string[];
  semantic_fit_score: number;
  narrative_alignment_score: number;
  reasoning: string;
}

interface Positioning {
  best_angle: string;
  why_this_angle: string;
  evidence_to_use: string[];
  things_to_avoid: string[];
  missing_story_piece: string;
}

interface DraftField {
  field: string;
  value: string;
  confidence: number;
}

interface Draft {
  autofilled_fields: DraftField[];
  draft_answer: string;
  draft_outline: string[];
  user_edit_required: string[];
}

interface ParseProfileResponse {
  student_profile: StudentProfile;
}

interface ExtractOpportunityResponse {
  opportunity: OpportunityIntelligence;
}

interface AnalyzeFitResponse {
  fit_analysis: FitAnalysis;
}

interface GeneratePositioningResponse {
  positioning: Positioning;
}

interface GenerateDraftResponse {
  draft: Draft;
}

interface LegacyResumeResponse {
  text_preview?: string;
}

interface StudentFormState {
  name: string;
  school: string;
  major: string;
  gpa: string;
  studentType: string;
  graduationYear: string;
  activities: string;
  workExperience: string;
  leadershipSignals: string;
  awards: string;
  skills: string;
  interests: string;
  careerGoals: string;
  identityFlagsOptIn: string;
  financialNeedFlag: boolean;
}

const textareaClassName =
  'flex min-h-[120px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50';

const initialLoadingState: Record<StepKey, boolean> = {
  parseProfile: false,
  extractOpportunity: false,
  analyzeFit: false,
  generatePositioning: false,
  generateDraft: false,
  legacyUpload: false,
};

const initialStudentForm: StudentFormState = {
  name: '',
  school: '',
  major: '',
  gpa: '',
  studentType: '',
  graduationYear: '',
  activities: '',
  workExperience: '',
  leadershipSignals: '',
  awards: '',
  skills: '',
  interests: '',
  careerGoals: '',
  identityFlagsOptIn: '',
  financialNeedFlag: false,
};

function parseList(value: string) {
  return value
    .split(/\r?\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function prettyJson(value: unknown) {
  return JSON.stringify(value, null, 2);
}

function buildFormDataPayload(studentForm: StudentFormState) {
  const formData: Record<string, unknown> = {};

  if (studentForm.name.trim()) {
    formData.name = studentForm.name.trim();
  }
  if (studentForm.school.trim()) {
    formData.school = studentForm.school.trim();
  }
  if (studentForm.major.trim()) {
    formData.major = studentForm.major.trim();
  }
  if (studentForm.gpa.trim()) {
    const parsedGpa = Number(studentForm.gpa);
    if (!Number.isNaN(parsedGpa)) {
      formData.gpa = parsedGpa;
    }
  }
  if (studentForm.studentType.trim()) {
    formData.student_type = studentForm.studentType.trim();
  }
  if (studentForm.graduationYear.trim()) {
    formData.graduation_year = studentForm.graduationYear.trim();
  }
  if (studentForm.activities.trim()) {
    formData.activities = parseList(studentForm.activities);
  }
  if (studentForm.workExperience.trim()) {
    formData.work_experience = parseList(studentForm.workExperience);
  }
  if (studentForm.leadershipSignals.trim()) {
    formData.leadership_signals = parseList(studentForm.leadershipSignals);
  }
  if (studentForm.awards.trim()) {
    formData.awards = parseList(studentForm.awards);
  }
  if (studentForm.skills.trim()) {
    formData.skills = parseList(studentForm.skills);
  }
  if (studentForm.interests.trim()) {
    formData.interests = parseList(studentForm.interests);
  }
  if (studentForm.careerGoals.trim()) {
    formData.career_goals = parseList(studentForm.careerGoals);
  }
  if (studentForm.identityFlagsOptIn.trim()) {
    formData.identity_flags_opt_in = parseList(studentForm.identityFlagsOptIn);
  }

  if (studentForm.financialNeedFlag) {
    formData.financial_need_flag = true;
  }

  return Object.keys(formData).length > 0 ? formData : undefined;
}

export default function CreateProfilePage() {
  const [resumeText, setResumeText] = useState('');
  const [opportunityText, setOpportunityText] = useState('');
  const [essayPrompt, setEssayPrompt] = useState('');
  const [applicationPrompt, setApplicationPrompt] = useState('');
  const [studentForm, setStudentForm] = useState(initialStudentForm);

  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(
    null,
  );
  const [opportunity, setOpportunity] =
    useState<OpportunityIntelligence | null>(null);
  const [fitAnalysis, setFitAnalysis] = useState<FitAnalysis | null>(null);
  const [positioning, setPositioning] = useState<Positioning | null>(null);
  const [draft, setDraft] = useState<Draft | null>(null);

  const [loadingState, setLoadingState] =
    useState<Record<StepKey, boolean>>(initialLoadingState);
  const [stepErrors, setStepErrors] = useState<Partial<Record<StepKey, string>>>(
    {},
  );

  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [legacyPreview, setLegacyPreview] = useState('');

  const isAnyAiStepLoading =
    loadingState.parseProfile ||
    loadingState.extractOpportunity ||
    loadingState.analyzeFit ||
    loadingState.generatePositioning ||
    loadingState.generateDraft;

  const updateStudentForm =
    (field: keyof StudentFormState) =>
    (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const value = event.target.value;
      setStudentForm((current) => ({ ...current, [field]: value }));
    };

  const setStepError = (step: StepKey, message: string | null) => {
    setStepErrors((current) => {
      if (!message) {
        const next = { ...current };
        delete next[step];
        return next;
      }
      return { ...current, [step]: message };
    });
  };

  async function runStep<T>(step: StepKey, action: () => Promise<T>) {
    setLoadingState((current) => ({ ...current, [step]: true }));
    setStepError(step, null);

    try {
      return await action();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Something went wrong.';
      setStepError(step, message);
      throw error;
    } finally {
      setLoadingState((current) => ({ ...current, [step]: false }));
    }
  }

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  }, []);

  const validatePdf = useCallback((selectedFile: File | null) => {
    if (!selectedFile) {
      return 'Please upload a PDF file.';
    }

    if (selectedFile.type !== 'application/pdf') {
      return 'Please upload a PDF file.';
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      return 'File must be under 10MB.';
    }

    return null;
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      event.stopPropagation();
      setIsDragging(false);

      const droppedFile = event.dataTransfer.files[0] || null;
      const validationMessage = validatePdf(droppedFile);

      if (validationMessage) {
        setStepError('legacyUpload', validationMessage);
        return;
      }

      setFile(droppedFile);
      setStepError('legacyUpload', null);
    },
    [validatePdf],
  );

  const onFileChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = event.target.files?.[0] || null;
      const validationMessage = validatePdf(selectedFile);

      if (validationMessage) {
        setStepError('legacyUpload', validationMessage);
        return;
      }

      setFile(selectedFile);
      setStepError('legacyUpload', null);
    },
    [validatePdf],
  );

  const removeFile = useCallback(() => {
    setFile(null);
  }, []);

  const parseProfileStep = async () => {
    const formDataPayload = buildFormDataPayload(studentForm);

    if (!resumeText.trim() && !formDataPayload) {
      const message =
        'Add resume text or a few structured student details before parsing.';
      setStepError('parseProfile', message);
      throw new Error(message);
    }

    const response = await runStep('parseProfile', () =>
      backendJsonRequest<ParseProfileResponse>('/api/ai/parse-profile', {
        resume_text: resumeText.trim() || null,
        form_data: formDataPayload,
        source_type: 'frontend-demo',
        source_label: 'profile-create-page',
      }),
    );

    setStudentProfile(response.student_profile);
    setFitAnalysis(null);
    setPositioning(null);
    setDraft(null);
    return response.student_profile;
  };

  const extractOpportunityStep = async () => {
    if (!opportunityText.trim()) {
      const message = 'Paste an ocean-related opportunity before extracting.';
      setStepError('extractOpportunity', message);
      throw new Error(message);
    }

    const response = await runStep('extractOpportunity', () =>
      backendJsonRequest<ExtractOpportunityResponse>(
        '/api/ai/extract-opportunity',
        {
          raw_text: opportunityText.trim(),
          source_type: 'frontend-demo',
          source_label: 'profile-create-page',
        },
      ),
    );

    setOpportunity(response.opportunity);
    setFitAnalysis(null);
    setPositioning(null);
    setDraft(null);
    return response.opportunity;
  };

  const analyzeFitStep = async (
    nextStudentProfile?: StudentProfile,
    nextOpportunity?: OpportunityIntelligence,
  ) => {
    const profileToUse = nextStudentProfile || studentProfile;
    const opportunityToUse = nextOpportunity || opportunity;

    if (!profileToUse || !opportunityToUse) {
      const message =
        'Parse a student profile and extract an opportunity before analyzing fit.';
      setStepError('analyzeFit', message);
      throw new Error(message);
    }

    const response = await runStep('analyzeFit', () =>
      backendJsonRequest<AnalyzeFitResponse>('/api/ai/analyze-fit', {
        student_profile: profileToUse,
        opportunity: opportunityToUse,
      }),
    );

    setFitAnalysis(response.fit_analysis);
    setPositioning(null);
    setDraft(null);
    return response.fit_analysis;
  };

  const generatePositioningStep = async (
    nextStudentProfile?: StudentProfile,
    nextOpportunity?: OpportunityIntelligence,
    nextFitAnalysis?: FitAnalysis,
  ) => {
    const profileToUse = nextStudentProfile || studentProfile;
    const opportunityToUse = nextOpportunity || opportunity;
    const fitToUse = nextFitAnalysis || fitAnalysis;

    if (!profileToUse || !opportunityToUse || !fitToUse) {
      const message =
        'Analyze fit before generating strategic positioning guidance.';
      setStepError('generatePositioning', message);
      throw new Error(message);
    }

    const response = await runStep('generatePositioning', () =>
      backendJsonRequest<GeneratePositioningResponse>(
        '/api/ai/generate-positioning',
        {
          student_profile: profileToUse,
          opportunity: opportunityToUse,
          fit_analysis: fitToUse,
        },
      ),
    );

    setPositioning(response.positioning);
    setDraft(null);
    return response.positioning;
  };

  const generateDraftStep = async (
    nextStudentProfile?: StudentProfile,
    nextOpportunity?: OpportunityIntelligence,
    nextPositioning?: Positioning,
  ) => {
    const profileToUse = nextStudentProfile || studentProfile;
    const opportunityToUse = nextOpportunity || opportunity;
    const positioningToUse = nextPositioning || positioning;

    if (!profileToUse || !opportunityToUse || !positioningToUse) {
      const message =
        'Generate positioning before asking for a first application draft.';
      setStepError('generateDraft', message);
      throw new Error(message);
    }

    const response = await runStep('generateDraft', () =>
      backendJsonRequest<GenerateDraftResponse>('/api/ai/generate-draft', {
        student_profile: profileToUse,
        opportunity: opportunityToUse,
        positioning: positioningToUse,
        essay_prompt: essayPrompt.trim() || null,
        application_prompt: applicationPrompt.trim() || null,
      }),
    );

    setDraft(response.draft);
    return response.draft;
  };

  const handleRunFullDemo = async () => {
    try {
      const parsedProfile = await parseProfileStep();
      const extractedOpportunity = await extractOpportunityStep();
      const nextFitAnalysis = await analyzeFitStep(
        parsedProfile,
        extractedOpportunity,
      );
      const nextPositioning = await generatePositioningStep(
        parsedProfile,
        extractedOpportunity,
        nextFitAnalysis,
      );
      await generateDraftStep(
        parsedProfile,
        extractedOpportunity,
        nextPositioning,
      );
    } catch {
      // step-level errors are already surfaced in the UI
    }
  };

  const handleLegacyUpload = async (event: React.FormEvent) => {
    event.preventDefault();

    const validationMessage = validatePdf(file);

    if (validationMessage) {
      setStepError('legacyUpload', validationMessage);
      return;
    }

    const formData = new FormData();
    formData.append('file', file as File);

    try {
      const result = await runStep('legacyUpload', async () => {
        const userId = await getSignedInUserId();
        return backendFormRequest<LegacyResumeResponse>(
          `/api/students/${userId}/analyze-resume`,
          formData,
        );
      });

      const preview = result.text_preview || '';
      setLegacyPreview(preview);

      if (preview) {
        setResumeText(preview);
      }
    } catch {
      // error is already shown inline
    }
  };

  return (
    <div className='container max-w-6xl py-10'>
      <div className='mb-8 space-y-2'>
        <h1 className='text-3xl font-semibold tracking-tight'>
          Ocean Opportunity Strategist
        </h1>
        <p className='max-w-3xl text-sm text-muted-foreground md:text-base'>
          This page is the safest frontend demo path for the merged AI layer.
          Paste resume text and an ocean-related opportunity, run the existing
          backend AI routes in sequence, and review each canonical result before
          moving to the next step.
        </p>
      </div>

      <div className='grid gap-6 lg:grid-cols-[1.1fr_0.9fr]'>
        <div className='space-y-6'>
          <Card>
            <CardHeader>
              <CardTitle>Main Demo Inputs</CardTitle>
              <CardDescription>
                The primary path is text-based so the frontend stays aligned to
                the current AI contracts and does not depend on database
                persistence.
              </CardDescription>
            </CardHeader>
            <CardContent className='space-y-8'>
              <div className='space-y-2'>
                <Label htmlFor='resume-text'>Resume or profile text</Label>
                <textarea
                  id='resume-text'
                  className={textareaClassName}
                  placeholder='Paste resume text, a LinkedIn summary, or notes about the student.'
                  value={resumeText}
                  onChange={(event) => setResumeText(event.target.value)}
                />
              </div>

              <div className='space-y-4'>
                <div>
                  <h2 className='text-sm font-medium'>
                    Optional structured student fields
                  </h2>
                  <p className='text-sm text-muted-foreground'>
                    These values are sent as `form_data` and can override what
                    the backend infers from the pasted resume text.
                  </p>
                </div>

                <div className='grid gap-4 md:grid-cols-2'>
                  <div className='space-y-2'>
                    <Label htmlFor='student-name'>Name</Label>
                    <Input
                      id='student-name'
                      value={studentForm.name}
                      onChange={updateStudentForm('name')}
                      placeholder='Jamie Rivera'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='student-school'>School</Label>
                    <Input
                      id='student-school'
                      value={studentForm.school}
                      onChange={updateStudentForm('school')}
                      placeholder='University of Washington'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='student-major'>Major</Label>
                    <Input
                      id='student-major'
                      value={studentForm.major}
                      onChange={updateStudentForm('major')}
                      placeholder='Oceanography'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='student-gpa'>GPA</Label>
                    <Input
                      id='student-gpa'
                      value={studentForm.gpa}
                      onChange={updateStudentForm('gpa')}
                      placeholder='3.72'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='student-type'>Student type</Label>
                    <Input
                      id='student-type'
                      value={studentForm.studentType}
                      onChange={updateStudentForm('studentType')}
                      placeholder='undergraduate'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='graduation-year'>Graduation year</Label>
                    <Input
                      id='graduation-year'
                      value={studentForm.graduationYear}
                      onChange={updateStudentForm('graduationYear')}
                      placeholder='2027'
                    />
                  </div>
                </div>

                <div className='grid gap-4 md:grid-cols-2'>
                  <div className='space-y-2'>
                    <Label htmlFor='activities'>Activities</Label>
                    <textarea
                      id='activities'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.activities}
                      onChange={updateStudentForm('activities')}
                      placeholder='Comma or line-separated'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='work-experience'>Work experience</Label>
                    <textarea
                      id='work-experience'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.workExperience}
                      onChange={updateStudentForm('workExperience')}
                      placeholder='Comma or line-separated'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='leadership-signals'>
                      Leadership signals
                    </Label>
                    <textarea
                      id='leadership-signals'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.leadershipSignals}
                      onChange={updateStudentForm('leadershipSignals')}
                      placeholder='Club president, team lead, mentor...'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='awards'>Awards</Label>
                    <textarea
                      id='awards'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.awards}
                      onChange={updateStudentForm('awards')}
                      placeholder='Scholarships, honors, recognitions'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='skills'>Skills</Label>
                    <textarea
                      id='skills'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.skills}
                      onChange={updateStudentForm('skills')}
                      placeholder='Python, GIS, field sampling, data analysis'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='interests'>Interests</Label>
                    <textarea
                      id='interests'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.interests}
                      onChange={updateStudentForm('interests')}
                      placeholder='Marine policy, conservation, climate justice'
                    />
                  </div>
                </div>

                <div className='grid gap-4 md:grid-cols-2'>
                  <div className='space-y-2'>
                    <Label htmlFor='career-goals'>Career goals</Label>
                    <textarea
                      id='career-goals'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.careerGoals}
                      onChange={updateStudentForm('careerGoals')}
                      placeholder='Blue economy, marine robotics, ocean conservation'
                    />
                  </div>
                  <div className='space-y-2'>
                    <Label htmlFor='identity-flags'>
                      Identity flags opt-in
                    </Label>
                    <textarea
                      id='identity-flags'
                      className={cn(textareaClassName, 'min-h-[96px]')}
                      value={studentForm.identityFlagsOptIn}
                      onChange={updateStudentForm('identityFlagsOptIn')}
                      placeholder='First-generation, low-income, veteran'
                    />
                  </div>
                </div>

                <div className='flex items-center gap-3 rounded-md border p-3'>
                  <Checkbox
                    id='financial-need-flag'
                    checked={studentForm.financialNeedFlag}
                    onCheckedChange={(checked) =>
                      setStudentForm((current) => ({
                        ...current,
                        financialNeedFlag: checked === true,
                      }))
                    }
                  />
                  <div className='space-y-1'>
                    <Label htmlFor='financial-need-flag'>
                      Financial need flag
                    </Label>
                    <p className='text-sm text-muted-foreground'>
                      Include this only if the student wants it considered in
                      the AI profile contract.
                    </p>
                  </div>
                </div>
              </div>

              <div className='space-y-2'>
                <Label htmlFor='opportunity-text'>Ocean opportunity text</Label>
                <textarea
                  id='opportunity-text'
                  className={textareaClassName}
                  placeholder='Paste the scholarship, internship, fellowship, or research opportunity text here.'
                  value={opportunityText}
                  onChange={(event) => setOpportunityText(event.target.value)}
                />
              </div>

              <div className='grid gap-4 md:grid-cols-2'>
                <div className='space-y-2'>
                  <Label htmlFor='essay-prompt'>Essay prompt</Label>
                  <textarea
                    id='essay-prompt'
                    className={cn(textareaClassName, 'min-h-[96px]')}
                    placeholder='Optional. If both prompts are filled in, the backend prefers this one.'
                    value={essayPrompt}
                    onChange={(event) => setEssayPrompt(event.target.value)}
                  />
                </div>
                <div className='space-y-2'>
                  <Label htmlFor='application-prompt'>Application prompt</Label>
                  <textarea
                    id='application-prompt'
                    className={cn(textareaClassName, 'min-h-[96px]')}
                    placeholder='Optional backup prompt for draft generation.'
                    value={applicationPrompt}
                    onChange={(event) =>
                      setApplicationPrompt(event.target.value)
                    }
                  />
                </div>
              </div>
            </CardContent>

            <CardFooter className='flex flex-wrap gap-3'>
              <Button
                type='button'
                onClick={handleRunFullDemo}
                disabled={isAnyAiStepLoading}
              >
                {isAnyAiStepLoading ? (
                  <>
                    <Loader2 className='h-4 w-4 animate-spin' />
                    Running demo...
                  </>
                ) : (
                  'Run Full AI Demo'
                )}
              </Button>
              <Button
                type='button'
                variant='outline'
                onClick={() => void parseProfileStep()}
                disabled={loadingState.parseProfile}
              >
                {loadingState.parseProfile ? (
                  <>
                    <Loader2 className='h-4 w-4 animate-spin' />
                    Parsing...
                  </>
                ) : (
                  'Parse Profile'
                )}
              </Button>
              <Button
                type='button'
                variant='outline'
                onClick={() => void extractOpportunityStep()}
                disabled={loadingState.extractOpportunity}
              >
                {loadingState.extractOpportunity ? (
                  <>
                    <Loader2 className='h-4 w-4 animate-spin' />
                    Extracting...
                  </>
                ) : (
                  'Extract Opportunity'
                )}
              </Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Legacy PDF Import</CardTitle>
              <CardDescription>
                Secondary path only. This still calls the existing resume
                endpoint, then copies the returned text preview into the main
                resume text box so you can continue through the AI flow.
              </CardDescription>
            </CardHeader>

            <form onSubmit={handleLegacyUpload}>
              <CardContent className='space-y-4'>
                <div
                  onDragOver={onDragOver}
                  onDragLeave={onDragLeave}
                  onDrop={onDrop}
                  className={cn(
                    'relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-lg border-2 border-dashed p-8 transition-colors',
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
                    <div className='flex w-full max-w-xs items-center gap-3 rounded-md border bg-background p-3 shadow-sm'>
                      <FileText className='h-8 w-8 shrink-0 text-blue-500' />
                      <div className='min-w-0 flex-1'>
                        <p className='truncate text-sm font-medium'>
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
                        onClick={(event) => {
                          event.stopPropagation();
                          removeFile();
                        }}
                      >
                        <X className='h-4 w-4' />
                      </Button>
                    </div>
                  ) : (
                    <>
                      <div className='rounded-full bg-muted p-3'>
                        <Upload className='h-6 w-6 text-muted-foreground' />
                      </div>
                      <div className='text-center'>
                        <p className='text-sm font-medium'>
                          Click or drag and drop a resume PDF
                        </p>
                        <p className='text-xs text-muted-foreground'>
                          PDF only, up to 10MB
                        </p>
                      </div>
                    </>
                  )}
                </div>

                {stepErrors.legacyUpload && (
                  <p className='text-sm font-medium text-destructive'>
                    {stepErrors.legacyUpload}
                  </p>
                )}

                {legacyPreview && (
                  <div className='space-y-2 rounded-lg border bg-muted/30 p-4'>
                    <p className='text-sm font-medium'>
                      Resume text preview loaded into the main demo input
                    </p>
                    <pre className='max-h-48 overflow-auto whitespace-pre-wrap text-xs text-muted-foreground'>
                      {legacyPreview}
                    </pre>
                  </div>
                )}
              </CardContent>

              <CardFooter>
                <Button
                  type='submit'
                  variant='outline'
                  disabled={loadingState.legacyUpload}
                >
                  {loadingState.legacyUpload ? (
                    <>
                      <Loader2 className='h-4 w-4 animate-spin' />
                      Importing PDF...
                    </>
                  ) : (
                    'Import PDF as Resume Text'
                  )}
                </Button>
              </CardFooter>
            </form>
          </Card>
        </div>

        <div className='space-y-6'>
          <Card>
            <CardHeader>
              <CardTitle>Parsed Student Profile</CardTitle>
              <CardDescription>
                `POST /api/ai/parse-profile`
              </CardDescription>
            </CardHeader>
            <CardContent className='space-y-4'>
              {stepErrors.parseProfile && (
                <p className='text-sm font-medium text-destructive'>
                  {stepErrors.parseProfile}
                </p>
              )}

              {studentProfile ? (
                <>
                  <div className='grid gap-2 text-sm md:grid-cols-2'>
                    <p>
                      <span className='font-medium'>Name:</span>{' '}
                      {studentProfile.name || 'TBD'}
                    </p>
                    <p>
                      <span className='font-medium'>School:</span>{' '}
                      {studentProfile.school || 'TBD'}
                    </p>
                    <p>
                      <span className='font-medium'>Major:</span>{' '}
                      {studentProfile.major || 'TBD'}
                    </p>
                    <p>
                      <span className='font-medium'>Graduation:</span>{' '}
                      {studentProfile.graduation_year || 'TBD'}
                    </p>
                  </div>
                  <pre className='max-h-80 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs'>
                    {prettyJson(studentProfile)}
                  </pre>
                </>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No parsed profile yet.
                </p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Extracted Opportunity</CardTitle>
              <CardDescription>
                `POST /api/ai/extract-opportunity`
              </CardDescription>
            </CardHeader>
            <CardContent className='space-y-4'>
              {stepErrors.extractOpportunity && (
                <p className='text-sm font-medium text-destructive'>
                  {stepErrors.extractOpportunity}
                </p>
              )}

              {opportunity ? (
                <>
                  <div className='grid gap-2 text-sm md:grid-cols-2'>
                    <p>
                      <span className='font-medium'>Title:</span>{' '}
                      {opportunity.title || 'TBD'}
                    </p>
                    <p>
                      <span className='font-medium'>Provider:</span>{' '}
                      {opportunity.provider || 'TBD'}
                    </p>
                    <p>
                      <span className='font-medium'>Type:</span>{' '}
                      {opportunity.opportunity_type}
                    </p>
                    <p>
                      <span className='font-medium'>Deadline:</span>{' '}
                      {opportunity.deadline || 'TBD'}
                    </p>
                  </div>
                  <pre className='max-h-80 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs'>
                    {prettyJson(opportunity)}
                  </pre>
                </>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No extracted opportunity yet.
                </p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className='flex flex-wrap items-center justify-between gap-3'>
                <div className='space-y-1'>
                  <CardTitle>Fit Analysis</CardTitle>
                  <CardDescription>
                    `POST /api/ai/analyze-fit`
                  </CardDescription>
                </div>
                <Button
                  type='button'
                  variant='outline'
                  onClick={() => void analyzeFitStep()}
                  disabled={loadingState.analyzeFit}
                >
                  {loadingState.analyzeFit ? (
                    <>
                      <Loader2 className='h-4 w-4 animate-spin' />
                      Analyzing...
                    </>
                  ) : (
                    'Analyze Fit'
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent className='space-y-4'>
              {stepErrors.analyzeFit && (
                <p className='text-sm font-medium text-destructive'>
                  {stepErrors.analyzeFit}
                </p>
              )}

              {fitAnalysis ? (
                <>
                  <div className='grid gap-2 text-sm md:grid-cols-2'>
                    <p>
                      <span className='font-medium'>Eligible:</span>{' '}
                      {fitAnalysis.eligible === null
                        ? 'unclear'
                        : fitAnalysis.eligible
                          ? 'yes'
                          : 'no'}
                    </p>
                    <p>
                      <span className='font-medium'>Semantic fit:</span>{' '}
                      {fitAnalysis.semantic_fit_score}
                    </p>
                    <p>
                      <span className='font-medium'>Narrative alignment:</span>{' '}
                      {fitAnalysis.narrative_alignment_score}
                    </p>
                    <p>
                      <span className='font-medium'>Hard filter failures:</span>{' '}
                      {fitAnalysis.hard_filter_failures.length}
                    </p>
                  </div>
                  <pre className='max-h-80 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs'>
                    {prettyJson(fitAnalysis)}
                  </pre>
                </>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No fit analysis yet.
                </p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className='flex flex-wrap items-center justify-between gap-3'>
                <div className='space-y-1'>
                  <CardTitle>Positioning</CardTitle>
                  <CardDescription>
                    `POST /api/ai/generate-positioning`
                  </CardDescription>
                </div>
                <Button
                  type='button'
                  variant='outline'
                  onClick={() => void generatePositioningStep()}
                  disabled={loadingState.generatePositioning}
                >
                  {loadingState.generatePositioning ? (
                    <>
                      <Loader2 className='h-4 w-4 animate-spin' />
                      Generating...
                    </>
                  ) : (
                    'Generate Positioning'
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent className='space-y-4'>
              {stepErrors.generatePositioning && (
                <p className='text-sm font-medium text-destructive'>
                  {stepErrors.generatePositioning}
                </p>
              )}

              {positioning ? (
                <>
                  <div className='space-y-2 text-sm'>
                    <p>
                      <span className='font-medium'>Best angle:</span>{' '}
                      {positioning.best_angle}
                    </p>
                    <p>
                      <span className='font-medium'>Missing story piece:</span>{' '}
                      {positioning.missing_story_piece}
                    </p>
                  </div>
                  <pre className='max-h-80 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs'>
                    {prettyJson(positioning)}
                  </pre>
                </>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No positioning guidance yet.
                </p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className='flex flex-wrap items-center justify-between gap-3'>
                <div className='space-y-1'>
                  <CardTitle>Draft</CardTitle>
                  <CardDescription>
                    `POST /api/ai/generate-draft`
                  </CardDescription>
                </div>
                <Button
                  type='button'
                  variant='outline'
                  onClick={() => void generateDraftStep()}
                  disabled={loadingState.generateDraft}
                >
                  {loadingState.generateDraft ? (
                    <>
                      <Loader2 className='h-4 w-4 animate-spin' />
                      Drafting...
                    </>
                  ) : (
                    'Generate Draft'
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent className='space-y-4'>
              {stepErrors.generateDraft && (
                <p className='text-sm font-medium text-destructive'>
                  {stepErrors.generateDraft}
                </p>
              )}

              {draft ? (
                <>
                  <div className='space-y-2 text-sm'>
                    <p className='font-medium'>Draft answer preview</p>
                    <p className='rounded-lg border bg-muted/30 p-4 whitespace-pre-wrap'>
                      {draft.draft_answer}
                    </p>
                  </div>
                  <pre className='max-h-80 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs'>
                    {prettyJson(draft)}
                  </pre>
                </>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No draft yet.
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
