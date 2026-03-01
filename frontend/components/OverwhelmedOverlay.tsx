"use client";

import { useStore } from "@/lib/store";

export default function OverwhelmedOverlay() {
    const { setOverwhelmed } = useStore();

    const steps = [
        { emoji: "🫁", text: "Breathe. 4 seconds in, hold, 4 out." },
        { emoji: "🎯", text: "You only need to do ONE thing right now." },
        { emoji: "🚫", text: "Close every app except the one you need." },
        { emoji: "⏱️", text: "Set a 15-minute timer. Start tiny." },
    ];

    return (
        <div
            id="overwhelmed-overlay"
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex flex-col items-center justify-center p-6 animate-fade-in"
        >
            <div className="w-full max-w-sm glass rounded-3xl p-6 shadow-2xl border border-white/10 animate-slide-up">
                {/* Header */}
                <div className="text-center mb-6">
                    <div className="text-5xl mb-3">🧠</div>
                    <h2 className="text-xl font-bold">You're overwhelmed.</h2>
                    <p className="text-sm text-gray-400 mt-1">That's okay. Let's simplify.</p>
                </div>

                {/* Steps */}
                <div className="flex flex-col gap-3 mb-6">
                    {steps.map((step, i) => (
                        <div
                            key={i}
                            className="flex items-start gap-3 p-3 rounded-xl bg-white/[0.04] border border-white/[0.06]"
                            style={{ animationDelay: `${i * 0.08}s` }}
                        >
                            <span className="text-2xl">{step.emoji}</span>
                            <p className="text-sm text-gray-300 leading-relaxed pt-0.5">{step.text}</p>
                        </div>
                    ))}
                </div>

                {/* Affirmation */}
                <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-3 text-center mb-5">
                    <p className="text-sm text-green-300 font-medium">
                        NeuroFlow has filtered your tasks. Only what truly matters is shown.
                    </p>
                </div>

                <button
                    id="overwhelmed-dismiss"
                    onClick={() => setOverwhelmed(false)}
                    className="w-full py-3 rounded-xl bg-white text-black font-semibold text-sm hover:bg-gray-100 transition-all active:scale-95"
                >
                    I'm ready. Show me the one thing.
                </button>
            </div>
        </div>
    );
}
