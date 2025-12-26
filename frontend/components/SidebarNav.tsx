import Link from 'next/link';

const links = [
  { href: '/', label: 'Overview' },
  { href: '/universe', label: 'Universe Builder' },
  { href: '/portfolio', label: 'Portfolio Builder' },
  { href: '/asset-explorer', label: 'Asset Explorer' },
  { href: '/positions', label: 'Positions & Blotter' },
  { href: '/performance', label: 'Performance' },
  { href: '/risk-lab', label: 'Risk Lab' },
  { href: '/tail-stress', label: 'Tail & Stress' },
  { href: '/fx-hedging', label: 'FX & Hedging' },
  { href: '/optimizer', label: 'Optimizer' },
  { href: '/regime-engine', label: 'Regime Engine' },
  { href: '/reports', label: 'Reports' },
];

export default function SidebarNav() {
  return (
    <aside className="w-64 border-r border-slate-800 p-6">
      <h1 className="text-lg font-semibold">GRAPPS</h1>
      <p className="text-xs text-slate-400">Global Regime-Adaptive Studio</p>
      <nav className="mt-6 flex flex-col gap-2 text-sm">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className="rounded px-3 py-2 text-slate-300 hover:bg-slate-800 hover:text-white"
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
