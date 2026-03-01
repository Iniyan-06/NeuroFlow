"use client";

import { useStore } from "@/lib/store";
import EnergySelector from "@/components/EnergySelector";
import CountdownTimer from "@/components/CountdownTimer";
import FocusTaskCard from "@/components/FocusTaskCard";
import OverwhelmedOverlay from "@/components/OverwhelmedOverlay";
import Link from "next/link";
import { useEffect } from "react";

export default function FocusPage() {
  const { focusedTask, isOverwhelmed, setOverwhelmed, energy, tasks, fetchRecommendation } = useStore();

  useEffect(() => {
    fetchRecommendation();
  }, [fetchRecommendation]);

  const priorityTask = focusedTask;
  const noiseCount = tasks.filter((t) => t.tier === "Noise").length;

  return (
    <>
      {isOverwhelmed && <OverwhelmedOverlay />}

      <div className="flex flex-col flex-1 px-4 md:px-6 lg:px-8 pt-5 md:pt-7 pb-8 gap-5 md:gap-6 overflow-y-auto">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h1 className="text-lg md:text-xl font-bold tracking-tight">
              NeuroFlow<span className="text-purple-400"> OS</span>
            </h1>
            <p className="text-xs text-gray-500 mt-0.5">Cognitive load cleared</p>
          </div>
          <Link
            href="/tasks"
            id="open-task-breakdown"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/[0.06] hover:bg-white/10 border border-white/[0.08] text-xs text-gray-400 transition-all"
          >
            <span>All tasks</span>
            <span className="bg-white/10 rounded-full w-4 h-4 flex items-center justify-center text-[10px] font-bold text-white">
              {tasks.length}
            </span>
          </Link>
        </div>

        <section>
          <p className="text-xs uppercase tracking-widest text-gray-600 mb-2 font-semibold">Current Energy</p>
          <EnergySelector />
        </section>

        <button
          id="overwhelmed-button"
          onClick={() => setOverwhelmed(true)}
          className="w-full py-3.5 px-4 rounded-xl border border-red-500/20 bg-red-500/[0.07] hover:bg-red-500/10 text-sm text-red-400 font-medium transition-all active:scale-[0.98] flex items-center justify-center gap-2"
        >
          <span>?????</span>
          <span>I feel overwhelmed - simplify everything</span>
        </button>

        <div className="flex items-center gap-3">
          <div className="flex-1 h-px bg-white/[0.05]" />
          <p className="text-[10px] uppercase tracking-widest text-gray-600 font-semibold">Your one thing</p>
          <div className="flex-1 h-px bg-white/[0.05]" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_300px] gap-5 md:gap-6 items-start">
          {priorityTask ? (
            <FocusTaskCard task={priorityTask} />
          ) : (
            <div className="glass rounded-2xl p-8 text-center">
              <p className="text-4xl mb-3">??</p>
              <p className="text-sm text-gray-400">All clear. No active tasks!</p>
            </div>
          )}

          <section className="glass rounded-2xl">
            <CountdownTimer durationMinutes={25} />
          </section>
        </div>

        {noiseCount > 0 && !isOverwhelmed && (
          <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 px-4 py-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
            <div>
              <p className="text-xs font-medium text-gray-400">
                {noiseCount} noise task{noiseCount > 1 ? "s" : ""} hidden
              </p>
              <p className="text-[11px] text-gray-600">Not visible. Protecting your focus.</p>
            </div>
            <Link
              href="/tasks"
              className="text-xs text-gray-500 hover:text-gray-300 transition-colors underline underline-offset-2"
            >
              Review
            </Link>
          </div>
        )}

        <p className="text-center text-[11px] text-gray-700 mt-auto">CLR Engine active · {energy} energy mode</p>
      </div>
    </>
  );
}

