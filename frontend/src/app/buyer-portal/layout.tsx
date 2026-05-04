import { BuyerPortalShell } from "@/components/BuyerPortalShell";

export default function BuyerPortalLayout({ children }: { children: React.ReactNode }) {
  return <BuyerPortalShell>{children}</BuyerPortalShell>;
}
