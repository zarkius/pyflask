from flask import Flask

app = Flask(__name__)

# Generador que produce una secuencia de saludos
def generador_saludos():
    saludos = ["Hola, Mundo!", "Bonjour, le Monde!", "Hallo, Welt!", "Ciao, Mondo!", "Olá, Mundo!"]
    for saludo in saludos:
        yield saludo

# Generador que produce una secuencia de errores
def generador_errores():
    errores = ["Error 404: Página no encontrada", "Error 500: Error interno del servidor"]
    for error in errores:
        yield error

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/saludos")
def mostrar_saludos():
    return "<br>".join(generador_saludos())

@app.route("/errores")
def mostrar_errores():
    return "<br>".join(generador_errores())

@app.route("/rutas")
def mostrar_rutas():
    rutas = []
    for rule in app.url_map.iter_rules():
        rutas.append(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
    return "<br>".join(rutas)

if __name__ == "__main__":
    app.run()