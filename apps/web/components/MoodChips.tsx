"use client";

import { MOOD_OPTIONS } from "@/lib/constants";

type Props = {
  value: string[];
  onChange: (value: string[]) => void;
};

export function MoodChips({ value, onChange }: Props) {
  return (
    <ChipGrid
      options={MOOD_OPTIONS}
      selected={value}
      onChange={onChange}
      selectedClassName="border-coral bg-gradient-to-r from-rose-100 to-orange-50 text-cocoa shadow-sm"
    />
  );
}

function ChipGrid({
  options,
  selected,
  onChange,
  selectedClassName
}: {
  options: { label: string; value: string }[];
  selected: string[];
  onChange: (value: string[]) => void;
  selectedClassName: string;
}) {
  function toggle(option: string) {
    onChange(selected.includes(option) ? selected.filter((item) => item !== option) : [...selected, option]);
  }

  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => {
        const isSelected = selected.includes(option.value);
        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={isSelected}
            onClick={() => toggle(option.value)}
            className={[
              "min-h-10 rounded-full border px-4 py-2 text-sm font-semibold transition hover:-translate-y-0.5 hover:shadow-sm",
              isSelected
                ? selectedClassName
                : "border-rose-100 bg-rose-50/55 text-stone-700 shadow-sm shadow-rose-100/30 hover:border-coral/45 hover:bg-white"
            ].join(" ")}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
