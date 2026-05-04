export function Section({
  title,
  action,
  children
}: {
  title: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="surface">
      <div className="section-title">
        <h3>{title}</h3>
        {action}
      </div>
      {children}
    </section>
  );
}
