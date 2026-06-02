"use client";

import { EmptyState } from "@/components/EmptyState";
import { RecommendationCard } from "@/components/RecommendationCard";
import { ResultSummary } from "@/components/ResultSummary";
import { LATEST_REQUEST_KEY, LATEST_RESULTS_KEY } from "@/lib/constants";
import { rejectRecommendation, saveRecommendation } from "@/lib/localPreferences";
import { sendFeedback } from "@/lib/api";
import type { RecommendRequest, RecommendResponse, Recommendation } from "@/lib/types";
import { ArrowLeft, RotateCcw } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function ResultsPage() {
  const [response, setResponse] = useState<RecommendResponse | null>(null);
  const [request, setRequest] = useState<RecommendRequest | undefined>();
  const [loaded, setLoaded] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  useEffect(() => {
    try {
      const raw = window.sessionStorage.getItem(LATEST_RESULTS_KEY);
      if (raw) {
        setResponse(JSON.parse(raw) as RecommendResponse);
      }
      const requestRaw = window.sessionStorage.getItem(LATEST_REQUEST_KEY);
      if (requestRaw) {
        setRequest(JSON.parse(requestRaw) as RecommendRequest);
      }
    } finally {
      setLoaded(true);
    }
  }, []);

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(null), 2400);
  }

  function feedbackContext(recommendation: Recommendation) {
    const rank = response?.recommendations.findIndex((item) => item.place_id === recommendation.place_id) ?? -1;
    return {
      request,
      rank: rank >= 0 ? rank + 1 : undefined,
      score: recommendation.score,
      distance_m: recommendation.distance_m,
      reason: recommendation.reason
    };
  }

  function onSave(recommendation: Recommendation) {
    saveRecommendation(recommendation);
    void sendFeedback(recommendation, "liked", feedbackContext(recommendation)).catch(() => undefined);
    showToast("Saved for next time.");
  }

  function onReject(recommendation: Recommendation) {
    rejectRecommendation(recommendation);
    void sendFeedback(recommendation, "not_for_me", feedbackContext(recommendation)).catch(() => undefined);
    showToast("Got it. We'll nudge away from similar places.");
  }

  if (!loaded) {
    return <main className="min-h-screen px-4 py-8" />;
  }

  if (!response) {
    return (
      <main className="min-h-screen px-4 py-8 sm:px-6">
        <div className="mx-auto max-w-3xl">
          <EmptyState />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen px-4 py-5 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl">
        <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-lg bg-white/80 px-4 py-2 text-sm font-bold text-cocoa shadow-sm hover:bg-white"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Edit survey
          </Link>
          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-lg bg-cocoa px-4 py-2 text-sm font-bold text-white shadow-sm hover:bg-stone-800"
          >
            <RotateCcw className="h-4 w-4" aria-hidden="true" />
            Try another mood
          </Link>
        </header>

        <section className="mb-6">
          <h1 className="text-4xl font-black leading-tight text-cocoa">Here are some places that match your mood.</h1>
        </section>

        <div className="space-y-5">
          <ResultSummary interpreted={response.interpreted_craving} />

          {response.recommendations.length ? (
            response.recommendations.map((recommendation) => (
              <RecommendationCard
                key={recommendation.place_id}
                recommendation={recommendation}
                onSave={onSave}
                onReject={onReject}
              />
            ))
          ) : (
            <EmptyState
              title="No matches nearby."
              message="Try a wider distance or a gentler craving combo."
            />
          )}
        </div>

        {toast ? (
          <div className="fixed bottom-4 left-1/2 z-10 w-[calc(100%-2rem)] max-w-sm -translate-x-1/2 rounded-lg bg-cocoa px-4 py-3 text-center text-sm font-bold text-white shadow-soft">
            {toast}
          </div>
        ) : null}
      </div>
    </main>
  );
}
