from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from app.services.sheets import write_to_google_sheet
from datetime import datetime

main_routes = Blueprint('main_routes', __name__)  # 🟢 Оце має бути перед усіма @main_routes.route

@main_routes.route("/")
def home():
    return render_template("home.html")


@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email and password:
            session["user"] = email
            return redirect(url_for("main_routes.form"))
        return "Invalid login"
    return render_template("login.html")


@main_routes.route("/form", methods=["GET", "POST"])
def form():
    if "user" not in session:
        return redirect(url_for("main_routes.login"))

    if request.method == "POST":
        name_input = request.form["name"]
        comment = request.form["comment"]
        photo = request.files["photo"]

        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join("app/static/uploads", filename)
            os.makedirs(os.path.dirname(photo_path), exist_ok=True)
            photo.save(photo_path)

            write_to_google_sheet({
                "name": name_input,
                "email": session.get("user"),
                "department": "Alpha Platforms",
                "comment": comment,
                "photo_url": url_for("static", filename="uploads/" + filename, _external=True)
            })

            return render_template("success.html", name=name_input, filename=filename)

    return render_template("form.html")
