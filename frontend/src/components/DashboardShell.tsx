import {
  BadgeDollarSign,
  Bot,
  BriefcaseBusiness,
  Building2,
  Calculator,
  CircleDollarSign,
  ClipboardList,
  Clock3,
  Command,
  Crown,
  FileCheck2,
  Handshake,
  LayoutDashboard,
  ListChecks,
  LockKeyhole,
  MapPinned,
  Network,
  PhoneCall,
  ShieldCheck,
  TimerReset,
  UsersRound
} from "lucide-react";
import Link from "next/link";
import { dashboardRoutes } from "@/lib/navigation";

const icons = {
  BadgeDollarSign,
  Bot,
  BriefcaseBusiness,
  Building2,
  Calculator,
  CircleDollarSign,
  ClipboardList,
  Clock3,
  Command,
  Crown,
  FileCheck2,
  Handshake,
  LayoutDashboard,
  ListChecks,
  LockKeyhole,
  MapPinned,
  Network,
  PhoneCall,
  ShieldCheck,
  TimerReset,
  UsersRound
};

type IconName = keyof typeof icons;

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <h1>Wholesale Prime</h1>
          <span>Private Deal OS</span>
        </div>
        <nav className="nav" aria-label="Dashboard navigation">
          {dashboardRoutes.map((route) => {
            const Icon = icons[route.icon as IconName];
            return (
              <Link href={route.href} key={route.href} title={route.label}>
                <Icon size={18} aria-hidden="true" />
                <span>{route.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>
      <main className="content">
        <div className="topbar">
          <div className="compact">
            <span className="eyebrow">Owner Controlled</span>
            <strong>Acquisition-to-assignment command center</strong>
          </div>
          <div className="operator-lock">
            <LockKeyhole size={16} aria-hidden="true" />
            Single-owner private mode
          </div>
        </div>
        {children}
      </main>
    </div>
  );
}
