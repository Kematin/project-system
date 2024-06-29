import io
import os
import shutil
import zipfile
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from pydantic import UUID4, BaseModel

from admin.auth import authenticate, create_access_token, verify_access_token
from config import config
from database import AsyncSessionLocal, Database, Project

admin_router = APIRouter(tags=["Admin"])
file_path = str


# dependency
async def get_db():
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


class AuthAdmin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {"example": {"username": "admin", "password": "password"}}


class ProjectCreate(BaseModel):
    name: str
    summary: str
    price: int
    have_presentation: bool
    have_product: bool
    have_unique: bool
    category: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "summary": "summary",
                "price": 799,
                "have_presentation": False,
                "have_product": False,
                "have_unique": False,
                "category": "minimum",
            }
        }


class ProjectChange(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    price: Optional[int] = None
    have_presentation: Optional[bool] = None
    have_product: Optional[bool] = None
    have_unique: Optional[bool] = None
    is_blocked: Optional[bool] = None
    category: Optional[str] = None

    class Config:
        json_schema_extra = {"example": {"price": 899, "is_blocked": True}}


@admin_router.post("/auth", status_code=status.HTTP_202_ACCEPTED)
@logger.catch(exclude=HTTPException)
async def auth_admin(data: AuthAdmin) -> dict:
    username, password = data.username, data.password
    if username != config.ADMIN_USERNAME or password != config.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials."
        )
    access_token = create_access_token(username)
    logger.info("Admin user sign in")
    return {"access_token": access_token, "token_type": "Bearer"}


@admin_router.get("/check_token", status_code=status.HTTP_202_ACCEPTED)
@logger.catch(exclude=HTTPException)
async def check_token(token: str):
    try:
        verify_access_token(token)
        return {"message": "succesfull"}
    except HTTPException as e:
        raise e


@admin_router.get("/projects")
@logger.catch(exclude=HTTPException)
async def retrieve_projects(
    category: str | None = None, db=Depends(get_db), admin: str = Depends(authenticate)
):
    project_database = Database(Project, db)
    projects = await project_database.get_all()
    if category is None:
        logger.info("Get all projects.")
        return {"projects": projects}
    elif category not in config.CATEGORIES:
        logger.warning("Invalid category for projects")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category."
        )
    else:
        projects = [
            project
            for project in projects
            if project.category == config.CATEGORIES[category]
        ]
        logger.info(f"Get projects with type: {category}")
        return {"projects": projects}


@admin_router.get("/project/{project_id}")
@logger.catch(exclude=HTTPException)
async def retrieve_single_project(
    project_id: UUID4,
    db=Depends(get_db),
    admin: str = Depends(authenticate),
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if project:
        logger.info(f"Get project {project_id}.")
        return {"project": project}
    else:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )


@admin_router.post("/project")
@logger.catch(exclude=HTTPException)
async def create_project(
    data: ProjectCreate,
    db=Depends(get_db),
    admin: str = Depends(authenticate),
):
    project_database = Database(Project, db)
    if data.category not in config.CATEGORIES:
        logger.warning(f"Invalid category for new project with data {data}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category."
        )
    data.category = config.CATEGORIES[data.category]
    project_id = await project_database.create(data.model_dump())
    os.mkdir(f"projects/{project_id}")
    logger.info(f"Create new project with data {data}")
    return {"new_id": project_id}


@admin_router.put("/project/{project_id}")
@logger.catch(exclude=HTTPException)
async def update_project(
    project_id: UUID4,
    data: ProjectChange,
    db=Depends(get_db),
    admin: str = Depends(authenticate),
):
    if data.category:
        if data.category not in config.CATEGORIES:
            logger.warning(f"Invalid category for project with data {data}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category."
            )
        else:
            data.category = config.CATEGORIES[data.category]
    project_database = Database(Project, db)
    res = await project_database.update(project_id, data.model_dump())
    if not res:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    logger.info(f"Update project with id {project_id}")
    return {"message": "successfull"}


@admin_router.delete("/project/{project_id}")
@logger.catch(exclude=HTTPException)
async def delete_project(
    project_id: UUID4, db=Depends(get_db), admin: str = Depends(authenticate)
):
    project_database = Database(Project, db)
    res = await project_database.delete(project_id)
    if res:
        shutil.rmtree(f"projects/{project_id}")
        logger.info(f"Delete project {project_id}.")
        return {"message": "successfull"}
    else:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )


@admin_router.delete("/project")
@logger.catch(exclude=HTTPException)
async def delete_projects(db=Depends(get_db), admin: str = Depends(authenticate)):
    project_database = Database(Project, db)
    await project_database.delete_all()
    projects_path = os.listdir("projects/")
    del projects_path[-1]
    for path in projects_path:
        os.rmdir(f"projects/{path}")
    logger.info("Delete all projects")
    return {"message": "succeffull"}


@admin_router.get("/logs")
@logger.catch(exclude=HTTPException)
async def get_logs(admin: str = Depends(authenticate)):
    log_file = "./logs/debug.log"
    return FileResponse(path=log_file, filename="debug.txt")


async def add_file(project_id: UUID4, file: UploadFile | None, name: str) -> None:
    if file is None:
        return
    else:
        with open(f"projects/{project_id}/" + name, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()
        logger.debug(f"ADD {name}")


async def add_product(project_id: UUID4, files: List[UploadFile] | None) -> None:
    if not len(files):
        return
    else:
        try:
            shutil.rmtree(f"projects/{project_id}/product")
        except FileNotFoundError:
            ...

        os.mkdir(f"projects/{project_id}/product")
        for file in files:
            with open(f"projects/{project_id}/product/{file.filename}", "wb") as wf:
                shutil.copyfileobj(file.file, wf)
                file.file.close()


@admin_router.post("/files/{project_id}")
@logger.catch(exclude=HTTPException)
async def add_files(
    project_id: UUID4,
    doc_file: UploadFile,
    cover_file: UploadFile,
    pptx_file: UploadFile | None = None,
    unique_file: UploadFile | None = None,
    product_files: List[UploadFile] = Form([]),
    db=Depends(get_db),
    admin: str = Depends(authenticate),
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if not project:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    else:
        await add_file(project_id, doc_file, "document.docx")
        await add_file(project_id, cover_file, "cover.png")
        await add_file(project_id, pptx_file, "presentation.pptx")
        await add_file(project_id, unique_file, "unique.png")
        await add_product(project_id, product_files)
        logger.info(f"Add files to project {project_id}")
        return {"message": "successfull"}


@admin_router.put("/files/{project_id}")
@logger.catch(exclude=HTTPException)
async def update_files(
    project_id: UUID4,
    doc_file: UploadFile | None = None,
    cover_file: UploadFile | None = None,
    pptx_file: UploadFile | None = None,
    unique_file: UploadFile | None = None,
    product_files: List[UploadFile] = Form([]),
    db=Depends(get_db),
    admin: str = Depends(authenticate),
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if not project:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    else:
        await add_file(project_id, doc_file, "document.docx")
        await add_file(project_id, cover_file, "cover.png")
        await add_file(project_id, pptx_file, "presentation.pptx")
        await add_file(project_id, unique_file, "unique.png")
        await add_product(project_id, product_files)
        logger.info(f"Change files to project {project_id}")
        return {"message": "successfull"}


@admin_router.get("/files/{project_id}")
@logger.catch(exclude=HTTPException)
async def retrieve_project_file(
    project_id: UUID4, type: str, db=Depends(get_db), admin: str = Depends(authenticate)
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if not project:
        logger.warning(f"Project with id {project_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    if type not in config.FILE_TYPES:
        logger.warning(f"Specified file type is not valid {project_id}")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Specified file type is not valid",
        )
    media_type = config.MEDIA_TYPES[type]
    if type != "doc" and type != "cover":
        if not project.__dict__[config.PROJECT_FIELDS[type]]:
            logger.warning(f"No {type} for project {project_id}")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Project dont have this type",
            )
    if type != "product":
        filename = config.FILE_TYPES[type]
        logger.info(f"Return {type} for project {project_id}")
        return FileResponse(
            path=f"projects/{project_id}/{filename}", media_type=media_type
        )
    else:
        file_dir = f"projects/{project_id}/product"
        files = os.listdir(file_dir)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file in files:
                file_path = os.path.join(file_dir, file)
                zip_file.write(file_path, arcname=file)
        zip_buffer.seek(0)

        logger.info(f"Return product zip for project {project_id}")
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type=media_type,
            headers={"Content-Disposition": "attachment;filename=project.zip"},
        )
