
export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex w-full max-w-6xl flex-col px-6 py-10 md:px-10">
        <header className="flex items-center justify-between border-b border-border pb-4">
          <span className="text-lg font-semibold tracking-tight text-primary">
            Salvage Cars Co.
          </span>
          <a
            href="#inventory"
            className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90"
          >
            Browse Inventory
          </a>
        </header>

        <section className="grid flex-1 items-center gap-10 py-14 md:grid-cols-2">
          <div className="space-y-5">
            <p className="text-sm font-medium uppercase tracking-[0.18em] text-accent">
              Quality Rebuilt Opportunities
            </p>
            <h1 className="text-4xl font-semibold leading-tight text-primary md:text-5xl">
              Clean, trustworthy salvage vehicle listings.
            </h1>
            <p className="max-w-xl text-lg leading-8 text-muted">
              Find inspected repairable cars, trucks, and SUVs with transparent
              details, fair pricing, and fast support.
            </p>
            <div className="flex flex-col gap-3 pt-2 sm:flex-row">
              <button className="rounded-md bg-primary px-5 py-3 text-sm font-medium text-white">
                View Featured Vehicles
              </button>
              <button className="rounded-md border border-border px-5 py-3 text-sm font-medium text-primary">
                Learn How Buying Works
              </button>
            </div>
          </div>

          <div
            id="inventory"
            className="rounded-xl border border-border bg-white p-6 shadow-sm"
          >
            <h2 className="text-xl font-semibold text-primary">
              Featured Inventory Snapshot
            </h2>
            <ul className="mt-4 space-y-3 text-sm text-muted">
              <li className="flex justify-between border-b border-border pb-2">
                <span>2020 Toyota Camry SE</span>
                <span className="font-medium text-primary">$8,900</span>
              </li>
              <li className="flex justify-between border-b border-border pb-2">
                <span>2019 Ford F-150 XLT</span>
                <span className="font-medium text-primary">$12,400</span>
              </li>
              <li className="flex justify-between">
                <span>2021 Honda CR-V EX</span>
                <span className="font-medium text-primary">$10,700</span>
              </li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}
