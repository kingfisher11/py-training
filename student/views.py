from flask import Blueprint, Response, jsonify
from markupsafe import escape
from einvoicing import db
from flask import render_template, request, redirect, url_for, flash
from einvoicing.student.models import Student
import pandas as pd
import matplotlib.pyplot as plt
import io

student = Blueprint('student', __name__)

@student.route("/create-student/", methods=['GET'])
def create_student():
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

    flash('Student saved successfully!', 'success')
    return redirect(url_for('student.list_student'))  # Replace with your listing route

@student.route("/delete-student/<id>", methods=["GET"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash(f'Student {student.name} has been deleted.', 'success')
    return redirect(url_for('student.list_student'))  # Replace with your actual listing route



@student.route("/list")
def list_student():
    # return "<p>Senarai student</p>"
    page = request.args.get('page', 1, type=int)
    per_page = 10
    paginated_students = Student.query.order_by(Student.id).paginate(page=page, per_page=per_page)
    return render_template('student/list.html', students=paginated_students)
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