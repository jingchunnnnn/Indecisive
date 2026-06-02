import { AlertCircle, RotateCcw } from "lucide-react";

type Props = {
  message: string;
  onRetry?: () => void;
};

export function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-4 text-rose-950">
      <div className="flex gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-rose-500" aria-hidden="true" />
        <div>
          <p className="font-bold">Tiny pause.</p>
          <p className="mt-1 text-sm leading-6">{message}</p>
          {onRetry ? (
            <button
              type="button"
              onClick={onRetry}
              className="mt-3 inline-flex items-center gap-2 rounded-lg bg-white px-3 py-2 text-sm font-bold text-rose-700 shadow-sm hover:bg-rose-100"
            >
              <RotateCcw className="h-4 w-4" aria-hidden="true" />
              Retry
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
