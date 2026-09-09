"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  PlaySquare, 
  Files, 
  ListChecks, 
  BarChart, 
  Settings 
} from "lucide-react";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isHome = pathname === "/";

  if (isHome) {
    return (
      <div className="min-h-screen flex flex-col">
        <header className="h-16 border-b flex items-center px-6 shrink-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <Link href="/" className="font-bold text-xl tracking-tight text-blue-600">CF Benchmark</Link>
          <nav className="ml-auto flex items-center gap-6 text-sm font-medium">
            <Link href="/dashboard" className="text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
            <Link href="/evaluate" className="text-muted-foreground hover:text-foreground transition-colors">Playground</Link>
          </nav>
        </header>
        <main className="flex-1 bg-slate-50 dark:bg-slate-950">
          {children}
        </main>
      </div>
    );
  }

  const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Playground", href: "/evaluate", icon: PlaySquare },
    { name: "Scenarios", href: "/scenarios", icon: Files },
    { name: "Evaluations", href: "/evaluations", icon: ListChecks },
    { name: "Analytics", href: "/analytics", icon: BarChart },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <div className="min-h-screen flex bg-slate-50 dark:bg-slate-950">
      <aside className="w-64 border-r bg-background flex flex-col hidden md:flex shrink-0">
        <div className="h-16 flex items-center px-6 border-b">
          <Link href="/" className="font-bold text-xl tracking-tight text-blue-600">CF Benchmark</Link>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300" 
                    : "text-muted-foreground hover:bg-slate-100 hover:text-foreground dark:hover:bg-slate-800"
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </aside>
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 border-b bg-background flex items-center px-6 md:hidden">
          <Link href="/" className="font-bold text-xl tracking-tight text-blue-600">CF Benchmark</Link>
        </header>
        <main className="flex-1 p-6 lg:p-8 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
