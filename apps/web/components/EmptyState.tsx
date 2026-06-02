import Link from "next/link";
import { SearchX } from "lucide-react";

type Props = {
  title?: string;
  message?: string;
};

export function EmptyState({
  title = "No food mood saved yet.",
  message = "Head back and tell us what sounds good."
}: Props) {
  return (
    <div className="rounded-lg border border-white/70 bg-white/85 px-6 py-8 text-center shadow-soft">
      <SearchX className="mx-auto h-10 w-10 text-coral" aria-hidden="true" />
      <h2 className="mt-4 text-2xl font-black text-cocoa">{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-stone-600">{message}</p>
      <Link
        href="/"
        className="mt-5 inline-flex rounded-lg bg-cocoa px-4 py-2 text-sm font-bold text-white hover:bg-stone-800"
      >
        Back to survey
      </Link>
    </div>
  );
}
