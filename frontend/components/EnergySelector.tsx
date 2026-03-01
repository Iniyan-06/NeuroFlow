"use client";

import { EnergyLevel, useStore } from "@/lib/store";

const ENERGY_OPTIONS: {
    level: EnergyLevel;
    emoji: string;
    desc: string;
    color: string;
    active: string;
}[] = [
        {
            level: "Low",
            emoji: "🪫",
            desc: "Drained",
            color: "text-orange-400",
            active: "bg-orange-500/15 border-orange-500/40 text-orange-300",
        },
        {
            level: "Medium",
            emoji: "⚡",
            desc: "Okay",
            color: "text-yellow-400",
            active: "bg-yellow-500/15 border-yellow-500/40 text-yellow-300",
        },
        {
            level: "High",
            emoji: "🔥",
            desc: "Sharp",
            color: "text-green-400",
            active: "bg-green-500/15 border-green-500/40 text-green-300",
        },
    ];

export default function EnergySelector() {
    const { energy, setEnergy } = useStore();

    return (
        <div className="flex items-center gap-2 w-full">
            {ENERGY_OPTIONS.map((opt) => {
                const isActive = energy === opt.level;
                return (
                    <button
                        key={opt.level}
                        id={`energy-${opt.level.toLowerCase()}`}
                        onClick={() => setEnergy(opt.level)}
                        className={`flex-1 flex flex-col items-center gap-1 py-3 px-2 rounded-xl border transition-all duration-200 ${isActive
                                ? opt.active + " shadow-lg scale-[1.03]"
                                : "bg-[var(--surface)] border-[var(--border-color)] text-gray-500 hover:border-white/20 hover:text-gray-300"
                            }`}
                    >
                        <span className="text-xl">{opt.emoji}</span>
                        <span className="text-xs font-semibold">{opt.level}</span>
                        <span className="text-[10px] opacity-70">{opt.desc}</span>
                    </button>
                );
            })}
        </div>
    );
}
