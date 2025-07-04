from flask import Blueprint, Response, jsonify, current_app
from markupsafe import escape
from einvoicing import db
from flask import render_template, request, redirect, url_for, flash
from einvoicing.student.models import Student
from einvoicing.membership.models import Membership
from einvoicing.club.models import Club
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from einvoicing.utils import login_required
from einvoicing.utils import send_student_created_email

import csv
import pandas as pd
import os

student = Blueprint('student', __name__)
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

@student.route("/create-student/", methods=['GET'])
def create_student():
    # return "<p>Tambah student</p>"
    return render_template('student/student_form.html')

@student.route("/edit-student/", methods=['GET'])
def edit_student():
    # return "<p>Tambah student</p>"
    return render_template('student/student_form.html')

@student.route("/save-student", methods=["POST"])
def save_student():
    # Get form data
    name = request.form.get('name_input')
    matric_no = request.form.get('matric_input')
    prog_code = request.form.get('progcode_input')
    prog_name = request.form.get('progname_input')
    ic_no = request.form.get('ic_input')
    semester = request.form.get('sem_input')
    session = request.form.get('session_input')

    # Validation: Check if matric number exists
    existing = Student.query.filter_by(matric_no=matric_no).first()
    if existing:
        flash('Matric number already exists. Please use a different one.', 'danger')
        return redirect(url_for('student.create_student'))
    
    # Save to database
    new_student = Student(
        name=name,
        matric_no=matric_no,
        prog_code=prog_code,
        prog_name=prog_name,
        ic_no=ic_no,
        semester=semester,
        session=session
    )

    db.session.add(new_student)
    db.session.commit()

    # Send email to all users
    send_student_created_email(new_student)

    flash("Student created successfully and notification email sent.", "success")
    return redirect(url_for('student.list_student'))  # Replace with your listing route

@student.route("/delete-student/<id>", methods=["GET"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash(f'Student {student.name} has been deleted.', 'success')
    return redirect(url_for('student.list_student'))  # Replace with your actual listing route

@student.route("/list")
@login_required
def list_student():
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Student.query

    if keyword:
        query = query.filter(
            db.or_(
                Student.name.ilike(f'%{keyword}%'),
                Student.prog_name.ilike(f'%{keyword}%'),
                Student.prog_code.ilike(f'%{keyword}%')
            )
        )

    paginated_students = query.order_by(Student.id).paginate(page=page, per_page=per_page)

    return render_template('student/list.html', students=paginated_students, keyword=keyword)
    # students = student.query.all()
    # return render_template('student/list.html', students=students)
    # res = []
    # for u in students:
    #     res.append({
    #         'id': u.id,
    #         'name': u.name,
    #         'email': u.email
    #     })

    # return jsonify(res)

@student.route('/student-graph-data')

def student_graph_data():
    # Query all students
    students = Student.query.all()

# Convert to DataFrame for image chart
    # df = pd.DataFrame([{
    #     "id": s.id,
    #     "name": s.name,
    #     "prog_code": s.prog_code,
    #     "semester": s.semester,
    #     "session": s.session
    # } for s in students])

    # Example: plot number of students per program code
    # prog_count = df['prog_code'].value_counts()

    # plt.figure(figsize=(8, 4))
    # prog_count.plot(kind='bar', color='skyblue')
    # plt.title("Jumlah Pelajar Mengikut Kod Program")
    # plt.xlabel("Kod Program")
    # plt.ylabel("Bilangan Pelajar")
    # plt.tight_layout()

    # Save plot to a PNG buffer
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # buf.seek(0)
    # plt.close()

    # return Response(buf.getvalue(), mimetype='image/png')
# End Graph Image

    # Convert to DataFrame for interactive chart
    df = pd.DataFrame([{
        "prog_code": s.prog_code
    } for s in students])

    # Count number of students by program code
    data = df['prog_code'].value_counts().to_dict()

    # Prepare data for Chart.js
    chart_data = {
        "labels": list(data.keys()),
        "values": list(data.values())
    }

    return jsonify(chart_data)

@student.route('/student-chart')
def student_chart():
    return render_template('student/student_graph.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@student.route("/upload-student-file", methods=["POST"])
def upload_student_file():
    file = request.files.get('file')

    if not file or not allowed_file(file.filename):
        flash('Invalid file format. Only .csv or .xlsx allowed.', 'danger')
        return redirect(url_for('student.list_student'))

    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    try:
        students_data = []
        if filename.endswith('.csv'):
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                students_data = list(reader)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath, engine='openpyxl')
            students_data = df.to_dict(orient='records')

        count = 0
        for row in students_data:
            # Ensure matric_no is cast to string for comparison
            matric_no = str(row['matric_no']).strip()

            # Skip if student already exists
            if Student.query.filter_by(matric_no=matric_no).first():
                continue

            # Create new student record
            student = Student(
                name=str(row['name']).strip(),
                matric_no=matric_no,
                prog_code=str(row['prog_code']).strip(),
                prog_name=str(row['prog_name']).strip(),
                ic_no=str(row['ic_no']).strip(),
                semester=str(row['semester']).strip(),
                session=str(row['session']).strip()
            )
            db.session.add(student)
            count += 1

        db.session.commit()
        flash(f'Successfully uploaded {count} new student(s).', 'success')

    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'danger')

    return redirect(url_for('student.list_student'))


@student.route('/register-membership', methods=['GET', 'POST'])
def register_membership():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        club_code = request.form.get('club_id')

        # Optional: Check if already registered
        existing = Membership.query.filter_by(student_id=student_id, club_code=club_code).first()
        if existing:
            flash('Student already registered to this club.', 'warning')
        else:
            m = Membership(student_id=student_id, club_code=club_code)
            db.session.add(m)
            db.session.commit()
            flash('Membership registered successfully!', 'success')

        return redirect(url_for('student.register_membership'))

    # Show form
    students = Student.query.all()
    clubs = Club.query.all()
    return render_template('student/register_membership.html', students=students, clubs=clubs)

@student.route('/search-student')
def search_student():
    keyword = request.args.get('keyword', '').strip()
    if keyword:
        results = Student.query.filter(
            db.or_(
                Student.name.ilike(f'%{keyword}%'),
                Student.prog_name.ilike(f'%{keyword}%'),
                Student.prog_code.ilike(f'%{keyword}%')
            )
        ).all()
    else:
        results = []

    return render_template('student/search_results.html', students=results)