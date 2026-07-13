from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Form,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from schemas import CreateCaseRequest
from services.ai.case_builder import generate_case
from services.storage.case_storage import save_case

templates = Jinja2Templates(directory="templates")

page_router = APIRouter()


@page_router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
    )


@page_router.get("/cases/new")
def new_case(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/new_case.html",
    )

@page_router.post("/cases/generate")
def generate_case_page(
    request: Request,
    db: Session = Depends(get_db),

    template: str = Form("product_designer"),
    project_name: str = Form(...),
    raw_notes: str = Form(...),
):

    payload = CreateCaseRequest(
        template=template,
        project_name=project_name,
        note=raw_notes,
    )

    result = generate_case(payload.note)

    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail=result["error"],
        )

    case = save_case(
        db=db,
        request=payload,
        result=result,
    )

    return RedirectResponse(
        url=f"/cases/{case.id}/edit",
        status_code=303,
    )


@page_router.get("/cases/{case_id}/edit")
def edit_case(
    request: Request,
    case_id: str,
):
    return templates.TemplateResponse(
        request=request,
        name="pages/edit_case.html",
        context={
            "case_id": case_id,
        },
    )


@page_router.get("/archive")
def archive(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/archive.html",
    )