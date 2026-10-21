from flask import Blueprint, jsonify, request

tools_bp = Blueprint("tools", __name__, url_prefix="/api/tools")


@tools_bp.post("/emi")
def emi():
    data = request.get_json() or {}
    principal = float(data["principal"])
    monthly_rate = float(data["annual_rate"]) / 1200
    months = int(data["months"])

    if monthly_rate == 0:
        monthly_emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        monthly_emi = principal * monthly_rate * factor / (factor - 1)

    total_payment = monthly_emi * months

    return jsonify(
        monthly_emi=round(monthly_emi, 2),
        total_payment=round(total_payment, 2),
        total_interest=round(total_payment - principal, 2),
    )


@tools_bp.post("/currency")
def currency():
    data = request.get_json() or {}
    converted = float(data["amount"]) * float(data["rate"])
    return jsonify(converted_amount=round(converted, 2))
