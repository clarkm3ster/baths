/**
 * TimelineView — hand-built SVG Gantt chart for SPHERES Studio
 *
 * Features:
 *  - Horizontal bars grouped by phase, colour-coded
 *  - Dependency arrows between tasks
 *  - "Today" marker line
 *  - Zoom: week / month / quarter
 *  - Click a task to view / edit details
 *  - Milestone diamonds on key dates
 *  - Critical-path highlighting
 *  - Drag to adjust task duration
 *  - Phase headers with collapse / expand
 */

import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

// ---------------------------------------------------------------------------
// Types (mirrors backend Pydantic models)
// ---------------------------------------------------------------------------

export type Phase =
  | "permits"
  | "procurement"
  | "site_prep"
  | "setup"
  | "activation"
  | "teardown"
  | "permanence_handoff";

export type TaskStatus =
  | "not_started"
  | "in_progress"
  | "completed"
  | "blocked";

export type AssignedTeam =
  | "permits_team"
  | "procurement"
  | "construction"
  | "operations"
  | "community";

export interface TimelineTask {
  id: string;
  name: string;
  phase: Phase;
  start_date: string; // ISO date
  end_date: string;
  duration_days: number;
  dependencies: string[];
  assigned_team: AssignedTeam;
  status: TaskStatus;
  notes: string;
  milestone: boolean;
}

export interface Timeline {
  id: string;
  design_id: string;
  name: string;
  tasks: TimelineTask[];
  target_activation_date: string;
  activation_end_date: string;
  created_at: string;
  total_duration_days: number;
  weather_buffer_days: number;
  season_warnings: string[];
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const PHASE_ORDER: Phase[] = [
  "permits",
  "procurement",
  "site_prep",
  "setup",
  "activation",
  "teardown",
  "permanence_handoff",
];

const PHASE_COLORS: Record<Phase, string> = {
  permits: "#3B82F6",        // blue-500
  procurement: "#F97316",    // orange-500
  site_prep: "#10B981",      // emerald-500
  setup: "#22C55E",          // green-500
  activation: "#EAB308",     // yellow-500
  teardown: "#EF4444",       // red-500
  permanence_handoff: "#A855F7", // purple-500
};

const PHASE_LABELS: Record<Phase, string> = {
  permits: "Permits",
  procurement: "Procurement",
  site_prep: "Site Prep",
  setup: "Setup",
  activation: "Activation",
  teardown: "Teardown",
  permanence_handoff: "Permanence Handoff",
};

const STATUS_OPACITY: Record<TaskStatus, number> = {
  not_started: 0.55,
  in_progress: 1,
  completed: 0.35,
  blocked: 0.7,
};

type ZoomLevel = "week" | "month" | "quarter";

const ROW_HEIGHT = 36;
const PHASE_HEADER_HEIGHT = 32;
const LABEL_COL_WIDTH = 260;
const MILESTONE_SIZE = 10;
const MIN_BAR_WIDTH = 6;
const HEADER_HEIGHT = 48;
const SCROLL_PADDING = 24;

// ---------------------------------------------------------------------------
// Date helpers (no date-fns — plain Date)
// ---------------------------------------------------------------------------

function parseDate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function formatDate(d: Date): string {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function addDays(d: Date, n: number): Date {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

function diffDays(a: Date, b: Date): number {
  return Math.round((a.getTime() - b.getTime()) / 86_400_000);
}

function startOfWeek(d: Date): Date {
  const r = new Date(d);
  r.setDate(r.getDate() - r.getDay());
  return r;
}

function startOfMonth(d: Date): Date {
  return new Date(d.getFullYear(), d.getMonth(), 1);
}

function endOfMonth(d: Date): Date {
  return new Date(d.getFullYear(), d.getMonth() + 1, 0);
}

function shortMonth(d: Date): string {
  return d.toLocaleString("en-US", { month: "short" });
}

function isSameDay(a: Date, b: Date): boolean {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

// ---------------------------------------------------------------------------
// Compute critical path (longest dependency chain)
// ---------------------------------------------------------------------------

function computeCriticalPath(tasks: TimelineTask[]): Set<string> {
  const taskMap = new Map<string, TimelineTask>();
  for (const t of tasks) taskMap.set(t.id, t);

  const memo = new Map<string, number>();

  function longestPath(id: string): number {
    if (memo.has(id)) return memo.get(id)!;
    const t = taskMap.get(id);
    if (!t) return 0;
    let maxDep = 0;
    for (const depId of t.dependencies) {
      maxDep = Math.max(maxDep, longestPath(depId));
    }
    const val = t.duration_days + maxDep;
    memo.set(id, val);
    return val;
  }

  for (const t of tasks) longestPath(t.id);

  // Find the longest total and trace back
  let maxLen = 0;
  let maxId = "";
  for (const [id, len] of memo) {
    if (len > maxLen) {
      maxLen = len;
      maxId = id;
    }
  }

  const critical = new Set<string>();

  function trace(id: string) {
    critical.add(id);
    const t = taskMap.get(id);
    if (!t) return;
    // Pick the dependency with the longest path
    let bestDep = "";
    let bestLen = -1;
    for (const depId of t.dependencies) {
      const l = memo.get(depId) ?? 0;
      if (l > bestLen) {
        bestLen = l;
        bestDep = depId;
      }
    }
    if (bestDep) trace(bestDep);
  }

  if (maxId) trace(maxId);
  return critical;
}

// ---------------------------------------------------------------------------
// Component props
// ---------------------------------------------------------------------------

export interface TimelineViewProps {
  timeline: Timeline;
  onTaskUpdate?: (task: TimelineTask) => void;
}

// ---------------------------------------------------------------------------
// TaskDetailModal
// ---------------------------------------------------------------------------

interface TaskDetailModalProps {
  task: TimelineTask;
  onClose: () => void;
  onSave: (updated: TimelineTask) => void;
}

function TaskDetailModal({ task, onClose, onSave }: TaskDetailModalProps) {
  const [editTask, setEditTask] = useState<TimelineTask>({ ...task });

  const handleSave = () => {
    onSave(editTask);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-lg mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{task.name}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-xl leading-none"
          >
            &times;
          </button>
        </div>

        <div className="space-y-4 text-sm">
          {/* Phase badge */}
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">Phase</span>
            <span
              className="px-2 py-0.5 rounded text-white text-xs font-medium"
              style={{ backgroundColor: PHASE_COLORS[task.phase] }}
            >
              {PHASE_LABELS[task.phase]}
            </span>
          </div>

          {/* Dates */}
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">Start</span>
            <input
              type="date"
              className="border rounded px-2 py-1 text-gray-800"
              value={editTask.start_date}
              onChange={(e) =>
                setEditTask({ ...editTask, start_date: e.target.value })
              }
            />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">End</span>
            <input
              type="date"
              className="border rounded px-2 py-1 text-gray-800"
              value={editTask.end_date}
              onChange={(e) =>
                setEditTask({ ...editTask, end_date: e.target.value })
              }
            />
          </div>

          {/* Duration */}
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">Duration</span>
            <span className="text-gray-800">
              {editTask.duration_days} day{editTask.duration_days !== 1 && "s"}
            </span>
          </div>

          {/* Assigned team */}
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">Team</span>
            <select
              className="border rounded px-2 py-1 text-gray-800"
              value={editTask.assigned_team}
              onChange={(e) =>
                setEditTask({
                  ...editTask,
                  assigned_team: e.target.value as AssignedTeam,
                })
              }
            >
              <option value="permits_team">Permits Team</option>
              <option value="procurement">Procurement</option>
              <option value="construction">Construction</option>
              <option value="operations">Operations</option>
              <option value="community">Community</option>
            </select>
          </div>

          {/* Status */}
          <div className="flex items-center gap-2">
            <span className="text-gray-500 w-24">Status</span>
            <select
              className="border rounded px-2 py-1 text-gray-800"
              value={editTask.status}
              onChange={(e) =>
                setEditTask({
                  ...editTask,
                  status: e.target.value as TaskStatus,
                })
              }
            >
              <option value="not_started">Not Started</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="blocked">Blocked</option>
            </select>
          </div>

          {/* Notes */}
          <div>
            <span className="text-gray-500 block mb-1">Notes</span>
            <textarea
              className="border rounded px-2 py-1 w-full text-gray-800 resize-none"
              rows={3}
              value={editTask.notes}
              onChange={(e) =>
                setEditTask({ ...editTask, notes: e.target.value })
              }
            />
          </div>

          {/* Dependencies */}
          {task.dependencies.length > 0 && (
            <div>
              <span className="text-gray-500 block mb-1">Depends on</span>
              <div className="text-xs text-gray-600 font-mono">
                {task.dependencies.join(", ")}
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end gap-2 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 text-sm bg-gray-900 text-white rounded-lg hover:bg-gray-800"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function TimelineView({
  timeline,
  onTaskUpdate,
}: TimelineViewProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const [zoom, setZoom] = useState<ZoomLevel>("month");
  const [collapsedPhases, setCollapsedPhases] = useState<Set<Phase>>(new Set());
  const [selectedTask, setSelectedTask] = useState<TimelineTask | null>(null);
  const [dragState, setDragState] = useState<{
    taskId: string;
    edge: "start" | "end";
    originX: number;
    originalDate: string;
  } | null>(null);
  const [showCriticalPath, setShowCriticalPath] = useState(true);

  // Mutable ref for tasks so drag can modify without re-render storms
  const [localTasks, setLocalTasks] = useState<TimelineTask[]>(
    timeline.tasks
  );

  useEffect(() => {
    setLocalTasks(timeline.tasks);
  }, [timeline.tasks]);

  // ----- derived data -----

  const criticalSet = useMemo(
    () => computeCriticalPath(localTasks),
    [localTasks]
  );

  const taskMap = useMemo(() => {
    const m = new Map<string, TimelineTask>();
    for (const t of localTasks) m.set(t.id, t);
    return m;
  }, [localTasks]);

  // Compute the global date range
  const { rangeStart, rangeEnd, totalDays } = useMemo(() => {
    if (localTasks.length === 0) {
      const today = new Date();
      return {
        rangeStart: today,
        rangeEnd: addDays(today, 30),
        totalDays: 30,
      };
    }
    let minD = parseDate(localTasks[0].start_date);
    let maxD = parseDate(localTasks[0].end_date);
    for (const t of localTasks) {
      const s = parseDate(t.start_date);
      const e = parseDate(t.end_date);
      if (s < minD) minD = s;
      if (e > maxD) maxD = e;
    }
    // Pad edges
    const rs = addDays(startOfWeek(minD), -7);
    const re = addDays(maxD, 14);
    return {
      rangeStart: rs,
      rangeEnd: re,
      totalDays: diffDays(re, rs) + 1,
    };
  }, [localTasks]);

  // Pixels per day based on zoom
  const dayWidth = useMemo(() => {
    switch (zoom) {
      case "week":
        return 28;
      case "month":
        return 10;
      case "quarter":
        return 3.5;
    }
  }, [zoom]);

  const chartWidth = totalDays * dayWidth;

  // Build visible row list (respecting collapsed phases)
  const { rows, phaseHeaderIndices, totalHeight } = useMemo(() => {
    type RowItem =
      | { kind: "phase"; phase: Phase }
      | { kind: "task"; task: TimelineTask };

    const items: RowItem[] = [];
    for (const phase of PHASE_ORDER) {
      const phaseTasks = localTasks.filter((t) => t.phase === phase);
      if (phaseTasks.length === 0) continue;
      items.push({ kind: "phase", phase });
      if (!collapsedPhases.has(phase)) {
        for (const t of phaseTasks) {
          items.push({ kind: "task", task: t });
        }
      }
    }

    const phi: number[] = [];
    let height = HEADER_HEIGHT;
    for (let i = 0; i < items.length; i++) {
      if (items[i].kind === "phase") {
        phi.push(i);
        height += PHASE_HEADER_HEIGHT;
      } else {
        height += ROW_HEIGHT;
      }
    }
    return { rows: items, phaseHeaderIndices: phi, totalHeight: height };
  }, [localTasks, collapsedPhases]);

  // Map task-id -> row centre Y for dependency arrows
  const taskYMap = useMemo(() => {
    const m = new Map<string, number>();
    let y = HEADER_HEIGHT;
    for (const row of rows) {
      if (row.kind === "phase") {
        y += PHASE_HEADER_HEIGHT;
      } else {
        m.set(row.task.id, y + ROW_HEIGHT / 2);
        y += ROW_HEIGHT;
      }
    }
    return m;
  }, [rows]);

  // ----- helpers -----

  const dateToX = useCallback(
    (d: Date) => diffDays(d, rangeStart) * dayWidth,
    [rangeStart, dayWidth]
  );

  const xToDate = useCallback(
    (x: number) => addDays(rangeStart, Math.round(x / dayWidth)),
    [rangeStart, dayWidth]
  );

  const togglePhase = (phase: Phase) => {
    setCollapsedPhases((prev) => {
      const next = new Set(prev);
      if (next.has(phase)) next.delete(phase);
      else next.add(phase);
      return next;
    });
  };

  // ----- drag handlers -----

  const handleDragStart = (
    e: React.MouseEvent,
    taskId: string,
    edge: "start" | "end"
  ) => {
    e.stopPropagation();
    const task = taskMap.get(taskId);
    if (!task) return;
    setDragState({
      taskId,
      edge,
      originX: e.clientX,
      originalDate: edge === "start" ? task.start_date : task.end_date,
    });
  };

  useEffect(() => {
    if (!dragState) return;

    const handleMouseMove = (e: MouseEvent) => {
      const dx = e.clientX - dragState.originX;
      const daysDelta = Math.round(dx / dayWidth);
      if (daysDelta === 0) return;

      setLocalTasks((prev) =>
        prev.map((t) => {
          if (t.id !== dragState.taskId) return t;
          const origDate = parseDate(dragState.originalDate);
          const newDate = addDays(origDate, daysDelta);

          if (dragState.edge === "end") {
            const startD = parseDate(t.start_date);
            if (newDate < startD) return t;
            const dur = diffDays(newDate, startD) + 1;
            return {
              ...t,
              end_date: formatDate(newDate),
              duration_days: dur,
            };
          } else {
            const endD = parseDate(t.end_date);
            if (newDate > endD) return t;
            const dur = diffDays(endD, newDate) + 1;
            return {
              ...t,
              start_date: formatDate(newDate),
              duration_days: dur,
            };
          }
        })
      );
    };

    const handleMouseUp = () => {
      if (dragState) {
        const updated = localTasks.find((t) => t.id === dragState.taskId);
        if (updated && onTaskUpdate) {
          onTaskUpdate(updated);
        }
      }
      setDragState(null);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragState, dayWidth, localTasks, onTaskUpdate]);

  // ----- render helpers -----

  const renderHeader = () => {
    const ticks: React.ReactNode[] = [];
    const d = new Date(rangeStart);
    let lastLabel = "";

    while (d <= rangeEnd) {
      const x = dateToX(d);

      if (zoom === "week") {
        // Show each day
        const label = `${d.getDate()}`;
        const monthLabel = `${shortMonth(d)} ${d.getFullYear()}`;
        if (d.getDate() === 1 || lastLabel !== monthLabel) {
          ticks.push(
            <text
              key={`mh-${formatDate(d)}`}
              x={x + 2}
              y={14}
              className="text-[10px] font-semibold fill-gray-600"
            >
              {monthLabel}
            </text>
          );
          lastLabel = monthLabel;
        }
        ticks.push(
          <g key={`dh-${formatDate(d)}`}>
            <line
              x1={x}
              y1={HEADER_HEIGHT - 18}
              x2={x}
              y2={HEADER_HEIGHT}
              stroke="#E5E7EB"
              strokeWidth={d.getDay() === 0 ? 1 : 0.5}
            />
            <text
              x={x + dayWidth / 2}
              y={HEADER_HEIGHT - 5}
              textAnchor="middle"
              className="text-[9px] fill-gray-400"
            >
              {label}
            </text>
          </g>
        );
      } else if (zoom === "month") {
        if (d.getDate() === 1) {
          const label = `${shortMonth(d)} ${d.getFullYear()}`;
          ticks.push(
            <g key={`mh-${formatDate(d)}`}>
              <line
                x1={x}
                y1={0}
                x2={x}
                y2={HEADER_HEIGHT}
                stroke="#D1D5DB"
                strokeWidth={1}
              />
              <text
                x={x + 4}
                y={HEADER_HEIGHT - 8}
                className="text-[11px] font-medium fill-gray-600"
              >
                {label}
              </text>
            </g>
          );
        } else if (d.getDate() % 7 === 1) {
          ticks.push(
            <line
              key={`wl-${formatDate(d)}`}
              x1={x}
              y1={HEADER_HEIGHT - 8}
              x2={x}
              y2={HEADER_HEIGHT}
              stroke="#E5E7EB"
              strokeWidth={0.5}
            />
          );
        }
      } else {
        // quarter
        if (d.getDate() === 1) {
          const label = `${shortMonth(d)} ${d.getFullYear()}`;
          ticks.push(
            <g key={`mh-${formatDate(d)}`}>
              <line
                x1={x}
                y1={0}
                x2={x}
                y2={HEADER_HEIGHT}
                stroke="#D1D5DB"
                strokeWidth={d.getMonth() % 3 === 0 ? 1.5 : 0.5}
              />
              {d.getMonth() % 3 === 0 && (
                <text
                  x={x + 4}
                  y={14}
                  className="text-[11px] font-semibold fill-gray-600"
                >
                  Q{Math.floor(d.getMonth() / 3) + 1} {d.getFullYear()}
                </text>
              )}
              <text
                x={x + 4}
                y={HEADER_HEIGHT - 6}
                className="text-[9px] fill-gray-400"
              >
                {label}
              </text>
            </g>
          );
        }
      }
      d.setDate(d.getDate() + 1);
    }
    return ticks;
  };

  const renderGridLines = () => {
    const lines: React.ReactNode[] = [];
    const d = new Date(rangeStart);
    while (d <= rangeEnd) {
      if (d.getDate() === 1) {
        const x = dateToX(d);
        lines.push(
          <line
            key={`grid-${formatDate(d)}`}
            x1={x}
            y1={HEADER_HEIGHT}
            x2={x}
            y2={totalHeight}
            stroke="#F3F4F6"
            strokeWidth={1}
          />
        );
      }
      d.setDate(d.getDate() + 1);
    }
    return lines;
  };

  const renderTodayLine = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (today < rangeStart || today > rangeEnd) return null;
    const x = dateToX(today);
    return (
      <g>
        <line
          x1={x}
          y1={0}
          x2={x}
          y2={totalHeight}
          stroke="#EF4444"
          strokeWidth={2}
          strokeDasharray="6 3"
        />
        <text
          x={x + 4}
          y={12}
          className="text-[9px] font-bold fill-red-500"
        >
          TODAY
        </text>
      </g>
    );
  };

  const renderDependencyArrows = () => {
    const arrows: React.ReactNode[] = [];

    for (const task of localTasks) {
      const toY = taskYMap.get(task.id);
      if (toY === undefined) continue;
      const toX = dateToX(parseDate(task.start_date));

      for (const depId of task.dependencies) {
        const dep = taskMap.get(depId);
        if (!dep) continue;
        const fromY = taskYMap.get(depId);
        if (fromY === undefined) continue;
        const fromX =
          dateToX(parseDate(dep.end_date)) + dayWidth;

        const isCrit =
          showCriticalPath &&
          criticalSet.has(task.id) &&
          criticalSet.has(depId);

        // Simple right-angle connector: from end of dep to start of task
        const midX = (fromX + toX) / 2;

        const pathD =
          fromY === toY
            ? `M ${fromX} ${fromY} L ${toX - 4} ${toY}`
            : `M ${fromX} ${fromY} L ${midX} ${fromY} L ${midX} ${toY} L ${toX - 4} ${toY}`;

        arrows.push(
          <g key={`dep-${depId}-${task.id}`}>
            <path
              d={pathD}
              fill="none"
              stroke={isCrit ? "#EF4444" : "#CBD5E1"}
              strokeWidth={isCrit ? 2 : 1}
              strokeDasharray={isCrit ? undefined : "4 2"}
            />
            {/* arrowhead */}
            <polygon
              points={`${toX - 4},${toY - 3} ${toX},${toY} ${toX - 4},${toY + 3}`}
              fill={isCrit ? "#EF4444" : "#CBD5E1"}
            />
          </g>
        );
      }
    }
    return arrows;
  };

  const renderRows = () => {
    const elements: React.ReactNode[] = [];
    let y = HEADER_HEIGHT;

    for (const row of rows) {
      if (row.kind === "phase") {
        const phase = row.phase;
        const isCollapsed = collapsedPhases.has(phase);
        const phaseTaskCount = localTasks.filter(
          (t) => t.phase === phase
        ).length;

        elements.push(
          <g
            key={`ph-${phase}`}
            className="cursor-pointer"
            onClick={() => togglePhase(phase)}
          >
            {/* Phase header background spanning chart */}
            <rect
              x={0}
              y={y}
              width={chartWidth + LABEL_COL_WIDTH}
              height={PHASE_HEADER_HEIGHT}
              fill={PHASE_COLORS[phase]}
              opacity={0.1}
            />
            {/* Collapse indicator */}
            <text
              x={8}
              y={y + PHASE_HEADER_HEIGHT / 2 + 4}
              className="text-[11px] fill-gray-500 select-none"
            >
              {isCollapsed ? "\u25B6" : "\u25BC"}
            </text>
            {/* Phase label */}
            <text
              x={24}
              y={y + PHASE_HEADER_HEIGHT / 2 + 4}
              className="text-[12px] font-semibold select-none"
              fill={PHASE_COLORS[phase]}
            >
              {PHASE_LABELS[phase]}
            </text>
            {/* Task count */}
            <text
              x={LABEL_COL_WIDTH - 12}
              y={y + PHASE_HEADER_HEIGHT / 2 + 4}
              textAnchor="end"
              className="text-[10px] fill-gray-400 select-none"
            >
              {phaseTaskCount} task{phaseTaskCount !== 1 && "s"}
            </text>
          </g>
        );
        y += PHASE_HEADER_HEIGHT;
        continue;
      }

      const task = row.task;
      const startX = dateToX(parseDate(task.start_date));
      const endX = dateToX(parseDate(task.end_date)) + dayWidth;
      const barWidth = Math.max(endX - startX, MIN_BAR_WIDTH);
      const barX = startX + LABEL_COL_WIDTH;
      const barY = y + 6;
      const barH = ROW_HEIGHT - 12;
      const isCrit = showCriticalPath && criticalSet.has(task.id);
      const isBlocked = task.status === "blocked";

      // Alternating row bg
      elements.push(
        <rect
          key={`rowbg-${task.id}`}
          x={0}
          y={y}
          width={chartWidth + LABEL_COL_WIDTH}
          height={ROW_HEIGHT}
          fill={y % (ROW_HEIGHT * 2) < ROW_HEIGHT ? "#FAFAFA" : "white"}
        />
      );

      // Task label (left column)
      elements.push(
        <text
          key={`lbl-${task.id}`}
          x={28}
          y={y + ROW_HEIGHT / 2 + 4}
          className="text-[11px] fill-gray-700 select-none"
          style={{
            cursor: "pointer",
            fontWeight: task.milestone ? 600 : 400,
          }}
          onClick={() => setSelectedTask(task)}
        >
          {task.name.length > 32
            ? task.name.slice(0, 30) + "..."
            : task.name}
        </text>
      );

      if (task.milestone && task.duration_days <= 1) {
        // Render as diamond
        const cx = barX + barWidth / 2;
        const cy = y + ROW_HEIGHT / 2;
        elements.push(
          <g
            key={`ms-${task.id}`}
            className="cursor-pointer"
            onClick={() => setSelectedTask(task)}
          >
            <polygon
              points={`${cx},${cy - MILESTONE_SIZE} ${cx + MILESTONE_SIZE},${cy} ${cx},${cy + MILESTONE_SIZE} ${cx - MILESTONE_SIZE},${cy}`}
              fill={PHASE_COLORS[task.phase]}
              stroke={isCrit ? "#EF4444" : "white"}
              strokeWidth={isCrit ? 2 : 1}
              opacity={STATUS_OPACITY[task.status]}
            />
          </g>
        );
      } else {
        // Render as bar
        elements.push(
          <g
            key={`bar-${task.id}`}
            className="cursor-pointer"
            onClick={() => setSelectedTask(task)}
          >
            <rect
              x={barX}
              y={barY}
              width={barWidth}
              height={barH}
              rx={4}
              fill={PHASE_COLORS[task.phase]}
              opacity={STATUS_OPACITY[task.status]}
              stroke={isCrit ? "#EF4444" : "none"}
              strokeWidth={isCrit ? 2 : 0}
            />
            {/* Blocked hatching */}
            {isBlocked && (
              <rect
                x={barX}
                y={barY}
                width={barWidth}
                height={barH}
                rx={4}
                fill="url(#hatch)"
                opacity={0.3}
              />
            )}
            {/* Progress fill for in_progress */}
            {task.status === "in_progress" && (
              <rect
                x={barX}
                y={barY}
                width={barWidth * 0.5}
                height={barH}
                rx={4}
                fill={PHASE_COLORS[task.phase]}
                opacity={0.3}
              />
            )}
            {/* Completed checkmark fill */}
            {task.status === "completed" && (
              <rect
                x={barX}
                y={barY}
                width={barWidth}
                height={barH}
                rx={4}
                fill={PHASE_COLORS[task.phase]}
                opacity={0.15}
              />
            )}
            {/* Bar label */}
            {barWidth > 60 && (
              <text
                x={barX + 6}
                y={barY + barH / 2 + 3}
                className="text-[9px] fill-white font-medium select-none pointer-events-none"
              >
                {task.duration_days}d
              </text>
            )}
            {/* Drag handles */}
            <rect
              x={barX}
              y={barY}
              width={6}
              height={barH}
              fill="transparent"
              className="cursor-w-resize"
              onMouseDown={(e) => handleDragStart(e, task.id, "start")}
            />
            <rect
              x={barX + barWidth - 6}
              y={barY}
              width={6}
              height={barH}
              fill="transparent"
              className="cursor-e-resize"
              onMouseDown={(e) => handleDragStart(e, task.id, "end")}
            />
          </g>
        );
      }

      y += ROW_HEIGHT;
    }

    return elements;
  };

  // Activation highlight band
  const renderActivationBand = () => {
    const aStart = parseDate(timeline.target_activation_date);
    const aEnd = parseDate(timeline.activation_end_date);
    const x1 = dateToX(aStart) + LABEL_COL_WIDTH;
    const x2 = dateToX(aEnd) + dayWidth + LABEL_COL_WIDTH;
    return (
      <rect
        x={x1}
        y={HEADER_HEIGHT}
        width={x2 - x1}
        height={totalHeight - HEADER_HEIGHT}
        fill="#EAB308"
        opacity={0.06}
      />
    );
  };

  // ----- render -----

  return (
    <div className="flex flex-col h-full bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-100 bg-gray-50/60 flex-shrink-0">
        <div className="flex items-center gap-3">
          <h2 className="text-sm font-semibold text-gray-800">
            {timeline.name}
          </h2>
          <span className="text-xs text-gray-400">
            {timeline.total_duration_days} days total
          </span>
        </div>
        <div className="flex items-center gap-2">
          {/* Critical path toggle */}
          <label className="flex items-center gap-1.5 text-xs text-gray-500 cursor-pointer select-none">
            <input
              type="checkbox"
              className="accent-red-500"
              checked={showCriticalPath}
              onChange={(e) => setShowCriticalPath(e.target.checked)}
            />
            Critical path
          </label>
          {/* Zoom buttons */}
          <div className="flex bg-white border border-gray-200 rounded-lg overflow-hidden">
            {(["week", "month", "quarter"] as ZoomLevel[]).map((z) => (
              <button
                key={z}
                onClick={() => setZoom(z)}
                className={`px-3 py-1 text-xs font-medium capitalize transition-colors ${
                  zoom === z
                    ? "bg-gray-900 text-white"
                    : "text-gray-500 hover:text-gray-800 hover:bg-gray-50"
                }`}
              >
                {z}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Season warnings */}
      {timeline.season_warnings.length > 0 && (
        <div className="px-4 py-2 bg-amber-50 border-b border-amber-100 flex-shrink-0">
          {timeline.season_warnings.map((w, i) => (
            <p key={i} className="text-xs text-amber-700">
              {w}
            </p>
          ))}
        </div>
      )}

      {/* Scrollable chart area */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-auto"
        style={{ minHeight: 200 }}
      >
        <svg
          ref={svgRef}
          width={chartWidth + LABEL_COL_WIDTH + SCROLL_PADDING}
          height={totalHeight + SCROLL_PADDING}
          className="select-none"
        >
          {/* Defs */}
          <defs>
            <pattern
              id="hatch"
              width="6"
              height="6"
              patternUnits="userSpaceOnUse"
              patternTransform="rotate(45)"
            >
              <line
                x1="0"
                y1="0"
                x2="0"
                y2="6"
                stroke="#EF4444"
                strokeWidth="1.5"
              />
            </pattern>
          </defs>

          {/* Header background */}
          <rect
            x={0}
            y={0}
            width={chartWidth + LABEL_COL_WIDTH + SCROLL_PADDING}
            height={HEADER_HEIGHT}
            fill="#F9FAFB"
          />

          {/* Label column divider */}
          <line
            x1={LABEL_COL_WIDTH}
            y1={0}
            x2={LABEL_COL_WIDTH}
            y2={totalHeight}
            stroke="#E5E7EB"
            strokeWidth={1}
          />

          {/* Header ticks offset to chart area */}
          <g transform={`translate(${LABEL_COL_WIDTH}, 0)`}>
            {renderHeader()}
          </g>

          {/* Grid lines in chart area */}
          <g transform={`translate(${LABEL_COL_WIDTH}, 0)`}>
            {renderGridLines()}
          </g>

          {/* Activation band */}
          {renderActivationBand()}

          {/* Rows (labels + bars) */}
          {renderRows()}

          {/* Dependency arrows (in chart coordinate space) */}
          <g transform={`translate(${LABEL_COL_WIDTH}, 0)`}>
            {renderDependencyArrows()}
          </g>

          {/* Today line */}
          <g transform={`translate(${LABEL_COL_WIDTH}, 0)`}>
            {renderTodayLine()}
          </g>
        </svg>
      </div>

      {/* Task detail modal */}
      {selectedTask && (
        <TaskDetailModal
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onSave={(updated) => {
            setLocalTasks((prev) =>
              prev.map((t) => (t.id === updated.id ? updated : t))
            );
            onTaskUpdate?.(updated);
            setSelectedTask(null);
          }}
        />
      )}
    </div>
  );
}
