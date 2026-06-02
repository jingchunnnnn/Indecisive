"use client";

import { PLACE_TYPE_OPTIONS } from "@/lib/constants";

type Props = {
  value: string[];
  onChange: (value: string[]) => void;
};

export function PlaceTypeChips({ value, onChange }: Props) {
  function toggle(option: string) {
    onChange(value.includes(option) ? value.filter((item) => item !== option) : [...value, option]);
  }

  return (
    <div className="flex flex-wrap gap-2">
      {PLACE_TYPE_OPTIONS.map((option) => {
        const isSelected = value.includes(option.value);
        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={isSelected}
            onClick={() => toggle(option.value)}
            className={[
              "min-h-10 rounded-full border px-4 py-2 text-sm font-semibold transition hover:-translate-y-0.5 hover:shadow-sm",
              isSelected
                ? "border-rose-400 bg-gradient-to-r from-pink-100 to-stone-50 text-cocoa shadow-sm"
                : "border-rose-100 bg-white/70 text-stone-700 shadow-sm shadow-rose-100/25 hover:border-rose-300 hover:bg-rose-50/70"
            ].join(" ")}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
