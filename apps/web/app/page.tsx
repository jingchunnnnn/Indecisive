import { CravingSurvey } from "@/components/CravingSurvey";
import Image from "next/image";

const polaroids = [
  {
    src: "/images/polaroid-cake.png",
    className: "left-0 top-8 w-40 -rotate-8 xl:left-6 xl:w-48"
  },
  {
    src: "/images/polaroid-fine-dining.png",
    className: "right-0 top-10 w-40 rotate-7 xl:right-5 xl:w-48"
  },
  {
    src: "/images/polaroid-noodles.png",
    className: "bottom-10 left-8 w-36 rotate-6 xl:left-16 xl:w-44"
  }
];

export default function Home() {
  return (
    <main className="h-screen overflow-hidden px-4 py-3 sm:px-6 lg:px-8">
      <div className="mx-auto flex h-full w-full max-w-6xl flex-col gap-6">
        <header className="flex shrink-0 justify-center pb-2 pt-0">
          <div className="brand-lockup" aria-label="Indecisive">
            <span className="brand-wordmark">Indecisive</span>
            <span className="brand-spark" aria-hidden="true" />
          </div>
        </header>

        <section className="relative min-h-0 flex-1 pt-3 lg:pt-5">
          <div className="pointer-events-none absolute inset-0 hidden lg:block" aria-hidden="true">
            {polaroids.map((polaroid) => (
              <figure
                key={polaroid.src}
                className={[
                  "absolute rounded-sm bg-white p-2 pb-7 shadow-soft ring-1 ring-rose-100",
                  polaroid.className
                ].join(" ")}
              >
                <Image
                  src={polaroid.src}
                  alt=""
                  width={360}
                  height={360}
                  className="aspect-square w-full rounded-sm object-cover"
                />
              </figure>
            ))}
          </div>

          <div className="relative z-10 mx-auto flex max-w-3xl flex-col items-center">
            <div className="mb-5 text-center">
              <h1 className="text-4xl font-black leading-tight text-cocoa sm:text-5xl lg:text-6xl">
                What are you craving?
              </h1>
              <p className="mt-3 text-base font-medium leading-7 text-stone-700 lg:text-lg">
              Tell us your mood. We&apos;ll find nearby places.
              </p>
            </div>

            <div className="w-full max-w-2xl">
              <CravingSurvey />
            </div>
          </div>
        </section>

        <footer className="shrink-0 pb-0 text-center text-xs text-stone-600">
          Powered by Google Places and a custom recommendation layer.
        </footer>
      </div>
    </main>
  );
}
