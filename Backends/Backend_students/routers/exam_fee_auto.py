from datetime import date, timedelta
from sqlalchemy.orm import Session
from Backends.Shared.connection import SessionLocal
from Backends.Shared.models.exam_fee_master import ExamFeeMaster

def auto_activate_exam_fees():
    db: Session = SessionLocal()
    today = date.today()

    # Set exam fee window
    effective_from = today
    effective_to = today + timedelta(days=60)

    exam_classes = ["X", "XII"]

    for class_name in exam_classes:
        class_row = db.execute(
            "SELECT class_id FROM classes_master WHERE class_name = :cn",
            {"cn": class_name}
        ).fetchone()

        if not class_row:
            continue

        class_id = class_row[0]

        # check if exam fee already active
        exists = db.query(ExamFeeMaster).filter(
            ExamFeeMaster.class_id == class_id,
            ExamFeeMaster.is_active == True
        ).first()

        if exists:
            continue

        db.add(ExamFeeMaster(
            class_id=class_id,
            exam_type="BOARD",
            amount=2500,
            effective_from=effective_from,
            effective_to=effective_to,
            is_active=True
        ))

    db.commit()
    db.close()
