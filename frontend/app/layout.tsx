import '../styles/globals.css';
import type { Metadata } from 'next';
import Providers from './providers';
import SidebarNav from '../components/SidebarNav';

export const metadata: Metadata = {
  title: 'Global Regime-Adaptive Portfolio Studio',
  description: 'Portfolio analytics and regime-adaptive platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="flex min-h-screen bg-slate-950 text-slate-100">
            <SidebarNav />
            <main className="flex-1 p-8">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
