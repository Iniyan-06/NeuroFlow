"use client";

import { create } from "zustand";

export type EnergyLevel = "Low" | "Medium" | "High";
export type TaskTier = "Survival-critical" | "Long-term meaningful" | "Routine repetitive" | "Noise";
export type TaskFrequency = "once" | "daily" | "weekly" | "monthly";

export interface Task {
  id: string;
  description: string;
  tier: TaskTier;
  score: number;
  estimated_effort_hours: number;
  deadline?: string;
  why_it_matters: string;
  next_action: string;
  frequency: TaskFrequency;
  emotional_weight?: number;
}

interface NeuroFlowStore {
  energy: EnergyLevel;
  setEnergy: (energy: EnergyLevel) => void;
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
  deleteTask: (id: string) => void;
  deleteNoiseTasks: () => void;
  isOverwhelmed: boolean;
  setOverwhelmed: (val: boolean) => void;
  focusedTask: Task | null;
  setFocusedTask: (task: Task | null) => void;
  focusMode: "auto" | "manual";
  timeAvailableMinutes: number;
  setTimeAvailableMinutes: (mins: number) => void;
  fetchRecommendation: () => Promise<void>;
}

async function persistFocusedTask(task: Task, energy: EnergyLevel, source: "manual" | "auto") {
  try {
    await fetch("/api/focus-task", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: task.description,
        energy,
        source,
        tier: task.tier,
        score: task.score,
      }),
    });
  } catch (error) {
    console.error("Failed to persist focused task:", error);
  }
}

function pickTaskByEnergy(tasks: Task[], energy: EnergyLevel, timeAvailableMinutes: number): Task | null {
  if (!tasks.length) return null;

  const nonNoise = tasks.filter((t) => t.tier !== "Noise");
  const pool = nonNoise.length ? nonNoise : tasks;
  const maxHours = Math.max(timeAvailableMinutes / 60, 0.5);

  const withinTime = pool.filter((t) => t.estimated_effort_hours <= maxHours);
  const candidates = withinTime.length ? withinTime : pool;

  if (energy === "Low") {
    return [...candidates].sort((a, b) => {
      const aRoutine = a.tier === "Routine repetitive" ? 1 : 0;
      const bRoutine = b.tier === "Routine repetitive" ? 1 : 0;
      if (aRoutine !== bRoutine) return bRoutine - aRoutine;
      if (a.estimated_effort_hours !== b.estimated_effort_hours) {
        return a.estimated_effort_hours - b.estimated_effort_hours;
      }
      return b.score - a.score;
    })[0] ?? null;
  }

  if (energy === "Medium") {
    return [...candidates].sort((a, b) => {
      const aMeaningful = a.tier === "Long-term meaningful" || a.tier === "Survival-critical" ? 1 : 0;
      const bMeaningful = b.tier === "Long-term meaningful" || b.tier === "Survival-critical" ? 1 : 0;
      if (aMeaningful !== bMeaningful) return bMeaningful - aMeaningful;
      const aDistance = Math.abs(a.estimated_effort_hours - 2);
      const bDistance = Math.abs(b.estimated_effort_hours - 2);
      if (aDistance !== bDistance) return aDistance - bDistance;
      return b.score - a.score;
    })[0] ?? null;
  }

  return [...candidates].sort((a, b) => b.score - a.score)[0] ?? null;
}

// Seed data matching the NeuroFlow scoring system
const SEED_TASKS: Task[] = [
  {
    id: "0",
    description: "Pay cloud hosting invoice before suspension",
    tier: "Survival-critical",
    score: 92.4,
    estimated_effort_hours: 0.5,
    deadline: new Date(Date.now() + 45 * 60 * 1000).toISOString(),
    why_it_matters: "Missed payment can suspend production services and cause downtime.",
    next_action: "Open billing portal now and complete payment.",
    frequency: "once",
    emotional_weight: 9,
  },
  {
    id: "1",
    description: "Fix critical auth bug in production",
    tier: "Survival-critical",
    score: 88.6,
    estimated_effort_hours: 1.5,
    deadline: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
    why_it_matters: "Users cannot log in. Every minute costs you trust and revenue.",
    next_action: "Execute immediately. Open the auth service logs now.",
    frequency: "once",
    emotional_weight: 9,
  },
  {
    id: "2",
    description: "Draft Q2 product roadmap",
    tier: "Long-term meaningful",
    score: 73.5,
    estimated_effort_hours: 4.0,
    deadline: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(),
    why_it_matters: "Defines the direction for the next 3 months. High strategic value.",
    next_action: "Schedule 3-hour deep work block. Start with user feedback.",
    frequency: "once",
    emotional_weight: 7,
  },
  {
    id: "3",
    description: "Review and merge 3 open pull requests",
    tier: "Long-term meaningful",
    score: 61.0,
    estimated_effort_hours: 1.0,
    deadline: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    why_it_matters: "Unblocks two teammates. Delays compound into missed sprint goals.",
    next_action: "Review smallest PR first. Leave inline comments.",
    frequency: "weekly",
    emotional_weight: 5,
  },
  {
    id: "8",
    description: "Submit tax filing before midnight deadline",
    tier: "Survival-critical",
    score: 90.1,
    estimated_effort_hours: 1.0,
    deadline: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString(),
    why_it_matters: "Late filing triggers penalties and compliance risk.",
    next_action: "Gather required docs and submit filing in one uninterrupted block.",
    frequency: "once",
    emotional_weight: 8,
  },
  {
    id: "4",
    description: "Update weekly team status report",
    tier: "Routine repetitive",
    score: 42.0,
    estimated_effort_hours: 0.5,
    why_it_matters: "Maintains team alignment and manager visibility.",
    next_action: "Batch with other admin tasks. Use last week's template.",
    frequency: "weekly",
    emotional_weight: 3,
  },
  {
    id: "5",
    description: "Respond to non-urgent Slack messages",
    tier: "Routine repetitive",
    score: 35.5,
    estimated_effort_hours: 0.5,
    why_it_matters: "Keeps communication healthy but not urgent.",
    next_action: "Set a 25-minute communication window at 4 PM.",
    frequency: "daily",
    emotional_weight: 2,
  },
  {
    id: "6",
    description: "Browse product hunt for trends",
    tier: "Noise",
    score: 14.0,
    estimated_effort_hours: 1.0,
    why_it_matters: "No direct impact on current priorities.",
    next_action: "Defer to evening or skip entirely.",
    frequency: "daily",
    emotional_weight: 1,
  },
  {
    id: "7",
    description: "Reorganize Notion workspace structure",
    tier: "Noise",
    score: 8.5,
    estimated_effort_hours: 2.0,
    why_it_matters: "Feels productive but produces no direct output.",
    next_action: "Archive for now. Revisit next month.",
    frequency: "monthly",
    emotional_weight: 1,
  },
];

export const useStore = create<NeuroFlowStore>((set) => ({
  energy: "Medium",
  setEnergy: (energy) => {
    const state = useStore.getState();
    const immediateFocus = pickTaskByEnergy(state.tasks, energy, state.timeAvailableMinutes);
    set({ energy, focusedTask: immediateFocus, focusMode: "auto" });
    if (immediateFocus) {
      persistFocusedTask(immediateFocus, energy, "auto");
    }
    // Trigger recommendation update when energy changes
    useStore.getState().fetchRecommendation();
  },
  tasks: SEED_TASKS,
  setTasks: (tasks) => set({ tasks }),
  deleteTask: (id) =>
    set((state) => ({ tasks: state.tasks.filter((t) => t.id !== id) })),
  deleteNoiseTasks: () =>
    set((state) => ({
      tasks: state.tasks.filter((t) => t.tier !== "Noise"),
    })),
  isOverwhelmed: false,
  setOverwhelmed: (val) => set({ isOverwhelmed: val }),
  focusedTask: SEED_TASKS[0],
  focusMode: "auto",
  setFocusedTask: (task) => {
    set({ focusedTask: task, focusMode: "manual" });
    if (task) {
      const state = useStore.getState();
      persistFocusedTask(task, state.energy, "manual");
    }
  },
  timeAvailableMinutes: 300,
  setTimeAvailableMinutes: (mins) => {
    const state = useStore.getState();
    const immediateFocus = pickTaskByEnergy(state.tasks, state.energy, mins);
    set({ timeAvailableMinutes: mins, focusedTask: immediateFocus, focusMode: "auto" });
    if (immediateFocus) {
      persistFocusedTask(immediateFocus, state.energy, "auto");
    }
    // Trigger recommendation update when time changes
    useStore.getState().fetchRecommendation();
  },
  fetchRecommendation: async () => {
    const state = useStore.getState();

    // Convert store tasks back to TaskInput format for backend
    const taskInputs = state.tasks.map(t => ({
      description: t.description,
      deadline: t.deadline,
      frequency: t.frequency,
      estimated_effort_hours: t.estimated_effort_hours,
      emotional_weight: t.emotional_weight || 5
    }));

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: json_stable_stringify({
          tasks: taskInputs,
          current_energy: state.energy,
          time_available_minutes: state.timeAvailableMinutes
        })
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        console.error("Recommendation API error:", response.status, errorPayload);
        return;
      }

      const data = await response.json();
      const latest = useStore.getState();
      if (latest.focusMode === "manual") {
        return;
      }

      // Keep energy-driven priority stable in auto mode.
      // This prevents backend latency from briefly showing one task and then overriding it.
      const energyPreferred = pickTaskByEnergy(
        latest.tasks,
        latest.energy,
        latest.timeAvailableMinutes
      );
      if (energyPreferred) {
        set({ focusedTask: energyPreferred });
        persistFocusedTask(energyPreferred, latest.energy, "auto");
        return;
      }

      if (data.selected_task) {
        // Find the actual task object from our store based on description
        // (In a real app, we'd use IDs, but here the engine returns a fresh classification)
        const recommended = state.tasks.find(t => t.description === data.selected_task.description);
        if (recommended) {
          set({ focusedTask: recommended });
          persistFocusedTask(recommended, latest.energy, "auto");
          return;
        }
      }

      const fallback = pickTaskByEnergy(state.tasks, state.energy, state.timeAvailableMinutes);
      set({ focusedTask: fallback });
      if (fallback) {
        persistFocusedTask(fallback, latest.energy, "auto");
      }
    } catch (error) {
      console.error("Failed to fetch recommendation:", error);
      const fallback = pickTaskByEnergy(state.tasks, state.energy, state.timeAvailableMinutes);
      set({ focusedTask: fallback });
      if (fallback) {
        const latest = useStore.getState();
        persistFocusedTask(fallback, latest.energy, "auto");
      }
    }
  },
}));

// Helper for JSON stringify stability
function json_stable_stringify(obj: unknown) {
  return JSON.stringify(obj);
}
