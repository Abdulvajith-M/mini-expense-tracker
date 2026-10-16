from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "expense-tracker-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Other"]


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(250))



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "")
        date_text = request.form.get("expense_date", "")
        notes = request.form.get("notes", "").strip()

        if not title or len(title) > 100:
            flash("Title is required and must be under 100 characters.")
        elif not amount_text:
            flash("Amount is required.")
        else:
            try:
                amount = float(amount_text)
            except ValueError:
                amount = 0

            if amount <= 0:
                flash("Amount must be greater than zero.")
            elif category not in CATEGORIES:
                flash("Please select a valid category.")
            elif len(notes) > 250:
                flash("Notes must be under 250 characters.")
            else:
                try:
                    expense_date = date.fromisoformat(date_text)
                except ValueError:
                    expense_date = None

                if expense_date is None:
                    flash("Please enter a valid expense date.")
                elif expense_date > date.today():
                    flash("Expense date cannot be in the future.")
                else:
                    expense = Expense(
                        title=title,
                        amount=amount,
                        category=category,
                        expense_date=expense_date,
                        notes=notes or None
                    )
                    db.session.add(expense)
                    db.session.commit()

                    flash("Expense added successfully!")
                    return redirect(url_for("home"))

        return redirect(url_for("home"))

    selected_category = request.args.get("category", "All")

    if selected_category == "All":
        expenses = Expense.query.order_by(
            Expense.expense_date.desc()
        ).all()
    else:
        expenses = Expense.query.filter_by(
            category=selected_category
        ).order_by(Expense.expense_date.desc()).all()

    total_amount = sum(expense.amount for expense in expenses)

    return render_template(
        "index.html",
        today=date.today().isoformat(),
        expenses=expenses,
        total_amount=total_amount,
        categories=CATEGORIES,
        selected_category=selected_category
    )
    @app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
    def edit_expense(expense_id):
        expense = db.get_or_404(Expense, expense_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "")
        date_text = request.form.get("expense_date", "")
        notes = request.form.get("notes", "").strip()

        if not title or len(title) > 100:
            flash("Title is required and must be under 100 characters.")
        elif len(notes) > 250:
            flash("Notes must be under 250 characters.")
        elif category not in CATEGORIES:
            flash("Please select a valid category.")
        else:
            try:
                amount = float(amount_text)
                expense_date = date.fromisoformat(date_text)
            except (ValueError, TypeError):
                flash("Enter a valid amount and date.")
            else:
                if amount <= 0:
                    flash("Amount must be greater than zero.")
                elif expense_date > date.today():
                    flash("Expense date cannot be in the future.")
                else:
                    expense.title = title
                    expense.amount = amount
                    expense.category = category
                    expense.expense_date = expense_date
                    expense.notes = notes or None

                    db.session.commit()
                    flash("Expense updated successfully!")
                    return redirect(url_for("home"))

        return redirect(url_for("edit_expense", expense_id=expense.id))

    return render_template(
        "edit.html",
        expense=expense,
        categories=CATEGORIES,
        today=date.today().isoformat()
    )

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = db.get_or_404(Expense, expense_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "")
        date_text = request.form.get("expense_date", "")
        notes = request.form.get("notes", "").strip()

        if not title or len(title) > 100:
            flash("Title is required and must be under 100 characters.")
        elif len(notes) > 250:
            flash("Notes must be under 250 characters.")
        elif category not in CATEGORIES:
            flash("Please select a valid category.")
        else:
            try:
                amount = float(amount_text)
                expense_date = date.fromisoformat(date_text)
            except (ValueError, TypeError):
                flash("Enter a valid amount and date.")
            else:
                if amount <= 0:
                    flash("Amount must be greater than zero.")
                elif expense_date > date.today():
                    flash("Expense date cannot be in the future.")
                else:
                    expense.title = title
                    expense.amount = amount
                    expense.category = category
                    expense.expense_date = expense_date
                    expense.notes = notes or None

                    db.session.commit()
                    flash("Expense updated successfully!")
                    return redirect(url_for("home"))

        return redirect(url_for("edit_expense", expense_id=expense.id))

    return render_template(
        "edit.html",
        expense=expense,
        categories=CATEGORIES,
        today=date.today().isoformat()
    )
    
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = db.get_or_404(Expense, expense_id)

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully!")
    return redirect(url_for("home"))    
    
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
    