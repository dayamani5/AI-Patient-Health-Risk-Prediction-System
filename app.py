from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient
from datetime import datetime, date
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "change-this-secret-key"

db.init_app(app)
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def generate_health_prediction(glucose, haemoglobin, cholesterol):
    remarks = []
    risk_points = 0

    # Glucose Analysis
    if glucose < 70:
        remarks.append("Low glucose detected. Possible hypoglycemia risk.")
        risk_points += 1
    elif glucose <= 140:
        remarks.append("Glucose is within normal range.")
    elif glucose <= 199:
        remarks.append("High glucose detected. Possible pre-diabetes risk.")
        risk_points += 1
    else:
        remarks.append("Very high glucose detected. Possible diabetes risk.")
        risk_points += 2

    # Haemoglobin Analysis
    if haemoglobin < 12:
        remarks.append("Low haemoglobin detected. Possible anaemia risk.")
        risk_points += 1
    elif haemoglobin <= 17.5:
        remarks.append("Haemoglobin is within normal range.")
    else:
        remarks.append("High haemoglobin detected. Medical consultation recommended.")
        risk_points += 1

    # Cholesterol Analysis
    if cholesterol < 200:
        remarks.append("Cholesterol is within desirable range.")
    elif cholesterol <= 239:
        remarks.append("Borderline high cholesterol detected. Lifestyle improvement recommended.")
        risk_points += 1
    else:
        remarks.append("High cholesterol detected. Possible cardiovascular risk.")
        risk_points += 2

    # Final Risk Level
    if risk_points >= 3:
        risk_level = "High"
    elif risk_points >= 1:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    # Timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Professional AI Remarks
    remarks_text = f"AI Prediction generated successfully on {timestamp}.\n\n"
    for remark in remarks:
        remarks_text += f"• {remark}\n"
    remarks_text += f"\nFinal AI Risk Classification: {risk_level} Risk."

   

    return risk_level, remarks_text


def validate_patient_data(form):
    errors=[]
    full_name=form.get('full_name','').strip(); dob=form.get('dob','').strip(); email=form.get('email','').strip()
    glucose=form.get('glucose','').strip(); haemoglobin=form.get('haemoglobin','').strip(); cholesterol=form.get('cholesterol','').strip()
    if not full_name: errors.append('Full name is required.')
    if not re.match(EMAIL_PATTERN,email): errors.append('Enter a valid email address.')
    try:
        dob_date=datetime.strptime(dob,'%Y-%m-%d').date()
        if dob_date > date.today(): errors.append('Date of birth cannot be a future date.')
    except ValueError: errors.append('Enter a valid date of birth.')
    nums={}
    for key,val in {'glucose':glucose,'haemoglobin':haemoglobin,'cholesterol':cholesterol}.items():
        try:
            nums[key]=float(val)
            if nums[key] < 0: errors.append(f'{key.title()} cannot be negative.')
        except ValueError: errors.append(f'{key.title()} must be numeric.')
    return errors, {'full_name':full_name,'dob':dob,'email':email,'glucose':nums.get('glucose'),'haemoglobin':nums.get('haemoglobin'),'cholesterol':nums.get('cholesterol')}

@app.route('/')
def index():
    search=request.args.get('search','').strip(); risk_filter=request.args.get('risk','').strip()
    query=Patient.query
    if search:
        query=query.filter((Patient.full_name.ilike(f'%{search}%')) | (Patient.email.ilike(f'%{search}%')))
    if risk_filter:
        query=query.filter(Patient.risk_level==risk_filter)
    patients=query.order_by(Patient.id.desc()).all()
    all_patients=Patient.query.all()
    return render_template('index.html', patients=patients, search=search, risk_filter=risk_filter,
        total_count=len(all_patients), low_count=len([p for p in all_patients if p.risk_level=='Low']),
        moderate_count=len([p for p in all_patients if p.risk_level=='Moderate']), high_count=len([p for p in all_patients if p.risk_level=='High']))

@app.route('/add', methods=['GET','POST'])
def add_patient():
    if request.method=='POST':
        errors,data=validate_patient_data(request.form)
        if errors:
            for e in errors: flash(e,'danger')
            return render_template('form.html', patient=request.form, action='Add')
        risk,remarks=generate_health_prediction(data['glucose'],data['haemoglobin'],data['cholesterol'])
        patient=Patient(**data, risk_level=risk, remarks=remarks)
        db.session.add(patient); db.session.commit(); flash('Patient record added successfully.','success')
        return redirect(url_for('index'))
    return render_template('form.html', patient=None, action='Add')

@app.route('/edit/<int:patient_id>', methods=['GET','POST'])
def edit_patient(patient_id):
    patient=Patient.query.get_or_404(patient_id)
    if request.method=='POST':
        errors,data=validate_patient_data(request.form)
        if errors:
            for e in errors: flash(e,'danger')
            return render_template('form.html', patient=request.form, action='Edit')
        risk,remarks=generate_health_prediction(data['glucose'],data['haemoglobin'],data['cholesterol'])
        for k,v in data.items(): setattr(patient,k,v)
        patient.risk_level=risk; patient.remarks=remarks
        db.session.commit(); flash('Patient record updated successfully.','success')
        return redirect(url_for('index'))
    return render_template('form.html', patient=patient, action='Edit')

@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient=Patient.query.get_or_404(patient_id)
    db.session.delete(patient); db.session.commit(); flash('Patient record deleted successfully.','success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)
