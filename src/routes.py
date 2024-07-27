import textwrap
from flask import redirect, render_template, request, url_for, current_app as app
from .models import Book
from . import db

contents = []
students = []


@app.template_filter("line_clamp")
def line_clamp(text, max_lines, width):
    return "\n".join(textwrap.wrap(text, width)[:max_lines]) + (
        "..." if len(textwrap.wrap(text, width)) > max_lines else ""
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content is not None:
            contents.append(content)
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        contents=contents,
    )


@app.route("/diary", methods=["GET", "POST"])
def diary():
    if request.method == "POST":
        name = request.form.get("name")
        grade = request.form.get("grade")
        if name is not None and grade is not None:
            students.append({"name": name, "grade": grade})
            return redirect(url_for("diary"))

    return render_template("diary.html", students=students)


@app.route("/books")
def books():
    page = request.args.get("page", 1, type=int)
    per_page = 2
    return render_template(
        "books.html", books=Book.query.paginate(page=page, per_page=per_page)
    )


@app.route("/new_book", methods=["GET", "POST"])
def new_book():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        if name is not None and description is not None and price is not None:
            book = Book(name, description, price)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for("books"))

    return render_template("new_book.html")


@app.route("/books/<int:id>/update", methods=["GET", "POST"])
def update_book(id):
    book = Book.query.filter_by(id=id)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        if name is not None and description is not None and price is not None:
            book.update({"name": name, "description": description, "price": price})
            db.session.commit()
            return redirect(url_for("books"))

    return render_template("update_book.html", book=book.first())


@app.route("/books/<int:id>/delete")
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("books"))
