import { createClient } from '@/lib/supabase/client';

function getBackendUrl() {
  return process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
}

async function getAccessToken() {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session?.access_token) {
    throw new Error('You must be signed in to use the AI demo.');
  }

  return session.access_token;
}

export async function getSignedInUserId() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user?.id) {
    throw new Error('You must be signed in to use the AI demo.');
  }

  return user.id;
}

async function parseError(response: Response) {
  const text = await response.text();

  try {
    const parsed = JSON.parse(text) as { detail?: string; message?: string };
    if (typeof parsed.detail === 'string') {
      return parsed.detail;
    }
    if (typeof parsed.message === 'string') {
      return parsed.message;
    }
  } catch {
    // fall back to raw text
  }

  return text || `Request failed with status ${response.status}.`;
}

export async function backendJsonRequest<TResponse>(
  path: string,
  body: unknown,
) {
  const accessToken = await getAccessToken();
  const response = await fetch(`${getBackendUrl()}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as TResponse;
}

export async function backendFormRequest<TResponse>(
  path: string,
  formData: FormData,
) {
  const accessToken = await getAccessToken();
  const response = await fetch(`${getBackendUrl()}${path}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as TResponse;
}
