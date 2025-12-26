import Link from "next/link";

const navItems = [
  { href: "/", label: "Overview" },
  { href: "/universe", label: "Universe Builder" },
  { href: "/portfolio-builder", label: "Portfolio Builder" },
  { href: "/asset-explorer", label: "Asset Explorer" },
  { href: "/positions", label: "Positions & Blotter" },
  { href: "/performance", label: "Performance" },
  { href: "/risk", label: "Risk Lab" },
  { href: "/tail", label: "Tail & Stress" },
  { href: "/fx", label: "FX & Hedging" },
  { href: "/optimizer", label: "Optimizer" },
  { href: "/regime", label: "Regime Engine" },
  { href: "/reports", label: "Reports" }
];

export function SidebarNav() {
  return (
    <aside className="w-64 border-r border-slate-200 bg-white p-6">
      <h1 className="text-lg font-semibold">Portfolio Studio</h1>
      <nav className="mt-6 space-y-2 text-sm">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block rounded px-3 py-2 text-slate-600 hover:bg-slate-100"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
