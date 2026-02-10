import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProfile } from '../../api/client';
import DomainBadge from '../shared/DomainBadge';
import CostDisplay from '../shared/CostDisplay';

interface TimelineEvent {
  date: string;
  event: string;
  systems: string[];
  domain: string;
  cost_impact?: number;
  is_gap?: boolean;
  gap_description?: string;
  coordination_would_help?: string;
}

const DOMAIN_COLORS: Record<string, string> = {
  health: '#1A6B3C',
  justice: '#8B1A1A',
  housing: '#1A3D8B',
  income: '#6B5A1A',
  education: '#5A1A6B',
  child_welfare: '#1A6B6B',
};

function generateTimeline(profile: any): TimelineEvent[] {
  const events: TimelineEvent[] = [];
  const circumstances = profile.circumstances || {};
  const name = profile.name || 'This person';

  if (circumstances.has_criminal_justice || circumstances.is_on_probation) {
    events.push({
      date: 'Year 1',
      event: `${name} enters the criminal justice system. Health records from community providers are inaccessible to corrections.`,
      systems: ['doc', 'cjis'],
      domain: 'justice',
      cost_impact: 39800,
      is_gap: true,
      gap_description: 'DOC has no access to community health records',
      coordination_would_help: 'Health record transfer at intake would prevent duplicate testing and medication errors',
    });
  }

  if (circumstances.has_substance_use) {
    events.push({
      date: 'Year 1',
      event: 'Substance use treatment begins. 42 CFR Part 2 blocks treatment records from being shared with other providers.',
      systems: ['bha'],
      domain: 'health',
      cost_impact: 8200,
      is_gap: true,
      gap_description: '42 CFR Part 2 blocks SUD treatment data sharing',
      coordination_would_help: 'Consent-based data sharing would enable coordinated treatment',
    });
  }

  if (circumstances.is_on_medicaid) {
    events.push({
      date: 'Year 1',
      event: 'Enrolled in Medicaid. Claims processing begins but behavioral health data remains siloed.',
      systems: ['mmis', 'mco'],
      domain: 'health',
      cost_impact: 8500,
    });
  }

  if (circumstances.is_homeless) {
    events.push({
      date: 'Year 1-2',
      event: 'Enters emergency shelter. HMIS records housing status but health system doesn\'t know. ER visits for conditions treatable in primary care.',
      systems: ['hmis'],
      domain: 'housing',
      cost_impact: 22400,
      is_gap: true,
      gap_description: 'HMIS disconnected from Medicaid/MCO',
      coordination_would_help: 'Housing status in care plans would enable appropriate prescribing and follow-up',
    });
  }

  if (circumstances.has_foster_care) {
    events.push({
      date: 'Year 1',
      event: 'Placed in foster care. Medicaid coverage lapses during placement change. Health history lost in transition.',
      systems: ['sacwis'],
      domain: 'child_welfare',
      cost_impact: 32000,
      is_gap: true,
      gap_description: 'SACWIS-MMIS interface is batch-only, delays coverage',
      coordination_would_help: 'Real-time SACWIS-MMIS interface + health passport would prevent coverage gaps',
    });
  }

  if (circumstances.is_on_snap) {
    events.push({
      date: 'Year 1',
      event: 'Receives SNAP benefits. Eligibility determination duplicates information already in Medicaid system.',
      systems: ['snap_ebt'],
      domain: 'income',
      cost_impact: 3400,
    });
  }

  if (circumstances.is_on_ssi) {
    events.push({
      date: 'Year 1-2',
      event: 'SSI application filed. Disability determination cannot access behavioral health records due to 42 CFR Part 2. Claim initially denied.',
      systems: ['ssa'],
      domain: 'income',
      cost_impact: 12600,
      is_gap: true,
      gap_description: 'SSA cannot access BHA treatment records',
      coordination_would_help: 'Integrated consent in SSI application would streamline disability evidence',
    });
  }

  if (circumstances.has_children) {
    events.push({
      date: 'Year 2',
      event: 'Children enrolled in school. Special education needs identified but school cannot access health records.',
      systems: ['slds', 'iep'],
      domain: 'education',
      cost_impact: 14800,
    });
  }

  events.push({
    date: 'Year 2-3',
    event: `${name} cycles through systems. Each agency re-assesses independently. The same story is told dozens of times to different workers.`,
    systems: profile.systems_involved || [],
    domain: 'health',
    cost_impact: profile.total_annual_cost,
    is_gap: true,
    gap_description: 'No unified view across systems',
    coordination_would_help: 'A single coordinated profile would eliminate redundant assessments and enable whole-person care',
  });

  events.push({
    date: 'Year 3+',
    event: `With coordination: ${name}'s cost drops from $${Math.round(profile.total_annual_cost / 1000)}K to $${Math.round(profile.coordinated_annual_cost / 1000)}K. Savings of $${Math.round(profile.savings_annual / 1000)}K per year.`,
    systems: profile.systems_involved || [],
    domain: 'income',
    cost_impact: -profile.savings_annual,
  });

  return events;
}

export function TimelinePage() {
  const { id } = useParams<{ id: string }>();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    getProfile(id).then(p => { setProfile(p); setLoading(false); }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="p-8 font-mono text-sm">Loading timeline...</div>;
  if (!profile) return <div className="p-8 font-mono text-sm">Profile not found. <Link to="/profiles" className="underline">Browse profiles</Link></div>;

  const events = generateTimeline(profile);

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-baseline justify-between mb-8">
        <div>
          <h1 className="font-serif text-3xl font-bold tracking-tight">{profile.name}</h1>
          <p className="text-gray-500 font-mono text-sm mt-1">System journey timeline</p>
        </div>
        <div className="flex gap-3">
          <Link to={`/dome/${id}`} className="border border-black px-4 py-2 font-mono text-xs uppercase tracking-wider hover:bg-black hover:text-white transition-colors">View Dome</Link>
          <Link to={`/cost/${id}`} className="border border-black px-4 py-2 font-mono text-xs uppercase tracking-wider hover:bg-black hover:text-white transition-colors">Cost Dashboard</Link>
        </div>
      </div>

      <div className="relative">
        <div className="absolute left-6 top-0 bottom-0 w-px bg-black" />

        {events.map((event, i) => (
          <div key={i} className="relative pl-16 pb-10">
            <div
              className="absolute left-4 top-1 w-5 h-5 border-2 border-black"
              style={{
                backgroundColor: event.is_gap ? '#DC2626' : (DOMAIN_COLORS[event.domain] || '#000'),
              }}
            />

            <div className={`border ${event.is_gap ? 'border-red-600' : 'border-black'} p-4`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs uppercase tracking-wider font-bold">{event.date}</span>
                  <DomainBadge domain={event.domain} />
                </div>
                {event.cost_impact && (
                  <span className={`font-mono text-sm font-bold ${event.cost_impact < 0 ? 'text-green-700' : ''}`}>
                    {event.cost_impact < 0 ? '-' : '+'}${Math.abs(Math.round(event.cost_impact / 1000))}K/yr
                  </span>
                )}
              </div>

              <p className="text-sm leading-relaxed">{event.event}</p>

              {event.systems.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {event.systems.slice(0, 6).map(s => (
                    <span key={s} className="bg-gray-100 border border-gray-300 px-1.5 py-0.5 font-mono text-[10px] uppercase">{s}</span>
                  ))}
                </div>
              )}

              {event.is_gap && event.gap_description && (
                <div className="mt-3 border-t border-red-200 pt-2">
                  <div className="text-xs font-mono uppercase tracking-wider text-red-600 mb-1">Gap</div>
                  <p className="text-xs text-red-800">{event.gap_description}</p>
                </div>
              )}

              {event.coordination_would_help && (
                <div className="mt-2 bg-green-50 border border-green-200 p-2">
                  <div className="text-xs font-mono uppercase tracking-wider text-green-700 mb-1">With Coordination</div>
                  <p className="text-xs text-green-800">{event.coordination_would_help}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
