"use client";

import { Task, useStore } from "@/lib/store";
import { TierBadge, ScoreRing } from "@/components/TierBadge";
import { useRouter } from "next/navigation";
import { formatDistanceToNow } from "@/lib/utils";

interface FocusTaskCardProps {
    task: Task;
}

export default function FocusTaskCard({ task }: FocusTaskCardProps) {
    const { setFocusedTask } = useStore();
    const router = useRouter();

    const tierGlow: Record<string, string> = {
        "Survival-critical": "shadow-red-500/20",
        "Long-term meaningful": "shadow-purple-500/20",
        "Routine repetitive": "shadow-blue-500/20",
        Noise: "shadow-gray-500/10",
    };

    const tierBorderTop: Record<string, string> = {
        "Survival-critical": "border-t-red-500/60",
        "Long-term meaningful": "border-t-purple-500/60",
        "Routine repetitive": "border-t-blue-500/60",
        Noise: "border-t-gray-500/30",
    };

    return (
        <div
            id="focus-task-card"
            className={`glass rounded-2xl p-5 shadow-2xl ${tierGlow[task.tier]} border-t-2 ${tierBorderTop[task.tier]} animate-slide-up`}
        >
            {/* Header */}
            <div className="flex items-start justify-between gap-3 mb-4">
                <TierBadge tier={task.tier} />
                <ScoreRing score={task.score} />
            </div>

            {/* Task description */}
            <h2 className="text-xl font-bold leading-snug mb-1">{task.description}</h2>

            {/* Deadline */}
            {task.deadline && (
                <p className="text-xs text-gray-500 mb-4">
                    ⏰ Due {formatDistanceToNow(new Date(task.deadline))}
                </p>
            )}

            {/* Why it matters */}
            <div className="bg-white/[0.03] rounded-xl p-3.5 mb-4 border border-white/[0.06]">
                <p className="text-[11px] text-gray-500 uppercase tracking-widest mb-1 font-semibold">
                    Why this matters
                </p>
                <p className="text-sm text-gray-300 leading-relaxed">{task.why_it_matters}</p>
            </div>

            {/* Next action */}
            <div className="flex items-start gap-2.5">
                <span className="text-green-400 mt-0.5 text-base">→</span>
                <p className="text-sm text-green-300 font-medium leading-snug">{task.next_action}</p>
            </div>

            {/* Effort */}
            <div className="flex items-center gap-2 mt-4 pt-4 border-t border-white/[0.05]">
                <span className="text-xs text-gray-600">Effort:</span>
                <div className="flex gap-1">
                    {Array.from({ length: 5 }, (_, i) => (
                        <div
                            key={i}
                            className={`h-1.5 w-6 rounded-full transition-all ${i < Math.ceil(task.estimated_effort_hours / 2)
                                    ? "bg-white/40"
                                    : "bg-white/08"
                                }`}
                        />
                    ))}
                </div>
                <span className="text-xs text-gray-600 ml-1">{task.estimated_effort_hours}h</span>
            </div>
        </div>
    );
}
