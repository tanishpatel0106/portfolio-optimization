import "../styles/globals.css";

import type { Metadata } from "next";

import { SidebarNav } from "../components/SidebarNav";
import { QueryProvider } from "../lib/query-provider";

export const metadata: Metadata = {
  title: "Global Regime-Adaptive Portfolio Studio",
  description: "Institutional portfolio analytics platform"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <div className="flex min-h-screen">
            <SidebarNav />
            <main className="flex-1 p-6">{children}</main>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
