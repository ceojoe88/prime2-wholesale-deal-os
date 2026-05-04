import { CalendarClock, ClipboardList, FileText, Home, LockKeyhole, MessageSquareText, WalletCards } from "lucide-react";
import Link from "next/link";

const sellerPortalLinks = [
  { href: "/seller-portal", label: "Offer Room", icon: WalletCards },
  { href: "/seller-portal/offer", label: "Offer", icon: ClipboardList },
  { href: "/seller-portal/property", label: "Property", icon: Home },
  { href: "/seller-portal/timeline", label: "Timeline", icon: CalendarClock },
  { href: "/seller-portal/documents", label: "Documents", icon: FileText },
  { href: "/seller-portal/messages", label: "Messages", icon: MessageSquareText }
];

export function SellerPortalShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <h1>Offer Review Room</h1>
          <span>Invite-gated seller access</span>
        </div>
        <nav className="nav" aria-label="Seller portal navigation">
          {sellerPortalLinks.map((link) => {
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
            <strong>Sanitized offer status and next steps</strong>
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
