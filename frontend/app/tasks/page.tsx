"use client";

import { useStore } from "@/lib/store";
import { TierBadge, ScoreRing } from "@/components/TierBadge";
import { formatDistanceToNow } from "@/lib/utils";
import { Task, TaskTier } from "@/lib/store";
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

const TIER_ORDER: TaskTier[] = [
  "Survival-critical",
  "Long-term meaningful",
  "Routine repetitive",
  "Noise",
];

function TaskRow({
  task,
  onDelete,
  onFocus,
}: {
  task: Task;
  onDelete: (id: string) => void;
  onFocus: (task: Task) => void;
}) {
  const [deleting, setDeleting] = useState(false);

  const handleDelete = () => {
    setDeleting(true);
    setTimeout(() => onDelete(task.id), 300);
  };

  return (
    <div
      className={`glass-2 rounded-xl p-4 transition-all duration-300 ${deleting ? "opacity-0 scale-95 translate-x-4" : "opacity-100"}`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <TierBadge tier={task.tier} />
            {task.deadline && (
              <span className="text-[10px] text-gray-600">? {formatDistanceToNow(new Date(task.deadline))}</span>
            )}
          </div>
          <p className="text-sm font-medium text-gray-200 leading-snug mb-1">{task.description}</p>
          <p className="text-xs text-gray-600 line-clamp-1">{task.why_it_matters}</p>

          <div className="flex items-center gap-3 mt-3">
            <span className="text-[11px] text-gray-600">? {task.estimated_effort_hours}h effort</span>
            <button
              onClick={() => onFocus(task)}
              className="text-[11px] text-purple-400 hover:text-purple-300 transition-colors"
            >
              ? Set as focus
            </button>
          </div>
        </div>

        <div className="flex flex-col items-center gap-2 shrink-0">
          <ScoreRing score={task.score} />
          <button
            onClick={handleDelete}
            className="text-gray-700 hover:text-red-400 transition-colors text-sm"
            aria-label="Remove task"
          >
            ?
          </button>
        </div>
      </div>
    </div>
  );
}

export default function TasksPage() {
  const router = useRouter();
  const { tasks, deleteTask, deleteNoiseTasks, setFocusedTask } = useStore();

  const noiseTasks = tasks.filter((t) => t.tier === "Noise");

  const groupedTasks = TIER_ORDER.reduce((acc, tier) => {
    const group = tasks.filter((t) => t.tier === tier);
    if (group.length > 0) acc[tier] = group;
    return acc;
  }, {} as Record<string, Task[]>);

  const tierIcons: Record<string, string> = {
    "Survival-critical": "??",
    "Long-term meaningful": "??",
    "Routine repetitive": "??",
    Noise: "?",
  };

  return (
    <div className="flex flex-col flex-1 px-4 md:px-6 lg:px-8 pt-5 md:pt-7 pb-8 gap-5 md:gap-6 overflow-y-auto">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h1 className="text-lg md:text-xl font-bold">Task Breakdown</h1>
          <p className="text-xs text-gray-500 mt-0.5">{tasks.length} active tasks</p>
        </div>
        <Link
          href="/"
          id="back-to-focus"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/[0.06] hover:bg-white/10 border border-white/[0.08] text-xs text-gray-400 transition-all"
        >
          ? Focus
        </Link>
      </div>

      {noiseTasks.length > 0 && (
        <div
          id="noise-auto-delete-banner"
          className="rounded-xl border border-gray-700/50 bg-gray-800/40 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3"
        >
          <div>
            <p className="text-sm font-semibold text-gray-300">
              {noiseTasks.length} Noise task{noiseTasks.length > 1 ? "s" : ""} detected
            </p>
            <p className="text-xs text-gray-600 mt-0.5">These drain attention without adding value.</p>
          </div>
          <button
            id="delete-noise-btn"
            onClick={deleteNoiseTasks}
            className="shrink-0 px-3.5 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-red-400 text-xs font-semibold transition-all active:scale-95"
          >
            ?? Auto-clear
          </button>
        </div>
      )}

      {TIER_ORDER.map((tier) => {
        const group = groupedTasks[tier];
        if (!group) return null;

        return (
          <section key={tier}>
            <div className="flex items-center gap-2 mb-3">
              <span>{tierIcons[tier]}</span>
              <h2 className="text-xs uppercase tracking-widest font-semibold text-gray-500">{tier}</h2>
              <span className="bg-white/10 rounded-full text-[10px] font-bold text-gray-400 w-4 h-4 flex items-center justify-center">
                {group.length}
              </span>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-2">
              {group.map((task) => (
                <TaskRow
                  key={task.id}
                  task={task}
                  onDelete={deleteTask}
                  onFocus={(t) => {
                    setFocusedTask(t);
                    router.push("/");
                  }}
                />
              ))}
            </div>
          </section>
        );
      })}

      {tasks.length === 0 && (
        <div className="flex flex-col items-center justify-center flex-1 gap-4 text-center">
          <p className="text-5xl">??</p>
          <p className="text-lg font-bold">Task queue is empty.</p>
          <p className="text-sm text-gray-500">Your cognitive load is zero. Rest, plan, or explore.</p>
          <Link href="/" className="mt-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-sm font-semibold transition-all">
            Back to Focus
          </Link>
        </div>
      )}
    </div>
  );
}

