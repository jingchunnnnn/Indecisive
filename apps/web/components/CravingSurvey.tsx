"use client";

import { ConstraintChips } from "@/components/ConstraintChips";
import { CuisineChips } from "@/components/CuisineChips";
import { ErrorState } from "@/components/ErrorState";
import { LoadingState } from "@/components/LoadingState";
import { MoodChips } from "@/components/MoodChips";
import { PlaceTypeChips } from "@/components/PlaceTypeChips";
import { RadiusSelector } from "@/components/RadiusSelector";
import { RemarksBox } from "@/components/RemarksBox";
import { fetchRecommendations } from "@/lib/api";
import {
  CONSTRAINT_OPTIONS,
  CUISINE_OPTIONS,
  LATEST_REQUEST_KEY,
  LATEST_RESULTS_KEY,
  MOOD_OPTIONS,
  PLACE_TYPE_OPTIONS,
  RADIUS_OPTIONS
} from "@/lib/constants";
import { requestBrowserLocation } from "@/lib/geolocation";
import { getLocalPreferences, resetLocalPreferences } from "@/lib/localPreferences";
import type { RecommendRequest } from "@/lib/types";
import { ArrowLeft, ArrowRight, Search, Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

type SurveyState = {
  moods: string[];
  cuisines: string[];
  placeTypes: string[];
  constraints: string[];
  radiusM: number;
  remarks: string;
};

const initialSurvey: SurveyState = {
  moods: [],
  cuisines: [],
  placeTypes: [],
  constraints: [],
  radiusM: 2000,
  remarks: ""
};

const TOTAL_STEPS = 6;

export function CravingSurvey() {
  const router = useRouter();
  const [survey, setSurvey] = useState<SurveyState>(initialSurvey);
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [preferencesReset, setPreferencesReset] = useState(false);

  const hasInput =
    survey.moods.length > 0 ||
    survey.cuisines.length > 0 ||
    survey.placeTypes.length > 0 ||
    survey.constraints.length > 0 ||
    survey.remarks.trim().length > 0;

  async function submitSurvey({ allowEmptyRemarks = false }: { allowEmptyRemarks?: boolean } = {}) {
    if (currentStep < TOTAL_STEPS) {
      goNext();
      return;
    }

    if (!hasInput) {
      setError("Pick at least one craving option or add a little note.");
      return;
    }

    if (!allowEmptyRemarks && !survey.remarks.trim()) {
      setError("Add a note or skip this step.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setPreferencesReset(false);

    try {
      const location = await requestBrowserLocation();
      const payload: RecommendRequest = {
        survey: {
          moods: survey.moods,
          cuisines: survey.cuisines,
          place_types: survey.placeTypes,
          constraints: survey.constraints,
          radius_m: survey.radiusM
        },
        remarks: survey.remarks.trim(),
        location,
        user_preferences: getLocalPreferences()
      };
      const response = await fetchRecommendations(payload);

      window.sessionStorage.setItem(LATEST_REQUEST_KEY, JSON.stringify(payload));
      window.sessionStorage.setItem(LATEST_RESULTS_KEY, JSON.stringify(response));
      router.push("/results");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "We could not find food right now.");
    } finally {
      setIsLoading(false);
    }
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void submitSurvey();
  }

  function resetPreferences() {
    resetLocalPreferences();
    setPreferencesReset(true);
  }

  function goBack() {
    setError(null);
    setCurrentStep((step) => Math.max(1, step - 1));
  }

  function goNext() {
    setError(null);
    if (currentStep === 1 && survey.moods.length === 0) {
      setError("Pick at least one food mood.");
      return;
    }
    if (currentStep === 2 && survey.cuisines.length === 0) {
      setError("Pick a cuisine or choose Anything works.");
      return;
    }
    if (currentStep === 3 && survey.placeTypes.length === 0) {
      setError("Pick at least one place type.");
      return;
    }
    setCurrentStep((step) => Math.min(TOTAL_STEPS, step + 1));
  }

  const stepTitle = [
    "What kind of food mood are you in?",
    "Any cuisine you're craving?",
    "What kind of place sounds good?",
    "Any deal-breakers?",
    "How far are you willing to go?",
    "Anything else?"
  ][currentStep - 1];

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-lg border border-white/75 bg-white/92 p-4 shadow-soft backdrop-blur sm:p-5"
    >
      <div className="mb-4">
        <div className="mb-3 flex items-center justify-between gap-3">
          <span className="rounded-full bg-rose-50 px-3 py-1.5 text-xs font-black uppercase tracking-normal text-coral ring-1 ring-rose-100">
            Step {currentStep} of {TOTAL_STEPS}
          </span>
          <div className="h-2 flex-1 overflow-hidden rounded-full bg-rose-50 ring-1 ring-rose-100">
            <div
              className="h-full rounded-full bg-gradient-to-r from-coral to-melon transition-all"
              style={{ width: `${(currentStep / TOTAL_STEPS) * 100}%` }}
            />
          </div>
        </div>
        <AnswerSummary survey={survey} currentStep={currentStep} onEdit={setCurrentStep} />
      </div>

      <div className="min-h-[15rem]">
        <section className="rounded-lg border border-rose-100 bg-white/55 p-4 shadow-sm shadow-rose-100/30">
          <label className="mb-4 block text-lg font-black leading-tight text-cocoa sm:text-xl">
            {stepTitle}
          </label>

          {currentStep === 1 ? (
            <MoodChips value={survey.moods} onChange={(moods) => setSurvey({ ...survey, moods })} />
          ) : null}

          {currentStep === 2 ? (
            <CuisineChips value={survey.cuisines} onChange={(cuisines) => setSurvey({ ...survey, cuisines })} />
          ) : null}

          {currentStep === 3 ? (
            <PlaceTypeChips
              value={survey.placeTypes}
              onChange={(placeTypes) => setSurvey({ ...survey, placeTypes })}
            />
          ) : null}

          {currentStep === 4 ? (
            <div className="space-y-4">
              <ConstraintChips
                value={survey.constraints}
                onChange={(constraints) => setSurvey({ ...survey, constraints })}
              />
              <button
                type="button"
                onClick={() => {
                  setSurvey({ ...survey, constraints: [] });
                  setCurrentStep(5);
                }}
                className="rounded-lg border border-rose-100 bg-white/85 px-4 py-2 text-sm font-black text-stone-700 shadow-sm hover:bg-rose-50"
              >
                No deal-breakers
              </button>
            </div>
          ) : null}

          {currentStep === 5 ? (
            <RadiusSelector value={survey.radiusM} onChange={(radiusM) => setSurvey({ ...survey, radiusM })} />
          ) : null}

          {currentStep === 6 ? (
            <RemarksBox value={survey.remarks} onChange={(remarks) => setSurvey({ ...survey, remarks })} />
          ) : null}
        </section>
      </div>

      <div className="mt-4 space-y-3">
        {error ? <ErrorState message={error} onRetry={() => void submitSurvey()} /> : null}
        {isLoading ? <LoadingState /> : null}

        <div className="flex flex-col gap-2 sm:flex-row">
          {currentStep > 1 ? (
            <button
              type="button"
              onClick={goBack}
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-rose-100 bg-white/85 px-5 py-3 text-base font-black text-cocoa shadow-sm transition hover:-translate-y-0.5 hover:bg-rose-50"
            >
              <ArrowLeft className="h-5 w-5" aria-hidden="true" />
              Back
            </button>
          ) : null}

          {currentStep < TOTAL_STEPS ? (
            <button
              type="button"
              onClick={goNext}
              className="inline-flex min-h-12 flex-1 items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-coral to-melon px-5 py-3 text-base font-black text-white shadow-lg shadow-rose-200 transition hover:-translate-y-0.5"
            >
              Continue
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </button>
          ) : (
            <>
              {!survey.remarks.trim() ? (
                <button
                  type="button"
                  disabled={isLoading}
                  onClick={() => void submitSurvey({ allowEmptyRemarks: true })}
                  className="inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-rose-100 bg-white/85 px-5 py-3 text-base font-black text-cocoa shadow-sm transition hover:-translate-y-0.5 hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Skip note
                  <ArrowRight className="h-5 w-5" aria-hidden="true" />
                </button>
              ) : null}
              <button
                type="submit"
                disabled={isLoading || !survey.remarks.trim()}
                className="inline-flex min-h-12 flex-1 items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-coral to-melon px-5 py-3 text-base font-black text-white shadow-lg shadow-rose-200 transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Search className="h-5 w-5" aria-hidden="true" />
                Find food
              </button>
            </>
          )}
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-stone-600">
          <button
            type="button"
            onClick={resetPreferences}
            className="inline-flex items-center gap-2 rounded-lg bg-white/80 px-3 py-2 font-bold text-stone-700 shadow-sm hover:bg-stone-50"
          >
            <Trash2 className="h-4 w-4" aria-hidden="true" />
            Reset preferences
          </button>
          {preferencesReset ? <span>Preferences reset.</span> : null}
        </div>
      </div>
    </form>
  );
}

function AnswerSummary({
  survey,
  currentStep,
  onEdit
}: {
  survey: SurveyState;
  currentStep: number;
  onEdit: (step: number) => void;
}) {
  const summaries = [
    {
      step: 1,
      label: "Mood",
      value: labelsFor(survey.moods, MOOD_OPTIONS)
    },
    {
      step: 2,
      label: "Cuisine",
      value: labelsFor(survey.cuisines, CUISINE_OPTIONS)
    },
    {
      step: 3,
      label: "Place",
      value: labelsFor(survey.placeTypes, PLACE_TYPE_OPTIONS)
    },
    {
      step: 4,
      label: "Deals",
      value: survey.constraints.length ? labelsFor(survey.constraints, CONSTRAINT_OPTIONS) : "None"
    },
    {
      step: 5,
      label: "Distance",
      value: RADIUS_OPTIONS.find((option) => option.value === survey.radiusM)?.label || `${survey.radiusM}m`
    }
  ].filter((item) => currentStep > item.step);

  if (!summaries.length) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {summaries.map((item) => (
        <button
          key={item.step}
          type="button"
          onClick={() => onEdit(item.step)}
          className="rounded-full bg-white/85 px-3 py-2 text-left text-xs font-bold text-stone-700 shadow-sm ring-1 ring-rose-100 hover:bg-rose-50"
        >
          <span className="text-coral">{item.label}:</span> {item.value}
        </button>
      ))}
    </div>
  );
}

function labelsFor(values: string[], options: { label: string; value: string }[]) {
  const lookup = new Map(options.map((option) => [option.value, option.label]));
  return values.map((value) => lookup.get(value) || value).join(", ");
}
