"""
Aplicación Flask Principal para la Calculadora con CI/CD, Render y ConfigCat Feature Toggles.
"""
from flask import Flask, jsonify, request, render_template
from calculator import Calculator
from configcat_service import feature_toggle_service

app = Flask(__name__)

@app.route("/")
def home():
    """Página principal con UI interactiva."""
    multiplicacion_on = feature_toggle_service.is_feature_enabled("multiplicacion_enabled", default_value=True)
    division_on = feature_toggle_service.is_feature_enabled("division_enabled", default_value=False)
    return render_template("index.html", 
                           multiplicacion_enabled=multiplicacion_on, 
                           division_enabled=division_on)

@app.route("/health")
def health_check():
    """Endpoint de comprobación de salud para Render / Deployment Pipelines."""
    return jsonify({
        "status": "healthy",
        "service": "calculadora-tbd-api",
        "version": "1.0.0",
        "environment": "production"
    }), 200

@app.route("/api/sumar", methods=["POST"])
def api_sumar():
    data = request.get_json() or {}
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    resultado = Calculator.sumar(a, b)
    return jsonify({"operacion": "suma", "a": a, "b": b, "resultado": resultado})

@app.route("/api/restar", methods=["POST"])
def api_restar():
    data = request.get_json() or {}
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    resultado = Calculator.restar(a, b)
    return jsonify({"operacion": "resta", "a": a, "b": b, "resultado": resultado})

@app.route("/api/multiplicar", methods=["POST"])
def api_multiplicar():
    """Endpoint de multiplicación protegido por Feature Toggle."""
    user_id = request.headers.get("X-User-ID", "anonymous")
    enabled = feature_toggle_service.is_feature_enabled("multiplicacion_enabled", default_value=True, user_id=user_id)
    
    if not enabled:
        return jsonify({
            "error": "FeatureDisabled",
            "message": "La funcionalidad de multiplicación está deshabilitada temporalmente vía Feature Toggle (ConfigCat)."
        }), 403

    data = request.get_json() or {}
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    resultado = Calculator.multiplicar(a, b)
    return jsonify({"operacion": "multiplicacion", "a": a, "b": b, "resultado": resultado})

@app.route("/api/dividir", methods=["POST"])
def api_dividir():
    """Endpoint de división protegido por Feature Toggle."""
    user_id = request.headers.get("X-User-ID", "anonymous")
    enabled = feature_toggle_service.is_feature_enabled("division_enabled", default_value=False, user_id=user_id)
    
    if not enabled:
        return jsonify({
            "error": "FeatureDisabled",
            "message": "La funcionalidad de división está en rollout progresivo o deshabilitada vía Feature Toggle (ConfigCat)."
        }), 403

    data = request.get_json() or {}
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    
    try:
        resultado = Calculator.dividir(a, b)
        return jsonify({"operacion": "division", "a": a, "b": b, "resultado": resultado})
    except ValueError as e:
        return jsonify({"error": "ValidationError", "message": str(e)}), 400

@app.route("/api/toggles", methods=["GET"])
def api_toggles():
    """Endpoint de diagnóstico para consultar el estado actual de los Feature Toggles."""
    user_id = request.args.get("user_id", "default_user")
    return jsonify({
        "multiplicacion_enabled": feature_toggle_service.is_feature_enabled("multiplicacion_enabled", True, user_id),
        "division_enabled": feature_toggle_service.is_feature_enabled("division_enabled", False, user_id)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
