import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  assignmentReadyDealRooms,
  blockedDealRooms,
  closingReadyDealRooms,
  formatCurrency,
  getDeal,
  getDealRoomBlockers,
  getLead,
  projectedAssignmentFeesAtRisk
} from "@/lib/demo-data";

export default function DealRoomPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V7 Unified Deal Room"
        title="Internal closing coordination command"
        description="Seller offer room, buyer deal room, contract control, title handoff, communications, and assignment readiness are joined into one governed coordination view."
      />
      <div className="metric-grid">
        <MetricCard label="Active deal rooms" value={String(activeDealRooms.length)} detail="Internal source-of-truth records" />
        <MetricCard label="Closing-ready" value={String(closingReadyDealRooms.length)} detail="All coordination gates clear" />
        <MetricCard label="Blocked rooms" value={String(blockedDealRooms.length)} detail="Blockers require operator handling" />
        <MetricCard label="Fees at risk" value={formatCurrency(projectedAssignmentFeesAtRisk)} detail="Projected assignment fees behind blockers" />
      </div>

      <Section title="Unified Deal Rooms">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal Room</th>
              <th>Property</th>
              <th>Portals</th>
              <th>Title / Assignment</th>
              <th>Blockers</th>
              <th>Fee At Risk</th>
            </tr>
          </thead>
          <tbody>
            {activeDealRooms.map((room) => {
              const deal = getDeal(room.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const blockers = getDealRoomBlockers(room.id);
              return (
                <tr key={room.id}>
                  <td>
                    <Link href={`/dashboard/deal-room/${room.id}`}>{room.id}</Link>
                    <div className="record-meta">{room.coordinationStatus}</div>
                  </td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{room.dealId}</div></td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={room.sellerPortalStatus === "visible" ? "green" : "red"}>seller {room.sellerPortalStatus}</Pill>
                      <Pill tone={room.buyerPortalStatus === "visible" ? "green" : "red"}>buyer {room.buyerPortalStatus}</Pill>
                    </div>
                  </td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={room.titleHandoffStatus === "draft_ready" ? "green" : "gold"}>{room.titleHandoffStatus}</Pill>
                      <Pill tone={room.assignmentReadinessStatus === "assignment_ready" ? "green" : "red"}>{room.assignmentReadinessStatus}</Pill>
                    </div>
                  </td>
                  <td>{blockers.length ? blockers.map((blocker) => blocker.blockerType).join(", ") : "clear"}</td>
                  <td className="money">{formatCurrency(room.projectedAssignmentFeeAtRisk)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Coordination Boundaries">
          <div className="record-list">
            <RecordCard title="Legal execution" meta="Executable contract generation remains blocked." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Title submission" meta="Title-company submission remains manual and owner-controlled." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Payment handling" meta="No payment collection or disbursement exists in this layer." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Negotiation automation" meta="Buyer and seller negotiation steps are recommendations only." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
        <Section title="Assignment-Ready Deal Rooms">
          <div className="record-list">
            {assignmentReadyDealRooms.map((room) => {
              const deal = getDeal(room.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <RecordCard
                  key={room.id}
                  title={room.id}
                  meta={`${lead?.city ?? "Unknown"}, ${lead?.state ?? ""} / ${room.closingTimeline}`}
                  right={<Pill tone="green">ready</Pill>}
                />
              );
            })}
          </div>
        </Section>
      </div>
    </div>
  );
}
