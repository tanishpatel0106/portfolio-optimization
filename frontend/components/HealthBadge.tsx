'use client';

import { useQuery } from '@tanstack/react-query';

import { fetcher } from '../lib/api';

export default function HealthBadge() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['health'],
    queryFn: () => fetcher<{ status: string }>('/health'),
    retry: 2,
  });

  let label = 'Checking API...';
  let color = 'text-slate-400';
  if (isLoading) {
    label = 'Checking API...';
  } else if (isError) {
    label = 'API unreachable';
    color = 'text-rose-400';
  } else if (data) {
    label = `API: ${data.status}`;
    color = 'text-emerald-400';
  }

  return <span className={`text-xs ${color}`}>{label}</span>;
}
