import sqlite3
import pickle
from flask import Flask, render_template, request, redirect, url_for, session,flash

# Initialize Flask app
app = Flask(__name__,static_url_path='/static')
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Load the trained model
with open("catboost_model.pkl", "rb") as file:
    model = pickle.load(file)
def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age REAL,
        sex REAL,
        chest_pain REAL,
        blood_pressure REAL,
        cholesterol REAL,
        fasting_sugar REAL,
        rest_ecg REAL,
        max_heart_rate REAL,
        exercise_angina REAL,
        st_depression REAL,
        slope REAL,
        prediction TEXT
    )
    """)

    conn.commit()
    conn.close()

# Dummy user data for authentication
users = {
    "admin": "123456",  # username: password
    "user1": "mypassword"
}

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password','error')
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/index")
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    elif request.method == "POST":
        # Extract form data and make predictions
        # Placeholder for prediction logic
        try:
            features = [
                float(request.form.get("age")),
                float(request.form.get("sex")),
                float(request.form.get("chest_pain")),
                float(request.form.get("blood_pressure")),
                float(request.form.get("cholesterol")),
                float(request.form.get("fasting_sugar")),
                float(request.form.get("rest_ecg")),
                float(request.form.get("max_heart_rate")),
                float(request.form.get("exercise_angina")),
                float(request.form.get("st_depression")),
                float(request.form.get("slope")),
            ]

            # Perform prediction
            prediction = model.predict([features])
            # Translate prediction (example: 0 = No Disease, 1 = Disease)
            result = "No Heart Disease Detected" if prediction == 0 else "Possible Heart Disease"
            # Save to database
            conn = sqlite3.connect("patients.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO patients (
            name,age, sex, chest_pain, blood_pressure, cholesterol,
            fasting_sugar, rest_ecg, max_heart_rate, exercise_angina,
            st_depression, slope, prediction
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
            request.form.get("name"),features[0], features[1], features[2], features[3], features[4],
            features[5], features[6], features[7], features[8],
            features[9], features[10], result
            ))

            conn.commit()
            conn.close()
        except Exception as e:
            result = f"Error in prediction: {e}"

        # return render_template("form.html", prediction=result, form_data=request.form)
        return render_template("result.html", prediction=result)

if __name__ == "__main__":
    init_db()
    app.run(debug=False)
