import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  blockedDealRooms,
  closingCoordinationChecklists,
  closingNextBestActions,
  closingReadyDealRooms,
  dealRoomBlockers,
  formatCurrency,
  getDeal,
  getLead,
  projectedAssignmentFeesAtRisk
} from "@/lib/demo-data";

export default function ClosingCoordinationPage() {
  const openBlockers = dealRoomBlockers.filter((blocker) => !blocker.resolved);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Closing Coordination Gate"
        title="Governed readiness and blocker control"
        description="The coordination layer ranks what must be resolved before a deal can be treated as closing-ready, while keeping every real-world step owner-controlled."
      />
      <div className="metric-grid">
        <MetricCard label="Deal rooms" value={String(activeDealRooms.length)} detail="Unified internal records" />
        <MetricCard label="Closing-ready" value={String(closingReadyDealRooms.length)} detail="Checklist clear" />
        <MetricCard label="Open blockers" value={String(openBlockers.length)} detail="No external action" />
        <MetricCard label="Fees at risk" value={formatCurrency(projectedAssignmentFeesAtRisk)} detail="Projected spread behind blockers" />
      </div>

      <div className="grid-two">
        <Section title="Coordination Readiness">
          <table className="data-table">
            <thead>
              <tr>
                <th>Deal Room</th>
                <th>Property</th>
                <th>Checklist</th>
                <th>Owner</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {closingCoordinationChecklists.map((checklist) => {
                const room = activeDealRooms.find((item) => item.id === checklist.dealRoomId);
                const deal = room ? getDeal(room.dealId) : undefined;
                const lead = deal ? getLead(deal.leadId) : undefined;
                return (
                  <tr key={checklist.id}>
                    <td>
                      <Link href={`/dashboard/deal-room/${checklist.dealRoomId}`}>{checklist.dealRoomId}</Link>
                      <div className="record-meta">{checklist.id}</div>
                    </td>
                    <td>{lead?.city}, {lead?.state}<div className="record-meta">{room?.dealId}</div></td>
                    <td>{checklist.blockedReasons.length ? checklist.blockedReasons.join(", ") : "complete"}</td>
                    <td><Pill tone={checklist.ownerApprovalComplete ? "green" : "red"}>{checklist.ownerApprovalComplete ? "approved" : "missing"}</Pill></td>
                    <td><Pill tone={checklist.readinessStatus === "checklist_complete" ? "green" : "red"}>{checklist.readinessStatus}</Pill></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </Section>

        <Section title="Next Best Actions">
          <div className="record-list">
            {closingNextBestActions.slice(0, 8).map((item) => (
              <RecordCard
                key={`${item.dealRoomId}-${item.action}`}
                title={item.action}
                meta={`${item.dealRoomId} / ${item.dealId}. Recommendation only; no automation.`}
                right={<Pill tone="gold">internal</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Blocked Deal Rooms">
        <div className="grid-three">
          {blockedDealRooms.map((room) => (
            <RecordCard
              key={room.id}
              title={room.id}
              meta={room.blockers.join(", ")}
              right={<Pill tone="red">{formatCurrency(room.projectedAssignmentFeeAtRisk)}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
