import { useState, useEffect } from 'react';
import {
  type LabSession,
  getSessions,
  getStatusColor,
  getTeammateColor,
  DEMO_SESSIONS,
  DEMO_TEAMMATES,
} from '../api/client';

export default function SessionManager() {
  const [sessions, setSessions] = useState<LabSession[]>(DEMO_SESSIONS);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    getSessions().then(setSessions);
  }, []);

  const filtered = statusFilter === 'all'
    ? sessions
    : sessions.filter((s) => s.status === statusFilter);

  const statusTabs = ['all', 'scheduled', 'active', 'completed', 'cancelled'] as const;

  const getParticipantName = (slug: string) => {
    const tm = DEMO_TEAMMATES.find(t => t.slug === slug);
    return tm?.name || slug;
  };

  const formatDateTime = (dt: string) => {
    return new Date(dt).toLocaleString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric',
      hour: '2-digit', minute: '2-digit', hour12: false,
    });
  };

  const getDuration = (start: string, end: string | null) => {
    if (!end) return 'ONGOING';
    const ms = new Date(end).getTime() - new Date(start).getTime();
    const hours = Math.floor(ms / (1000 * 60 * 60));
    const mins = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${mins}m`;
  };

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div>
        <h2 className="font-serif text-2xl tracking-wide">Lab Sessions</h2>
        <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
          {sessions.length} SESSIONS LOGGED // {sessions.filter(s => s.status === 'active').length} ACTIVE NOW
        </p>
      </div>

      {/* ── Status Filter ── */}
      <div className="flex items-center gap-1">
        <span className="font-mono text-[10px] text-text-muted tracking-wider mr-3">STATUS:</span>
        {statusTabs.map((s) => (
          <button
            key={s}
            onClick={() => setStatusFilter(s)}
            className={`font-mono text-[10px] tracking-wider px-3 py-1.5 border transition-colors ${
              statusFilter === s
                ? 'border-accent-glow bg-accent/30 text-text'
                : 'border-border text-text-muted hover:text-text hover:border-text-muted'
            }`}
          >
            {s === 'all' ? 'ALL' : s.toUpperCase()}
          </button>
        ))}
      </div>

      {/* ── Session Timeline ── */}
      {filtered.length === 0 ? (
        <div className="bg-surface border border-border p-8 text-center">
          <div className="font-mono text-sm text-text-muted">
            NO SESSIONS MATCH CURRENT FILTER
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((session) => {
            const isExpanded = expandedId === session.id;

            return (
              <div key={session.id} className="bg-surface border border-border">
                {/* Session Header */}
                <button
                  onClick={() => setExpandedId(isExpanded ? null : session.id)}
                  className="w-full text-left p-4 hover:bg-surface-alt transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        {/* Session Status Indicator */}
                        <div
                          className={`h-2.5 w-2.5 shrink-0 ${
                            session.status === 'active' ? 'animate-pulse' : ''
                          }`}
                          style={{ backgroundColor: getStatusColor(session.status) }}
                        />
                        <h3 className="text-base font-medium">{session.title}</h3>
                        <div
                          className="badge shrink-0"
                          style={{
                            color: getStatusColor(session.status),
                            borderColor: getStatusColor(session.status),
                          }}
                        >
                          {session.status.toUpperCase()}
                        </div>
                      </div>

                      {/* Focus Domain */}
                      <div className="font-mono text-[10px] text-text-muted tracking-wider mt-1">
                        FOCUS: {session.focus_domain}
                      </div>
                    </div>

                    {/* Time + Expand */}
                    <div className="flex items-center gap-4 shrink-0 ml-4">
                      <div className="text-right">
                        <div className="font-mono text-[10px] text-text-muted">
                          {formatDateTime(session.started_at)}
                        </div>
                        <div className="font-mono text-[10px] mt-0.5" style={{ color: getStatusColor(session.status) }}>
                          {getDuration(session.started_at, session.ended_at)}
                        </div>
                      </div>
                      <span className="font-mono text-xs text-text-muted">
                        {isExpanded ? '[-]' : '[+]'}
                      </span>
                    </div>
                  </div>

                  {/* Participants */}
                  <div className="flex items-center gap-2 mt-3">
                    <span className="font-mono text-[10px] text-text-muted tracking-wider">
                      PARTICIPANTS:
                    </span>
                    <div className="flex items-center gap-2">
                      {session.participants.map((slug) => (
                        <div key={slug} className="flex items-center gap-1">
                          <div
                            className="h-2.5 w-2.5 shrink-0"
                            style={{ backgroundColor: getTeammateColor(slug) }}
                          />
                          <span className="font-mono text-[10px] text-text-muted">
                            {getParticipantName(slug).split(' ').pop()}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </button>

                {/* Expanded: Findings */}
                {isExpanded && (
                  <div className="border-t border-border p-4 bg-surface-alt">
                    {/* Session Details Grid */}
                    <div className="grid grid-cols-3 gap-4 mb-4">
                      <div className="bg-bg border border-border p-3">
                        <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1">
                          STARTED
                        </div>
                        <div className="font-mono text-sm">
                          {formatDateTime(session.started_at)}
                        </div>
                      </div>
                      <div className="bg-bg border border-border p-3">
                        <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1">
                          ENDED
                        </div>
                        <div className="font-mono text-sm">
                          {session.ended_at ? formatDateTime(session.ended_at) : '-- IN PROGRESS --'}
                        </div>
                      </div>
                      <div className="bg-bg border border-border p-3">
                        <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1">
                          DURATION
                        </div>
                        <div className="font-mono text-sm" style={{ color: getStatusColor(session.status) }}>
                          {getDuration(session.started_at, session.ended_at)}
                        </div>
                      </div>
                    </div>

                    {/* Participants Detail */}
                    <div className="mb-4">
                      <div className="font-mono text-[10px] text-text-muted tracking-wider mb-2">
                        PARTICIPANT ROSTER
                      </div>
                      <div className="flex items-center gap-3">
                        {session.participants.map((slug) => (
                          <div
                            key={slug}
                            className="flex items-center gap-2 bg-bg border border-border px-3 py-2"
                          >
                            <div
                              className="h-4 w-4 shrink-0 flex items-center justify-center font-mono text-[8px] font-bold"
                              style={{
                                backgroundColor: getTeammateColor(slug) + '22',
                                color: getTeammateColor(slug),
                                border: `1px solid ${getTeammateColor(slug)}`,
                              }}
                            >
                              {getParticipantName(slug).split(' ').pop()?.charAt(0)}
                            </div>
                            <span className="font-mono text-xs">{getParticipantName(slug)}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Findings */}
                    <div>
                      <div className="font-mono text-[10px] text-text-muted tracking-wider mb-2">
                        FINDINGS
                      </div>
                      {session.findings ? (
                        <div className="bg-bg border border-border p-4">
                          <p className="text-sm leading-relaxed text-text-muted">
                            {session.findings}
                          </p>
                        </div>
                      ) : (
                        <div className="bg-bg border border-border p-4 text-center">
                          <span className="font-mono text-xs text-text-muted italic">
                            {session.status === 'scheduled'
                              ? 'Session has not started yet. Findings will be recorded during the session.'
                              : 'No findings recorded.'}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
