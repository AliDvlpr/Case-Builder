import json

from sqlalchemy.orm import Session

from models.case import CaseStudy


def create_case(
    db: Session,
    case: CaseStudy,
) -> CaseStudy:

    db.add(case)

    db.commit()

    db.refresh(case)

    return case

def get_cases(
    db: Session,
) -> list[CaseStudy]:

    return (
        db.query(CaseStudy)
        .order_by(CaseStudy.created_at.desc())
        .all()
    )

def get_case_by_id(
    db: Session,
    case_id: int,
) -> CaseStudy | None:

    return (
        db.query(CaseStudy)
        .filter(CaseStudy.id == case_id)
        .first()
    )

def update_case(
    db: Session,
    case: CaseStudy,
) -> CaseStudy:

    db.commit()
    db.refresh(case)

    return case

def update_case_content(
    db: Session,
    case: CaseStudy,
    generated_json: dict,
    status: str | None = None,
) -> CaseStudy:

    case.generated_json = json.dumps(
        generated_json,
        ensure_ascii=False,
    )

    if status is not None:
        case.status = status

    db.commit()
    db.refresh(case)

    return case