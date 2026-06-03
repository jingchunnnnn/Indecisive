"use client";

import type { Recommendation } from "@/lib/types";
import { ExternalLink, MapPin, ThumbsDown, ThumbsUp } from "lucide-react";

type Props = {
  recommendation: Recommendation;
  feedbackChoice?: "good" | "bad";
  onGoodRecommendation: (recommendation: Recommendation) => void;
  onBadRecommendation: (recommendation: Recommendation) => void;
};

function formatDistance(distance: number | null) {
  if (distance === null) {
    return "Nearby";
  }
  if (distance < 1000) {
    return `${Math.round(distance)}m`;
  }
  return `${(distance / 1000).toFixed(1)}km`;
}

function formatType(type: string) {
  return type.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function RecommendationCard({
  recommendation,
  feedbackChoice,
  onGoodRecommendation,
  onBadRecommendation
}: Props) {
  const percent = Math.round(recommendation.score * 100);
  const hasFeedback = Boolean(feedbackChoice);

  return (
    <article className="rounded-lg border border-white/75 bg-white/90 p-5 shadow-soft">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-xl font-black text-cocoa">{recommendation.name}</h2>
            <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-black text-amber-700">
              {percent}% match
            </span>
          </div>
          {recommendation.address ? (
            <p className="mt-2 flex items-start gap-2 text-sm leading-6 text-stone-600">
              <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-coral" aria-hidden="true" />
              {recommendation.address}
            </p>
          ) : null}
        </div>
        <span className="w-fit rounded-full bg-teal-50 px-3 py-1.5 text-sm font-bold text-teal-800">
          {formatDistance(recommendation.distance_m)}
        </span>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {recommendation.types.slice(0, 5).map((type) => (
          <span key={type} className="rounded-full bg-stone-100 px-3 py-1 text-xs font-semibold text-stone-700">
            {formatType(type)}
          </span>
        ))}
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        {recommendation.google_maps_uri ? (
          <a
            href={recommendation.google_maps_uri}
            target="_blank"
            rel="noreferrer"
            className="inline-flex min-h-10 items-center gap-2 rounded-lg bg-cocoa px-4 py-2 text-sm font-bold text-white hover:bg-stone-800"
          >
            <ExternalLink className="h-4 w-4" aria-hidden="true" />
            Open in Google Maps
          </a>
        ) : null}
        <button
          type="button"
          aria-pressed={feedbackChoice === "good"}
          disabled={hasFeedback}
          onClick={() => onGoodRecommendation(recommendation)}
          className={[
            "inline-flex min-h-10 items-center gap-2 rounded-lg px-4 py-2 text-sm font-bold transition",
            feedbackChoice === "good"
              ? "bg-teal-600 text-white shadow-sm"
              : "bg-teal-50 text-teal-800 hover:bg-teal-100",
            feedbackChoice === "bad" ? "cursor-not-allowed opacity-45" : "",
            feedbackChoice === "good" ? "cursor-default" : ""
          ].join(" ")}
        >
          <ThumbsUp className="h-4 w-4" aria-hidden="true" />
          Good recommendation
        </button>
        <button
          type="button"
          aria-pressed={feedbackChoice === "bad"}
          disabled={hasFeedback}
          onClick={() => onBadRecommendation(recommendation)}
          className={[
            "inline-flex min-h-10 items-center gap-2 rounded-lg px-4 py-2 text-sm font-bold transition",
            feedbackChoice === "bad"
              ? "bg-cocoa text-white shadow-sm"
              : "bg-stone-100 text-stone-700 hover:bg-stone-200",
            feedbackChoice === "good" ? "cursor-not-allowed opacity-45" : "",
            feedbackChoice === "bad" ? "cursor-default" : ""
          ].join(" ")}
        >
          <ThumbsDown className="h-4 w-4" aria-hidden="true" />
          Bad recommendation
        </button>
      </div>
    </article>
  );
}
