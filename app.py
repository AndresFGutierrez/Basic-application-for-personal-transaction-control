# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        # Crear un nuevo objeto de transacción usando los valores del campo del formulario
        transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"]),
        }
        # Agregar la nueva transacción a la lista
        transactions.append(transaction)
        # Redirigir a la página de lista de transacciones
        return redirect(url_for("get_transactions"))
    # Renderizar la plantilla de formulario para mostrar el formulario de agregar transacción
    return render_template("form.html")


# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        # Extraer los valores actualizados de los campos del formulario.
        date = request.form["date"]
        amount = float(request.form["amount"])

        # Encuentre la transacción con el ID coincidente y actualice sus valores
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                break

        # Redirigir a la página de lista de transacciones
        return redirect(url_for("get_transactions"))
    # Busque la transacción con el ID coincidente y presente el formulario de edición
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)


# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Encuentre la transacción con el ID coincidente y eliminela de la lista
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break
    # Redirigir a la página de lista de transacciones
    return redirect(url_for("get_transactions"))


# Buscar en un rango
@app.route("/search", methods=["POST", "GET"])
def search_transactions():
    if request.method == "POST":
        # Extraer los valores de los campos del formulario.
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])

        # Filtrar las transacciones según el rango de monto especificado.
        filtered_transactions = [
            transaction
            for transaction in transactions
            if min_amount <= transaction["amount"] <= max_amount
        ]

        # Pasar las transacciones filtradas y el saldo total a la plantilla.
        return render_template("transactions.html", transactions=filtered_transactions, total_balance=total_balance())

    # Si el método de solicitud es GET, renderizar la plantilla de búsqueda.
    return render_template("search.html")


# Saldo total
@app.route("/balance")
def total_balance():
    total = sum(transaction["amount"] for transaction in transactions)
    return f"Saldo total: {total}"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
