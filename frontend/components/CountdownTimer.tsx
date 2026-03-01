"use client";

import { useEffect, useRef, useState } from "react";

interface CountdownTimerProps {
    durationMinutes?: number;
    onComplete?: () => void;
}

function formatTime(seconds: number): string {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function CountdownTimer({
    durationMinutes = 25,
    onComplete,
}: CountdownTimerProps) {
    const totalSecs = durationMinutes * 60;
    const [secondsLeft, setSecondsLeft] = useState(totalSecs);
    const [running, setRunning] = useState(false);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        if (running) {
            intervalRef.current = setInterval(() => {
                setSecondsLeft((prev) => {
                    if (prev <= 1) {
                        clearInterval(intervalRef.current!);
                        setRunning(false);
                        onComplete?.();
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        }
        return () => clearInterval(intervalRef.current!);
    }, [running, onComplete]);

    const progress = (secondsLeft / totalSecs) * 100;
    const circumference = 2 * Math.PI * 44;
    const filled = (progress / 100) * circumference;

    const strokeColor =
        progress > 60 ? "#22c55e" : progress > 30 ? "#eab308" : "#ef4444";

    const reset = () => {
        clearInterval(intervalRef.current!);
        setRunning(false);
        setSecondsLeft(totalSecs);
    };

    return (
        <div
            id="countdown-timer"
            className="flex flex-col items-center gap-4 py-6"
        >
            <div className="relative w-28 h-28">
                <svg width="112" height="112" className="rotate-[-90deg]">
                    <circle
                        cx="56"
                        cy="56"
                        r="44"
                        fill="none"
                        stroke="rgba(255,255,255,0.05)"
                        strokeWidth="6"
                    />
                    <circle
                        cx="56"
                        cy="56"
                        r="44"
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth="6"
                        strokeDasharray={`${filled} ${circumference}`}
                        strokeLinecap="round"
                        style={{ transition: "stroke-dasharray 0.5s linear, stroke 0.5s" }}
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span
                        className="text-2xl font-bold tabular-nums"
                        style={{ color: strokeColor }}
                    >
                        {formatTime(secondsLeft)}
                    </span>
                    <span className="text-[10px] text-gray-500 uppercase tracking-widest mt-0.5">
                        focus
                    </span>
                </div>
            </div>

            <div className="flex gap-3">
                <button
                    id="timer-start-pause"
                    onClick={() => setRunning((r) => !r)}
                    className="px-5 py-2 rounded-lg bg-white/10 hover:bg-white/15 border border-white/10 text-sm font-medium transition-all"
                >
                    {running ? "⏸ Pause" : secondsLeft < totalSecs ? "▶ Resume" : "▶ Start"}
                </button>
                <button
                    id="timer-reset"
                    onClick={reset}
                    className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-gray-400 transition-all"
                >
                    ↺ Reset
                </button>
            </div>

            <p className="text-xs text-gray-600">
                Pomodoro · {durationMinutes}m session
            </p>
        </div>
    );
}
