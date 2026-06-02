import { LoaderCircle } from "lucide-react";

export function LoadingState() {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-white/70 bg-white/75 px-4 py-3 text-sm font-semibold text-cocoa shadow-sm">
      <LoaderCircle className="h-5 w-5 animate-spin text-coral" aria-hidden="true" />
      Thinking with your stomach...
    </div>
  );
}
