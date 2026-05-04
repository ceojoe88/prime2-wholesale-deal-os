import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  closingCoordinationChecklists,
  closingReadyDealRooms,
  getDeal,
  getLead
} from "@/lib/demo-data";

export default function ClosingCoordinationReadinessPage() {
  const blockedChecklists = closingCoordinationChecklists.filter(
    (checklist) => checklist.readinessStatus !== "checklist_complete"
  );
  const pofGaps = closingCoordinationChecklists.filter((checklist) => !checklist.buyerPofVerified);
  const titleGaps = closingCoordinationChecklists.filter((checklist) => !checklist.titleHandoffPrepared);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Readiness Gate"
        title="Buyer, seller, title, compliance, and owner readiness"
        description="Closing readiness requires seller acceptance, buyer match and POF, assignment confirmation, title handoff prep, compliance review, and owner approval."
      />
      <div className="metric-grid">
        <MetricCard label="Checklist records" value={String(closingCoordinationChecklists.length)} detail="Unified room checks" />
        <MetricCard label="Closing-ready" value={String(closingReadyDealRooms.length)} detail="All required conditions complete" />
        <MetricCard label="Blocked" value={String(blockedChecklists.length)} detail="One or more required items missing" />
        <MetricCard label="POF / title gaps" value={`${pofGaps.length}/${titleGaps.length}`} detail="Buyer POF and title handoff" />
      </div>
      <Section title="Readiness Matrix">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal Room</th>
              <th>Property</th>
              <th>Seller</th>
              <th>Buyer / POF</th>
              <th>Assignment / Title</th>
              <th>Compliance / Owner</th>
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
                  <td>
                    <div className="pill-row">
                      <Pill tone={checklist.sellerAcceptedOffer ? "green" : "red"}>accepted</Pill>
                      <Pill tone={checklist.sellerDocumentsRequested ? "green" : "gold"}>docs</Pill>
                    </div>
                  </td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={checklist.buyerMatched ? "green" : "red"}>matched</Pill>
                      <Pill tone={checklist.buyerPofVerified ? "green" : "red"}>POF</Pill>
                      <Pill tone={checklist.buyerIntentRecorded ? "green" : "red"}>intent</Pill>
                    </div>
                  </td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={checklist.assignmentAllowedConfirmed ? "green" : "red"}>assignment</Pill>
                      <Pill tone={checklist.titleHandoffPrepared ? "green" : "red"}>title</Pill>
                    </div>
                  </td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={checklist.complianceReviewComplete ? "green" : "red"}>compliance</Pill>
                      <Pill tone={checklist.ownerApprovalComplete ? "green" : "red"}>owner</Pill>
                    </div>
                  </td>
                  <td>{checklist.blockedReasons.length ? checklist.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
