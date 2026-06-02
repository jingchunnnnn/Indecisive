"use client";

import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { fetchPlaceDetails } from "@/lib/api";
import type { PlaceDetails } from "@/lib/types";
import { ArrowLeft, ExternalLink, MapPin } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

function formatType(type: string) {
  return type.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export default function PlacePage() {
  const params = useParams<{ placeId: string }>();
  const placeId = params.placeId;
  const [place, setPlace] = useState<PlaceDetails | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    fetchPlaceDetails(placeId)
      .then((details) => {
        if (isMounted) {
          setPlace(details);
          setError(null);
        }
      })
      .catch((caught) => {
        if (isMounted) {
          setError(caught instanceof Error ? caught.message : "Place details are not available.");
        }
      })
      .finally(() => {
        if (isMounted) {
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [placeId]);

  return (
    <main className="min-h-screen px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <Link
          href="/results"
          className="inline-flex items-center gap-2 rounded-lg bg-white/80 px-4 py-2 text-sm font-bold text-cocoa shadow-sm hover:bg-white"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Back to results
        </Link>

        <section className="mt-6 rounded-lg border border-white/70 bg-white/90 p-6 shadow-soft">
          {loading ? (
            <p className="text-sm font-bold text-stone-600">Fetching place details...</p>
          ) : error ? (
            <ErrorState message={error} />
          ) : place ? (
            <div>
              <h1 className="text-3xl font-black leading-tight text-cocoa">{place.name}</h1>
              {place.address ? (
                <p className="mt-4 flex items-start gap-2 text-sm leading-6 text-stone-600">
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-coral" aria-hidden="true" />
                  {place.address}
                </p>
              ) : null}
              <div className="mt-5 flex flex-wrap gap-2">
                {place.types.map((type) => (
                  <span key={type} className="rounded-full bg-teal-50 px-3 py-1.5 text-sm font-semibold text-cocoa">
                    {formatType(type)}
                  </span>
                ))}
              </div>
              {place.google_maps_uri ? (
                <a
                  href={place.google_maps_uri}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-6 inline-flex items-center gap-2 rounded-lg bg-cocoa px-4 py-2 text-sm font-bold text-white hover:bg-stone-800"
                >
                  <ExternalLink className="h-4 w-4" aria-hidden="true" />
                  Open in Google Maps
                </a>
              ) : null}
            </div>
          ) : (
            <EmptyState title="Place details are unavailable." message="The recommendation may still open in Maps." />
          )}
        </section>
      </div>
    </main>
  );
}
