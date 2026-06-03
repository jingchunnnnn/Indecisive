import { CravingSurvey } from "@/components/CravingSurvey";
import Image from "next/image";

const polaroidColumns = [
  {
    id: "left-edge",
    className: "left-[-2.5rem] -top-20 w-32 gap-8 xl:left-5 xl:w-40",
    items: [
      { id: "steak-top", src: "/images/polaroid-steak-frites.png", className: "ml-8 rotate-3" },
      { id: "cake-left", src: "/images/polaroid-cake.png", className: "-rotate-3" },
      { id: "chilaquiles-left", src: "/images/polaroid-web-chilaquiles.jpg", className: "ml-5 rotate-2" },
      { id: "lamb-left", src: "/images/polaroid-lamb-chops.png", className: "-ml-4 -rotate-4" },
      { id: "panna-left", src: "/images/polaroid-web-panna-cotta.jpg", className: "ml-8 rotate-5" },
      { id: "oysters-left", src: "/images/polaroid-web-oysters.jpg", className: "-rotate-2" }
    ]
  },
  {
    id: "left-middle",
    className: "left-[8rem] top-12 w-28 gap-9 xl:left-[13rem] xl:w-36",
    items: [
      { id: "wagyu-left-mid", src: "/images/polaroid-web-wagyu.jpg", className: "-ml-3 -rotate-2" },
      { id: "truffle-pasta", src: "/images/polaroid-web-truffle-pasta.jpg", className: "ml-10 rotate-3" },
      { id: "noodles-left-mid", src: "/images/polaroid-noodles.png", className: "-rotate-3" },
      { id: "mille-feuille", src: "/images/polaroid-web-mille-feuille.jpg", className: "ml-6 rotate-2" },
      { id: "beef-tartare", src: "/images/polaroid-web-beef-tartare.jpg", className: "-ml-2 -rotate-5" }
    ]
  },
  {
    id: "left-inner",
    className: "left-[19rem] -top-8 w-24 gap-10 xl:left-[27rem] xl:w-32",
    items: [
      { id: "scallops-inner-left", src: "/images/polaroid-web-scallops.jpg", className: "ml-8 rotate-4" },
      { id: "sushi-inner-left", src: "/images/polaroid-sushi.png", className: "-ml-3 -rotate-2" },
      { id: "risotto-inner-left", src: "/images/polaroid-web-risotto.jpg", className: "ml-5 rotate-3" },
      { id: "tacos-inner-left", src: "/images/polaroid-tacos.png", className: "-rotate-4" },
      { id: "caviar-inner-left", src: "/images/polaroid-web-caviar-canapes.jpg", className: "ml-10 rotate-2" }
    ]
  },
  {
    id: "right-inner",
    className: "right-[19rem] top-8 w-24 gap-10 xl:right-[27rem] xl:w-32",
    items: [
      { id: "lobster-inner-right", src: "/images/polaroid-web-lobster.jpg", className: "-ml-2 -rotate-3" },
      { id: "omakase-inner-right", src: "/images/polaroid-web-omakase.jpg", className: "ml-8 rotate-2" },
      { id: "fine-dining-inner-right", src: "/images/polaroid-fine-dining.png", className: "-rotate-4" },
      { id: "paella-inner-right", src: "/images/polaroid-web-paella.jpg", className: "ml-6 rotate-3" },
      { id: "gnocchi-inner-right", src: "/images/polaroid-web-gnocchi.jpg", className: "-ml-4 -rotate-2" }
    ]
  },
  {
    id: "right-middle",
    className: "right-[8rem] -top-4 w-28 gap-9 xl:right-[13rem] xl:w-36",
    items: [
      { id: "poke-right-mid", src: "/images/polaroid-poke.png", className: "ml-6 rotate-2" },
      { id: "sea-bass-right-mid", src: "/images/polaroid-web-sea-bass.jpg", className: "-ml-2 -rotate-4" },
      { id: "sashimi-right-mid", src: "/images/polaroid-web-sashimi.jpg", className: "ml-9 rotate-3" },
      { id: "dim-sum-right-mid", src: "/images/polaroid-dim-sum.png", className: "-rotate-2" },
      { id: "mole-right-mid", src: "/images/polaroid-web-mole.jpg", className: "ml-5 rotate-4" }
    ]
  },
  {
    id: "right-edge",
    className: "right-[-2.5rem] top-16 w-32 gap-8 xl:right-5 xl:w-40",
    items: [
      { id: "fine-dessert-right", src: "/images/polaroid-web-fine-dessert.jpg", className: "-rotate-3" },
      { id: "duck-breast-right", src: "/images/polaroid-web-duck-breast.jpg", className: "ml-8 rotate-2" },
      { id: "biryani-right", src: "/images/polaroid-biryani.png", className: "-ml-4 -rotate-4" },
      { id: "japanese-fish-right", src: "/images/polaroid-web-japanese-grilled-fish.jpg", className: "ml-6 rotate-3" },
      { id: "shakshuka-right", src: "/images/polaroid-shakshuka.png", className: "-rotate-2" }
    ]
  }
];

export default function Home() {
  return (
    <main className="relative h-screen overflow-hidden px-4 py-3 sm:px-6 lg:px-8">
      <div className="pointer-events-none absolute inset-0 z-0 hidden select-none lg:block" aria-hidden="true">
        {polaroidColumns.map((column) => (
          <div key={column.id} className={["absolute flex flex-col", column.className].join(" ")}>
            {column.items.map((polaroid) => (
              <figure
                key={polaroid.id}
                className={[
                  "relative rounded-sm bg-white p-2 pb-7 shadow-soft ring-1 ring-rose-100",
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
        ))}
      </div>

      <div className="relative z-10 mx-auto flex h-full w-full max-w-6xl flex-col gap-6">
        <header className="flex shrink-0 justify-center pb-2 pt-0">
          <div className="brand-lockup" aria-label="Indecisive">
            <span className="brand-wordmark">Indecisive</span>
            <span className="brand-spark" aria-hidden="true" />
          </div>
        </header>

        <section className="relative min-h-0 flex-1 pt-3 lg:pt-5">
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
