import { TaskTier } from "@/lib/store";

const TIER_CONFIG: Record<
    TaskTier,
    { label: string; color: string; bg: string; dot: string }
> = {
    "Survival-critical": {
        label: "Critical",
        color: "text-red-400",
        bg: "bg-red-500/10 border-red-500/20",
        dot: "bg-red-400",
    },
    "Long-term meaningful": {
        label: "Meaningful",
        color: "text-purple-400",
        bg: "bg-purple-500/10 border-purple-500/20",
        dot: "bg-purple-400",
    },
    "Routine repetitive": {
        label: "Routine",
        color: "text-blue-400",
        bg: "bg-blue-500/10 border-blue-500/20",
        dot: "bg-blue-400",
    },
    Noise: {
        label: "Noise",
        color: "text-gray-500",
        bg: "bg-gray-500/10 border-gray-500/20",
        dot: "bg-gray-500",
    },
};

export function getTierConfig(tier: TaskTier) {
    return TIER_CONFIG[tier];
}

export function TierBadge({ tier }: { tier: TaskTier }) {
    const cfg = getTierConfig(tier);
    return (
        <span
            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${cfg.bg} ${cfg.color}`}
        >
            <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot}`} />
            {cfg.label}
        </span>
    );
}

export function ScoreRing({ score }: { score: number }) {
    const radius = 28;
    const circumference = 2 * Math.PI * radius;
    const filled = (score / 100) * circumference;
    const color =
        score >= 80
            ? "#ef4444"
            : score >= 60
                ? "#a855f7"
                : score >= 30
                    ? "#3b82f6"
                    : "#6b7280";

    return (
        <svg width="72" height="72" className="rotate-[-90deg]">
            <circle
                cx="36"
                cy="36"
                r={radius}
                fill="none"
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="4"
            />
            <circle
                cx="36"
                cy="36"
                r={radius}
                fill="none"
                stroke={color}
                strokeWidth="4"
                strokeDasharray={`${filled} ${circumference}`}
                strokeLinecap="round"
                style={{ transition: "stroke-dasharray 0.6s ease" }}
            />
            <text
                x="36"
                y="36"
                textAnchor="middle"
                dominantBaseline="central"
                fill={color}
                fontSize="13"
                fontWeight="600"
                style={{ transform: "rotate(90deg)", transformOrigin: "36px 36px" }}
            >
                {Math.round(score)}
            </text>
        </svg>
    );
}
