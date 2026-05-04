export function RecordCard({
  title,
  meta,
  right,
  children
}: {
  title: string;
  meta?: string;
  right?: React.ReactNode;
  children?: React.ReactNode;
}) {
  return (
    <article className="record-card">
      <div className="record-head">
        <div className="compact">
          <h3>{title}</h3>
          {meta ? <span className="record-meta">{meta}</span> : null}
        </div>
        {right}
      </div>
      {children}
    </article>
  );
}
