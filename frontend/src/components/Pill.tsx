export function Pill({
  children,
  tone = "default"
}: {
  children: React.ReactNode;
  tone?: "default" | "green" | "gold" | "red";
}) {
  return <span className={`pill ${tone === "default" ? "" : tone}`}>{children}</span>;
}
