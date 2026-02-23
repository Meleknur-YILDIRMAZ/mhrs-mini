from flask import Flask, request, jsonify, render_template
from db import init_db, get_conn

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

# -------- Patients --------
@app.post("/api/patients")
def create_patient():
    data = request.get_json(force=True)  # boş da gelse patlatmasın
    name = (data.get("name") or "").strip()
    tc = (data.get("tc") or "").strip()

    if not name or not tc:
        return jsonify({"error": "name ve tc zorunlu"}), 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO patients (name, tc) VALUES (?, ?)", (name, tc))
        conn.commit()
    except Exception as e:
        conn.close()
        # TC unique olduğu için aynı tc eklenirse buraya düşer
        return jsonify({"error": f"hasta eklenemedi: {str(e)}"}), 400

    patient_id = cur.lastrowid
    conn.close()

    return jsonify({"id": patient_id, "name": name, "tc": tc}), 201

@app.get("/api/patients")
def list_patients():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, tc FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# -------- Appointments --------
@app.post("/api/appointments")
def create_appointment():
    data = request.get_json(force=True)
    patient_tc = (data.get("patient_tc") or "").strip()
    doctor = (data.get("doctor") or "").strip()
    date = (data.get("date") or "").strip()   # YYYY-MM-DD
    time = (data.get("time") or "").strip()   # HH:MM

    if not patient_tc or not doctor or not date or not time:
        return jsonify({"error": "patient_tc, doctor, date, time zorunlu"}), 400

    conn = get_conn()
    cur = conn.cursor()

    # Hasta var mı?
    p = cur.execute("SELECT tc FROM patients WHERE tc = ?", (patient_tc,)).fetchone()
    if not p:
        conn.close()
        return jsonify({"error": "Bu tc ile hasta bulunamadı"}), 404

    cur.execute(
        "INSERT INTO appointments (patient_tc, doctor, date, time) VALUES (?, ?, ?, ?)",
        (patient_tc, doctor, date, time),
    )
    conn.commit()
    appt_id = cur.lastrowid
    conn.close()

    return jsonify({
        "id": appt_id,
        "patient_tc": patient_tc,
        "doctor": doctor,
        "date": date,
        "time": time
    }), 201

@app.get("/api/appointments")
def list_appointments():
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, patient_tc, doctor, date, time
        FROM appointments
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

def create_app():
    # testler için ayrı app instance üretmek istersek
    init_db()
    return app

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)