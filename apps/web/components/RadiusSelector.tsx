"use client";

import { RADIUS_OPTIONS } from "@/lib/constants";

type Props = {
  value: number;
  onChange: (value: number) => void;
};

export function RadiusSelector({ value, onChange }: Props) {
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-5">
      {RADIUS_OPTIONS.map((option) => {
        const isSelected = value === option.value;
        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={isSelected}
            onClick={() => onChange(option.value)}
            className={[
              "h-11 rounded-lg border text-sm font-bold transition hover:-translate-y-0.5 hover:shadow-sm",
              isSelected
                ? "border-coral bg-gradient-to-r from-coral to-melon text-white shadow-sm"
                : "border-rose-100 bg-white/75 text-stone-700 shadow-sm shadow-rose-100/25 hover:border-coral/45 hover:bg-rose-50/80"
            ].join(" ")}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
