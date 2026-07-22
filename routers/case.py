import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories import get_cases, get_case_by_id, update_case
from schemas import (
    CreateCaseRequest,
    CaseListItem,
    CaseDetailResponse,
    UpdateCaseRequest,
    UpdateCaseRequest,
)
from services.ai.case_builder import generate_case
from services.storage.case_storage import save_case

case_router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)

@case_router.post("")
def create_case(
    request: CreateCaseRequest,
    db: Session = Depends(get_db),
):

    result = generate_case(request.note)

    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail=result["error"],
        )

    case = save_case(
        db=db,
        request=request,
        result=result,
    )

    return {
        "id": case.id,
        "title": case.title,
        "template": case.template,
        "status": case.status,
        "version": case.version,
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        "result": result,
    }


@case_router.get(
    "",
    response_model=list[CaseListItem],
)
def list_cases(
    db: Session = Depends(get_db),
):

    return get_cases(db)


@case_router.get(
    "/{case_id}",
    response_model=CaseDetailResponse,
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
):

    case = get_case_by_id(
        db=db,
        case_id=case_id,
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found.",
        )

    return {
        "id": case.id,
        "title": case.title,
        "template": case.template,
        "status": case.status,
        "version": case.version,
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        "result": json.loads(case.generated_json),
    }

@case_router.patch("/{case_id}")
def review_case_field(
    case_id: int,
    request: dict,
    db: Session = Depends(get_db),
):
    case = get_case_by_id(
        db=db,
        case_id=case_id,
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found.",
        )

    current_case = json.loads(case.generated_json)

    updates = request.get("result")

    if not isinstance(updates, dict):
        raise HTTPException(
            status_code=400,
            detail="Invalid payload.",
        )

    field_name = next(iter(updates.keys()))
    field_data = updates[field_name]

    print("=" * 80)
    print("CASE ID:")
    print(case_id)

    print("\nFULL CASE:")
    print(json.dumps(current_case, indent=2, ensure_ascii=False))

    print("\nUPDATED FIELD:")
    print(json.dumps(
        {
            field_name: field_data,
        },
        indent=2,
        ensure_ascii=False,
    ))

    print("=" * 80)

    return {
        "success": True,
        "message": "Payload received.",
        "field": field_name,
        "content": field_data.get("content"),
    }