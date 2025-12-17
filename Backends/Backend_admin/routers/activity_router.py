from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.activity_models import ExtraCurricularActivity
from Backends.Shared.schemas.activity_schemas import ( ActivityCreate, ActivityUpdate, ActivityOut )
from Backends.Shared.models.activity_student_models import ActivityStudentMap
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.classes_master import ClassMaster


router = APIRouter( prefix="/admin/activities", tags=["Admin - Extra Curricular Activities"] )


# CREATE
@router.post("/", response_model=ActivityOut)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    new_activity = ExtraCurricularActivity(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


# READ ALL
@router.get("/")
def get_all_activities(db: Session = Depends(get_db)):
    rows = (
        db.query(
            ExtraCurricularActivity,
            TeacherMaster.full_name
        )
        .join(
            TeacherMaster,
            ExtraCurricularActivity.incharge_teacher_id == TeacherMaster.teacher_id,
            isouter=True
        )
        .order_by(ExtraCurricularActivity.activity_id)
        .all()
    )

    result = []
    for activity, teacher_name in rows:
        result.append({
            "activity_id": activity.activity_id,
            "activity_name": activity.activity_name,
            "category": activity.category or "",
            "incharge_teacher": teacher_name or "N/A",
            "created_at": (
                activity.created_at.strftime("%Y-%m-%d")
                if activity.created_at else ""
            )
        })

    return result


# READ ONE (for Edit Activity)
@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(
            ExtraCurricularActivity,
            TeacherMaster.full_name
        )
        .join(
            TeacherMaster,
            ExtraCurricularActivity.incharge_teacher_id == TeacherMaster.teacher_id,
            isouter=True
        )
        .filter(ExtraCurricularActivity.activity_id == activity_id)
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity, teacher_name = row

    return {
        "activity_id": activity.activity_id,
        "activity_name": activity.activity_name,
        "category": activity.category,
        "description": activity.description,
        "incharge_teacher_id": activity.incharge_teacher_id,
        "incharge_teacher_name": teacher_name
    }


# UPDATE
@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    activity: ActivityUpdate,
    db: Session = Depends(get_db)
):
    db_activity = db.query(ExtraCurricularActivity).filter(
        ExtraCurricularActivity.activity_id == activity_id
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    for key, value in activity.dict(exclude_unset=True).items():
        setattr(db_activity, key, value)

    db.commit()
    db.expire_all()    
    db.refresh(db_activity)

    return db_activity


# DELETE
@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(ExtraCurricularActivity).filter(
        ExtraCurricularActivity.activity_id == activity_id
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    db.delete(db_activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


# Assign Activity
@router.post("/{activity_id}/assign-students")
def assign_students_to_activity(
    activity_id: int,
    student_ids: list[int],
    db: Session = Depends(get_db)
):
    # Check activity exists
    activity = db.query(ExtraCurricularActivity).filter(
        ExtraCurricularActivity.activity_id == activity_id
    ).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    for sid in student_ids:
        # optional: check student exists
        student = db.query(StudentMaster).filter(
            StudentMaster.student_id == sid
        ).first()
        if not student:
            continue

        exists = db.query(ActivityStudentMap).filter(
            ActivityStudentMap.activity_id == activity_id,
            ActivityStudentMap.student_id == sid
        ).first()

        if not exists:
            db.add(ActivityStudentMap(
                activity_id=activity_id,
                student_id=sid
            ))

    db.commit()
    return {"message": "Students assigned successfully"}


# View/Edit
@router.get("/{activity_id}/students")
def get_activity_students(activity_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(
            StudentMaster.student_id,
            StudentMaster.full_name,
            ClassMaster.class_name,
            ClassMaster.section
        )
        .join(
            ActivityStudentMap,
            StudentMaster.student_id == ActivityStudentMap.student_id
        )
        .join(
            ClassMaster,
            StudentMaster.class_id == ClassMaster.class_id
        )
        .filter(ActivityStudentMap.activity_id == activity_id)
        .all()
    )

    return [
        {
            "student_id": r.student_id,
            "full_name": r.full_name,
            "class_name": r.class_name,
            "section": r.section
        }
        for r in rows
    ]

