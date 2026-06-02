import type { RecommendResponse } from "@/lib/types";

type Props = {
  interpreted: RecommendResponse["interpreted_craving"];
};

function titleCase(term: string) {
  return term.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function ResultSummary({ interpreted }: Props) {
  const positives = interpreted.positive_terms.slice(0, 10);
  const negatives = interpreted.negative_terms;

  return (
    <section className="rounded-lg border border-white/70 bg-white/85 p-5 shadow-soft">
      <p className="text-sm font-bold uppercase tracking-normal text-coral">We interpreted your craving as</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {positives.length ? (
          positives.map((term) => (
            <span key={term} className="rounded-full bg-teal-50 px-3 py-1.5 text-sm font-semibold text-cocoa">
              {titleCase(term)}
            </span>
          ))
        ) : (
          <span className="text-sm text-stone-600">Food nearby</span>
        )}
      </div>
      {negatives.length ? (
        <div className="mt-4">
          <p className="text-sm font-bold text-stone-700">Avoiding</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {negatives.map((term) => (
              <span key={term} className="rounded-full bg-rose-50 px-3 py-1.5 text-sm font-semibold text-rose-800">
                {titleCase(term)}
              </span>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}
