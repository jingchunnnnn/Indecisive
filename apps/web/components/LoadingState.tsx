import { LoaderCircle, MapPin, Sparkles } from "lucide-react";
import Image from "next/image";

const loadingPolaroids = [
  {
    src: "/images/polaroid-web-truffle-pasta.jpg",
    className: "-left-4 top-8 w-24 -rotate-6 sm:left-8 sm:w-28"
  },
  {
    src: "/images/polaroid-web-sashimi.jpg",
    className: "right-0 top-4 w-24 rotate-6 sm:right-10 sm:w-28"
  },
  {
    src: "/images/polaroid-web-fine-dessert.jpg",
    className: "bottom-4 left-10 w-24 rotate-5 sm:left-20 sm:w-28"
  },
  {
    src: "/images/polaroid-web-wagyu.jpg",
    className: "bottom-8 right-8 w-24 -rotate-5 sm:right-20 sm:w-28"
  }
];

export function LoadingState() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-hidden bg-[linear-gradient(115deg,rgba(255,248,237,0.98),rgba(255,241,242,0.98)_46%,rgba(253,232,240,0.96))] px-4">
      <div className="pointer-events-none absolute inset-0 hidden sm:block" aria-hidden="true">
        {loadingPolaroids.map((polaroid) => (
          <figure
            key={polaroid.src}
            className={[
              "absolute rounded-sm bg-white p-2 pb-6 shadow-soft ring-1 ring-rose-100",
              polaroid.className
            ].join(" ")}
          >
            <Image
              src={polaroid.src}
              alt=""
              width={280}
              height={280}
              className="aspect-square w-full rounded-sm object-cover"
            />
          </figure>
        ))}
      </div>

      <section className="relative w-full max-w-md rounded-lg border border-white/80 bg-white/90 p-6 text-center shadow-soft backdrop-blur sm:p-8">
        <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-rose-50 ring-1 ring-rose-100">
          <div className="relative flex h-14 w-14 items-center justify-center rounded-full bg-white shadow-sm">
            <LoaderCircle className="h-11 w-11 animate-spin text-coral" aria-hidden="true" />
            <MapPin className="absolute h-5 w-5 text-cocoa" aria-hidden="true" />
          </div>
        </div>

        <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-rose-50 px-3 py-1 text-xs font-black uppercase tracking-normal text-coral ring-1 ring-rose-100">
          <Sparkles className="h-4 w-4" aria-hidden="true" />
          Building your shortlist
        </div>

        <h2 className="text-3xl font-black leading-tight text-cocoa">Finding places that fit.</h2>
        <p className="mt-3 text-sm font-medium leading-6 text-stone-600">
          Matching your craving, cuisine picks, distance, and local spots.
        </p>

        <div className="mt-6 h-2 overflow-hidden rounded-full bg-rose-50 ring-1 ring-rose-100">
          <div className="h-full w-1/2 animate-[loading-slide_1.35s_ease-in-out_infinite] rounded-full bg-gradient-to-r from-coral to-melon" />
        </div>

        <div className="mt-5 grid grid-cols-3 gap-2 text-xs font-black text-stone-600">
          <span className="rounded-full bg-white px-3 py-2 shadow-sm ring-1 ring-rose-100">Craving</span>
          <span className="rounded-full bg-white px-3 py-2 shadow-sm ring-1 ring-rose-100">Cuisine</span>
          <span className="rounded-full bg-white px-3 py-2 shadow-sm ring-1 ring-rose-100">Nearby</span>
        </div>
      </section>
    </div>
  );
}
