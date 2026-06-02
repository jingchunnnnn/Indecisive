"use client";

import { REMARK_PLACEHOLDERS } from "@/lib/constants";
import { useEffect, useState } from "react";

type Props = {
  value: string;
  onChange: (value: string) => void;
};

export function RemarksBox({ value, onChange }: Props) {
  const [placeholder, setPlaceholder] = useState(REMARK_PLACEHOLDERS[0]);

  useEffect(() => {
    setPlaceholder(REMARK_PLACEHOLDERS[Math.floor(Math.random() * REMARK_PLACEHOLDERS.length)]);
  }, []);

  return (
    <textarea
      value={value}
      onChange={(event) => onChange(event.target.value)}
      placeholder={placeholder}
      rows={4}
      maxLength={300}
      className="w-full resize-none rounded-lg border border-rose-100 bg-white/85 px-4 py-3 text-base leading-7 text-cocoa shadow-sm shadow-rose-100/25 transition placeholder:text-stone-400 focus:border-coral"
    />
  );
}
