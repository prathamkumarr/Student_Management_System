## Database Tables Overview
## model names:
## StudentAdmission (table name : student_admissions)
- admission_id
- full_name
- gender
- date_of_birth
- class_name
- address
- parent_phone
- parent_email
- father_name
- mother_name
- class_id
- previous_school
- created_at (timestamp)


## StudentMaster (Table name: students_master)
- student_id
- full_name
- class_id
- roll_no
- relationships (with other tables) : ClassMaster, AttendanceRecord, StudentFee, PaymentMethod, ExamFeePayment


## ClassMaster (table name: classes_master)
- class_id
- class_name
- section
- relationships : AttendanceRecord, FeeMaster, StudentFee, ExamFeeMaster


## SubjectMaster (table names: subjects_master)
- subject_id
- subject_name
- relationships : AttendanceRecord


## FeeMaster (table name: fees_master)
- fee_id
- class_id
- fee_type
- amount
- currency
- effective_from
- effective_to
- notes
- is_active
- created_at
- updated_at
- relationships : StudentFee


## ExamFeeMaster (table name: exam_fee_master)
- exam_fee_id
- class_id
- exam type
- amount
- effective_from
- effective_to
- is_active


## TeacherMaster (table name: teachers_master)
- teacher_id
- full_name
- subject_id
- email
- phone
- relationships : AttendanceRecord, TeacherAttendance


## PaymentMethod (table name: payment_methods)
- method_id
- method_name
- active
- created_at
- relationships : FeePayment, ExamFeePayment


## StudentFee (table name: student_fees)
- invoice_id
- student_id
- class_id
- fee_id
- amount_due
- amount_paid
- due_date
- status
- created_at
- updated_at
- receipt_path
- relationships : FeePayment, FeeAudit


## FeePayment (table name: fee_payments)
- payment_id
- student_id
- invoice_id
- amount
- payment_method_id
- status
- created_at


## FeeAudit (table name: fee_audit)
- audit_id
- invoice_id
- changed_by
- action
- before_change
- after_change
- ts (timestamp)


## ExamFeePayment (table name: exam_fee_payments)
- payment_id
- exam_fee_id
- student_id
- amount
- payment_method_id
- status
- created_at


## AttendanceRecord (table name: attendance_records)
- attendance_id
- student_id
- class_id
- subject_id
- teacher_id
- lecture_date
- status
- remarks
- created_at
- updated_at
- student_name
- subject_name


## TeacherAttendance (table name: teacher_attendance)
- record_id
- teacher_id
- date
- check_in
- check_out
- status
- remarks
- created_at
- updated_at


