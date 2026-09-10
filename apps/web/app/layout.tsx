import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ClozFlow Dashboard",
  description: "Sales intelligence and sales-response evaluation platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen bg-gray-50 text-gray-900">
          {/* Sidebar */}
          <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
            <div className="h-16 flex items-center px-6 border-b border-gray-200 font-bold text-xl text-blue-600">
              ClozFlow
            </div>
            <nav className="flex-1 py-4 flex flex-col gap-1 px-3">
              <a href="/" className="px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium text-gray-700">Overview</a>
              <a href="/benchmarks" className="px-3 py-2 rounded-md bg-blue-50 text-blue-700 text-sm font-medium">CF Benchmark</a>
              <a href="#" className="px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium text-gray-700">Conversations</a>
              <a href="#" className="px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium text-gray-700">Evaluations</a>
              <a href="#" className="px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium text-gray-700">Prospects</a>
              <a href="#" className="px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium text-gray-700">Settings</a>
            </nav>
          </aside>
          {/* Main content */}
          <main className="flex-1 overflow-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
