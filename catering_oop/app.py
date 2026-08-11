from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for
from database import CateringRepository, Database
from services import CateringService

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config.update(SECRET_KEY="oop-catering-development-key")
database = Database(BASE_DIR / "catering.db")
database.initialize()
repository = CateringRepository(database)
service = CateringService(repository)


def execute(action, success, endpoint):
    try:
        action()
        flash(success, "success")
    except (ValueError, KeyError, TypeError) as error:
        flash(str(error), "error")
    return redirect(url_for(endpoint))


@app.route("/")
def dashboard():
    return render_template("dashboard.html", stats=repository.dashboard(), orders=repository.all_orders()[:5])


@app.route("/menus", methods=["GET", "POST"])
def menus():
    if request.method == "POST":
        return execute(lambda: service.add_menu(request.form), "Menu berhasil ditambahkan.", "menus")
    return render_template("menus.html", menus=repository.all_menus())


@app.post("/menus/<int:menu_id>/delete")
def delete_menu(menu_id):
    return execute(lambda: repository.delete_menu(menu_id), "Menu berhasil dihapus.", "menus")


@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        return execute(lambda: service.add_customer(request.form), "Pelanggan berhasil disimpan.", "customers")
    return render_template("customers.html", customers=repository.all_customers())


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        return execute(lambda: service.create_order(request.form), "Pesanan berhasil dibuat.", "orders")
    return render_template("orders.html", orders=repository.all_orders(), customers=repository.all_customers(), menus=repository.all_menus())


@app.post("/orders/<int:order_id>/status")
def order_status(order_id):
    return execute(lambda: repository.update_status(order_id, request.form["status"]), "Status diperbarui.", "orders")


if __name__ == "__main__":
    app.run(debug=True)

