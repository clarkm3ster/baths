/**
 * TimelinePanel — studio integration wrapper for the timeline engine.
 *
 * Provides controls for generating a timeline from the current design,
 * summary statistics, and calendar / CSV export capabilities.
 */

import React, { useCallback, useMemo, useState } from "react";
import TimelineView, {
  type Timeline,
  type TimelineTask,
  type Phase,
} from "./TimelineView";

// ---------------------------------------------------------------------------
// Types matching the backend request / response schemas
// ---------------------------------------------------------------------------

type ActivationType = "single_day" | "weekend" | "week" | "month" | "ongoing";

interface DesignElement {
  id: string;
  name: string;
  element_type: string;
  is_permanent: boolean;
  permit_requirements: string[];
  requires_construction: boolean;
  requires_vendors: boolean;
  lead_time_days: number;
  setup_hours: number;
  teardown_hours: number;
  notes: string;
}

interface DesignInput {
  id: string;
  name: string;
  elements: DesignElement[];
  activation_type: ActivationType;
  location: string;
  notes: string;
}

interface ConflictEvent {
  name: string;
  date: string;
  end_date: string | null;
  location: string;
  conflict_level: "low" | "medium" | "high" | "critical";
  description: string;
  impact_notes: string;
}

interface ConflictReport {
  checked_range_start: string;
  checked_range_end: string;
  conflicts: ConflictEvent[];
  total_conflicts: number;
  has_critical: boolean;
  recommendation: string;
}

// ---------------------------------------------------------------------------
// Duration option mapping
// ---------------------------------------------------------------------------

const DURATION_OPTIONS: { label: string; value: ActivationType; days: number }[] = [
  { label: "1 Day", value: "single_day", days: 1 },
  { label: "Weekend", value: "weekend", days: 2 },
  { label: "Week", value: "week", days: 7 },
  { label: "Month", value: "month", days: 30 },
  { label: "Ongoing", value: "ongoing", days: 90 },
];

const PHASE_LABELS: Record<Phase, string> = {
  permits: "Permits",
  procurement: "Procurement",
  site_prep: "Site Prep",
  setup: "Setup",
  activation: "Activation",
  teardown: "Teardown",
  permanence_handoff: "Permanence Handoff",
};

// ---------------------------------------------------------------------------
// Date helpers
// ---------------------------------------------------------------------------

function parseDate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function formatDateDisplay(iso: string): string {
  const d = parseDate(iso);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function toISODate(d: Date): string {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// ---------------------------------------------------------------------------
// ICS export
// ---------------------------------------------------------------------------

function generateICS(timeline: Timeline): string {
  const lines: string[] = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//SPHERES Studio//Timeline//EN",
    "CALSCALE:GREGORIAN",
    `X-WR-CALNAME:${timeline.name}`,
  ];

  for (const task of timeline.tasks) {
    const uid = `${task.id}@spheres.studio`;
    const dtStart = task.start_date.replace(/-/g, "");
    // DTEND for all-day events is the day AFTER the last day
    const endDate = parseDate(task.end_date);
    endDate.setDate(endDate.getDate() + 1);
    const dtEnd = toISODate(endDate).replace(/-/g, "");

    lines.push(
      "BEGIN:VEVENT",
      `UID:${uid}`,
      `DTSTART;VALUE=DATE:${dtStart}`,
      `DTEND;VALUE=DATE:${dtEnd}`,
      `SUMMARY:[${PHASE_LABELS[task.phase]}] ${task.name}`,
      `DESCRIPTION:Team: ${task.assigned_team}\\nStatus: ${task.status}${task.notes ? "\\n" + task.notes : ""}`,
      `CATEGORIES:${PHASE_LABELS[task.phase]}`,
      "END:VEVENT"
    );
  }

  lines.push("END:VCALENDAR");
  return lines.join("\r\n");
}

function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ---------------------------------------------------------------------------
// CSV export
// ---------------------------------------------------------------------------

function generateCSV(timeline: Timeline): string {
  const headers = [
    "ID",
    "Name",
    "Phase",
    "Start Date",
    "End Date",
    "Duration (days)",
    "Dependencies",
    "Assigned Team",
    "Status",
    "Milestone",
    "Notes",
  ];
  const rows = timeline.tasks.map((t) => [
    t.id,
    `"${t.name.replace(/"/g, '""')}"`,
    t.phase,
    t.start_date,
    t.end_date,
    String(t.duration_days),
    `"${t.dependencies.join("; ")}"`,
    t.assigned_team,
    t.status,
    t.milestone ? "Yes" : "No",
    `"${(t.notes || "").replace(/"/g, '""')}"`,
  ]);

  return [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
}

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

export interface TimelinePanelProps {
  /** Current design from the studio (pass `null` when no design is loaded) */
  design?: DesignInput | null;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function TimelinePanel({ design }: TimelinePanelProps) {
  const [targetDate, setTargetDate] = useState<string>(() => {
    // Default to 90 days from now
    const d = new Date();
    d.setDate(d.getDate() + 90);
    return toISODate(d);
  });
  const [activationType, setActivationType] =
    useState<ActivationType>("single_day");
  const [timeline, setTimeline] = useState<Timeline | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conflicts, setConflicts] = useState<ConflictReport | null>(null);
  const [conflictsLoading, setConflictsLoading] = useState(false);

  const durationDays = useMemo(
    () =>
      DURATION_OPTIONS.find((o) => o.value === activationType)?.days ?? 1,
    [activationType]
  );

  // ---- Generate timeline ----
  const handleGenerate = useCallback(async () => {
    if (!design) {
      setError("No design loaded. Create a design first.");
      return;
    }

    setLoading(true);
    setError(null);
    setConflicts(null);

    try {
      const body = {
        design: {
          id: design.id,
          name: design.name,
          elements: design.elements,
          activation_type: activationType,
          location: design.location || "Philadelphia, PA",
          notes: design.notes || "",
        },
        target_activation_date: targetDate,
        duration_days: durationDays,
      };

      const res = await fetch("/api/timeline/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(
          errBody.detail || `Server error ${res.status}`
        );
      }

      const data: Timeline = await res.json();
      setTimeline(data);

      // Also check for conflicts
      fetchConflicts(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [design, targetDate, activationType, durationDays]);

  // ---- Fetch conflicts ----
  const fetchConflicts = useCallback(async (tl: Timeline) => {
    setConflictsLoading(true);
    try {
      const earliest = tl.tasks.length
        ? tl.tasks.reduce(
            (min, t) => (t.start_date < min ? t.start_date : min),
            tl.tasks[0].start_date
          )
        : tl.target_activation_date;

      const latest = tl.tasks.length
        ? tl.tasks.reduce(
            (max, t) => (t.end_date > max ? t.end_date : max),
            tl.tasks[0].end_date
          )
        : tl.activation_end_date;

      const params = new URLSearchParams({
        start_date: earliest,
        end_date: latest,
      });

      const res = await fetch(`/api/timeline/conflicts?${params}`);
      if (res.ok) {
        setConflicts(await res.json());
      }
    } catch {
      // Silently fail — conflicts are advisory
    } finally {
      setConflictsLoading(false);
    }
  }, []);

  // ---- Task update handler ----
  const handleTaskUpdate = useCallback(
    async (task: TimelineTask) => {
      if (!timeline) return;
      // Optimistic local update
      setTimeline((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          tasks: prev.tasks.map((t) => (t.id === task.id ? task : t)),
        };
      });

      // Persist to backend
      try {
        await fetch(`/api/timeline/${timeline.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            tasks: timeline.tasks.map((t) =>
              t.id === task.id ? task : t
            ),
          }),
        });
      } catch {
        // Silently fail — user can retry
      }
    },
    [timeline]
  );

  // ---- Summary stats ----
  const stats = useMemo(() => {
    if (!timeline) return null;
    const tasks = timeline.tasks;
    const permits = tasks.filter((t) => t.phase === "permits");
    const milestones = tasks.filter((t) => t.milestone);
    const earliest = tasks.length
      ? tasks.reduce(
          (min, t) => (t.start_date < min ? t.start_date : min),
          tasks[0].start_date
        )
      : timeline.target_activation_date;

    // Critical path length: sum duration of tasks on the critical path
    // (Simplified: use the total_duration_days from the timeline)
    return {
      totalDuration: timeline.total_duration_days,
      totalTasks: tasks.length,
      permitsNeeded: permits.length,
      milestoneCount: milestones.length,
      estimatedStart: earliest,
      weatherBuffer: timeline.weather_buffer_days,
    };
  }, [timeline]);

  // ---- Export handlers ----
  const handleExportICS = () => {
    if (!timeline) return;
    const ics = generateICS(timeline);
    const safeName = timeline.name.replace(/[^a-zA-Z0-9_-]/g, "_");
    downloadFile(ics, `${safeName}.ics`, "text/calendar");
  };

  const handleExportCSV = () => {
    if (!timeline) return;
    const csv = generateCSV(timeline);
    const safeName = timeline.name.replace(/[^a-zA-Z0-9_-]/g, "_");
    downloadFile(csv, `${safeName}.csv`, "text/csv");
  };

  // ---- Render ----
  return (
    <div className="flex flex-col h-full">
      {/* Controls bar */}
      <div className="flex flex-wrap items-end gap-4 p-4 border-b border-gray-200 bg-white">
        {/* Target date */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
            Activation Date
          </label>
          <input
            type="date"
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none"
            value={targetDate}
            onChange={(e) => setTargetDate(e.target.value)}
          />
        </div>

        {/* Duration */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
            Duration
          </label>
          <select
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none"
            value={activationType}
            onChange={(e) =>
              setActivationType(e.target.value as ActivationType)
            }
          >
            {DURATION_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={loading || !design}
          className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all ${
            loading || !design
              ? "bg-gray-200 text-gray-400 cursor-not-allowed"
              : "bg-gray-900 text-white hover:bg-gray-800 active:bg-gray-950"
          }`}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg
                className="animate-spin h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Generating...
            </span>
          ) : (
            "Generate Timeline"
          )}
        </button>

        {/* Export buttons (show only when timeline exists) */}
        {timeline && (
          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={handleExportICS}
              className="px-3 py-2 text-xs font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Export .ics
            </button>
            <button
              onClick={handleExportCSV}
              className="px-3 py-2 text-xs font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Export CSV
            </button>
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="mx-4 mt-3 px-4 py-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Summary stats + conflicts */}
      {stats && (
        <div className="flex flex-wrap gap-4 p-4 border-b border-gray-100">
          {/* Stat cards */}
          <StatCard
            label="Total Duration"
            value={`${stats.totalDuration} days`}
          />
          <StatCard label="Tasks" value={String(stats.totalTasks)} />
          <StatCard
            label="Permits"
            value={`${stats.permitsNeeded} tasks`}
          />
          <StatCard
            label="Milestones"
            value={String(stats.milestoneCount)}
          />
          <StatCard
            label="Est. Start"
            value={formatDateDisplay(stats.estimatedStart)}
          />
          {stats.weatherBuffer > 0 && (
            <StatCard
              label="Weather Buffer"
              value={`+${stats.weatherBuffer} days`}
              warn
            />
          )}

          {/* Conflict summary */}
          {conflictsLoading && (
            <div className="flex items-center text-xs text-gray-400 ml-auto">
              Checking city calendar...
            </div>
          )}
          {conflicts && conflicts.total_conflicts > 0 && (
            <div
              className={`ml-auto px-4 py-2 rounded-lg text-xs ${
                conflicts.has_critical
                  ? "bg-red-50 border border-red-200 text-red-700"
                  : "bg-amber-50 border border-amber-200 text-amber-700"
              }`}
            >
              <p className="font-semibold mb-1">
                {conflicts.total_conflicts} City Event Conflict
                {conflicts.total_conflicts !== 1 && "s"}
              </p>
              <p>{conflicts.recommendation}</p>
              <div className="mt-2 space-y-1">
                {conflicts.conflicts.map((c, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <ConflictBadge level={c.conflict_level} />
                    <span>
                      {c.name} — {formatDateDisplay(c.date)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {conflicts && conflicts.total_conflicts === 0 && (
            <div className="ml-auto px-4 py-2 rounded-lg text-xs bg-green-50 border border-green-200 text-green-700">
              No city event conflicts detected.
            </div>
          )}
        </div>
      )}

      {/* Timeline Gantt chart */}
      {timeline ? (
        <div className="flex-1 min-h-0">
          <TimelineView
            timeline={timeline}
            onTaskUpdate={handleTaskUpdate}
          />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center max-w-md">
            <div className="text-6xl text-gray-200 mb-4">
              <svg
                width="64"
                height="64"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                className="mx-auto"
              >
                <rect x="3" y="4" width="18" height="18" rx="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
                <line x1="8" y1="14" x2="16" y2="14" />
                <line x1="8" y1="18" x2="12" y2="18" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              No timeline generated yet
            </h3>
            <p className="text-sm text-gray-400">
              {design
                ? "Choose a target activation date and click Generate Timeline to create a full project schedule."
                : "Load a design first, then generate a timeline to see a full Gantt chart with phases, tasks, and dependencies."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StatCard({
  label,
  value,
  warn = false,
}: {
  label: string;
  value: string;
  warn?: boolean;
}) {
  return (
    <div
      className={`px-3 py-2 rounded-lg border ${
        warn
          ? "bg-amber-50 border-amber-200"
          : "bg-gray-50 border-gray-200"
      }`}
    >
      <p
        className={`text-[10px] font-medium uppercase tracking-wide ${
          warn ? "text-amber-600" : "text-gray-400"
        }`}
      >
        {label}
      </p>
      <p
        className={`text-sm font-semibold ${
          warn ? "text-amber-700" : "text-gray-800"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function ConflictBadge({
  level,
}: {
  level: "low" | "medium" | "high" | "critical";
}) {
  const colors: Record<string, string> = {
    low: "bg-gray-200 text-gray-600",
    medium: "bg-amber-200 text-amber-700",
    high: "bg-orange-200 text-orange-700",
    critical: "bg-red-200 text-red-700",
  };
  return (
    <span
      className={`px-1.5 py-0.5 rounded text-[9px] font-bold uppercase ${colors[level]}`}
    >
      {level}
    </span>
  );
}
