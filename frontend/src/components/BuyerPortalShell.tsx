import { Building2, Eye, FileClock, LockKeyhole, UserRound } from "lucide-react";
import Link from "next/link";

const portalLinks = [
  { href: "/buyer-portal", label: "Deal Room", icon: Building2 },
  { href: "/buyer-portal/deals", label: "Deals", icon: Eye },
  { href: "/buyer-portal/watchlist", label: "Watchlist", icon: FileClock },
  { href: "/buyer-portal/profile", label: "Profile", icon: UserRound }
];

export function BuyerPortalShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <h1>Buyer Deal Room</h1>
          <span>Invite-gated access</span>
        </div>
        <nav className="nav" aria-label="Buyer portal navigation">
          {portalLinks.map((link) => {
            const Icon = link.icon;
            return (
              <Link href={link.href} key={link.href} title={link.label}>
                <Icon size={18} aria-hidden="true" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>
      <main className="content">
        <div className="topbar">
          <div className="compact">
            <span className="eyebrow">Controlled Access</span>
            <strong>Sanitized buyer-facing deal room</strong>
          </div>
          <div className="operator-lock">
            <LockKeyhole size={16} aria-hidden="true" />
            Invite required
          </div>
        </div>
        {children}
      </main>
    </div>
  );
}
