from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from app.services.sheets import write_to_google_sheet
from datetime import datetime
import os

main_routes = Blueprint("main_routes", __name__)

# ===============================
# 🔹 Home Page
# ===============================
@main_routes.route("/")
def home():
    return render_template("home.html", current_year=datetime.now().year)

# ===============================
# 🔹 Login Page
# ===============================
@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            session["user"] = email
            return redirect(url_for("main_routes.form"))
        else:
            return "Invalid login"

    return render_template("login.html", current_year=datetime.now().year)

# ===============================
# 🔹 Form Page (Inspection Form)
# ===============================
@main_routes.route("/form", methods=["GET", "POST"])
def form():
    if "user" not in session:
        return redirect(url_for("main_routes.login"))

    if request.method == "POST":
        name_input = request.form.get("name")
        comment = request.form.get("comment")
        photo = request.files.get("photo")

        if photo:
            filename = secure_filename(photo.filename)
            upload_folder = os.path.join("app", "static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            photo_path = os.path.join(upload_folder, filename)
            photo.save(photo_path)

            # 🔄 Google Sheet
            write_to_google_sheet({
                "name": name_input,
                "email": session.get("user"),
                "department": "Alpha Platforms",
                "comment": comment,
                "photo_url": url_for("static", filename="uploads/" + filename, _external=True)
            })

            return render_template("success.html", name=name_input, filename=filename, current_year=datetime.now().year)

    return render_template("form.html", current_year=datetime.now().year)

# ===============================
# 🔹 Logout
# ===============================
@main_routes.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main_routes.home"))
