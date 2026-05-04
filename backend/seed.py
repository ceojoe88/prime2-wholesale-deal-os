from __future__ import annotations

from app.core.database import Base, SessionLocal, engine
from app.models import Agent, Buyer, BuyerMatch, ComplianceRecord, Deal, Division, Lead
from app.seed_data import seed_database


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        counts = seed_database(session)
    print("Seeded Wholesale Deal OS demo data:")
    for name, count in counts.items():
        print(f"- {name}: {count}")


if __name__ == "__main__":
    main()
