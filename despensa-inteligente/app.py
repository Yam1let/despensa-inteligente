"""Despensa Inteligente - RY Software (Ibero León, DASV)
I1 v0.1.0 Acceso a cuentas | I2 v0.2.0 Inventario | I3 v0.3.0 Alertas y compras
Ejecutar: pip install -r requirements.txt && python app.py  ->  http://127.0.0.1:5000
"""
import os, re, sqlite3, threading, webbrowser
from html import escape
from datetime import date
from functools import wraps
from flask import (Flask, g, request, session, redirect, url_for, flash,
                   render_template, abort)
from jinja2 import DictLoader
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "despensa.db")
INTERFAZ = os.path.join(BASE, "static", "despensa.html")
DIAS_AVISO = 7
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

# ---------- Base de datos (SQLite + WAL) ----------
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def cerrar(_):
    c = g.pop("db", None)
    if c:
        c.close()

def init_db():
    with sqlite3.connect(DB) as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY, correo TEXT UNIQUE NOT NULL, hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            nombre TEXT NOT NULL, categoria TEXT NOT NULL DEFAULT 'General',
            cantidad REAL NOT NULL DEFAULT 1, unidad TEXT NOT NULL DEFAULT 'pzas',
            minimo REAL NOT NULL DEFAULT 1, caducidad TEXT);
        CREATE TABLE IF NOT EXISTS compras(
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            nombre TEXT NOT NULL, cantidad REAL NOT NULL DEFAULT 1,
            comprado INTEGER NOT NULL DEFAULT 0);
        """)

# ---------- I1: validación y sesiones ----------
CORREO_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def normalizar_correo(c):
    return (c or "").strip().lower()

def validar(correo, pw):
    errores = []
    if not CORREO_RE.match(correo):
        errores.append("Correo no válido.")
    if not (8 <= len(pw or "") <= 64):
        errores.append("La contraseña debe tener de 8 a 64 caracteres.")
    return errores

def login_required(f):
    @wraps(f)
    def w(*a, **k):
        if "uid" not in session:
            return redirect(url_for("login"))
        return f(*a, **k)
    return w

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        correo = normalizar_correo(request.form.get("correo"))
        pw = request.form.get("password", "")
        errs = validar(correo, pw)
        if not errs:
            try:
                db().execute("INSERT INTO usuarios(correo,hash) VALUES(?,?)",
                             (correo, generate_password_hash(pw)))
                db().commit()
                flash("Cuenta creada. Inicia sesión.", "ok")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                errs.append("Ese correo ya está registrado.")
        for e in errs:
            flash(e, "error")
    return render_template("auth.html", titulo="Crear cuenta", boton="Registrarme")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = normalizar_correo(request.form.get("correo"))
        u = db().execute("SELECT * FROM usuarios WHERE correo=?", (correo,)).fetchone()
        if u and check_password_hash(u["hash"], request.form.get("password", "")):
            session.clear()
            session["uid"], session["correo"] = u["id"], u["correo"]
            return redirect(url_for("despensa"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("auth.html", titulo="Iniciar sesión", boton="Entrar")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- I2: inventario (siempre filtrado por usuario) ----------
def estado(cad):
    if not cad:
        return "sin fecha", None
    dias = (date.fromisoformat(cad) - date.today()).days
    if dias < 0:
        return "vencido", dias
    if dias <= DIAS_AVISO:
        return "por vencer", dias
    return "ok", dias

def leer_form():
    f = request.form
    nombre = f.get("nombre", "").strip()
    try:
        cant, minimo = float(f.get("cantidad", 0)), float(f.get("minimo", 0))
        if cant < 0 or minimo < 0:
            raise ValueError
    except ValueError:
        return None, "Cantidad y mínimo deben ser números mayores o iguales a 0."
    cad = f.get("caducidad") or None
    if cad:
        try:
            date.fromisoformat(cad)
        except ValueError:
            return None, "Fecha de caducidad no válida."
    if not nombre:
        return None, "El nombre es obligatorio."
    return (nombre, f.get("categoria", "").strip() or "General", cant,
            f.get("unidad", "").strip() or "pzas", minimo, cad), None

def mio(pid):
    p = db().execute("SELECT * FROM productos WHERE id=? AND usuario_id=?",
                     (pid, session["uid"])).fetchone()
    if not p:
        abort(404)
    return p

# ---------- Interfaz principal (Despensa Inteligente) ----------
@app.route("/")
@login_required
def despensa():
    """Sirve la interfaz; los datos se guardan en el navegador, separados por usuario."""
    with open(INTERFAZ, encoding="utf-8") as f:
        html = f.read()
    html = (html.replace("{{USUARIO}}", str(session["uid"]))
                .replace("{{CORREO}}", escape(session["correo"])))
    return html

@app.route("/inventario")
@login_required
def inventario():
    q = request.args.get("q", "").strip()
    cat = request.args.get("categoria", "").strip()
    sql, args = "SELECT * FROM productos WHERE usuario_id=?", [session["uid"]]
    if q:
        sql += " AND nombre LIKE ?"; args.append(f"%{q}%")
    if cat:
        sql += " AND categoria=?"; args.append(cat)
    filas = db().execute(sql + " ORDER BY nombre", args).fetchall()
    cats = [r[0] for r in db().execute(
        "SELECT DISTINCT categoria FROM productos WHERE usuario_id=? ORDER BY 1",
        (session["uid"],))]
    prods = [dict(r, est=estado(r["caducidad"])) for r in filas]
    return render_template("inventario.html", prods=prods, cats=cats, q=q, cat=cat)

@app.route("/producto/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        datos, err = leer_form()
        if err:
            flash(err, "error")
        else:
            db().execute("INSERT INTO productos(usuario_id,nombre,categoria,cantidad,"
                         "unidad,minimo,caducidad) VALUES(?,?,?,?,?,?,?)",
                         (session["uid"], *datos))
            db().commit()
            flash("Producto agregado.", "ok")
            return redirect(url_for("inventario"))
    return render_template("form.html", p=request.form, titulo="Nuevo producto")

@app.route("/producto/<int:pid>/editar", methods=["GET", "POST"])
@login_required
def editar(pid):
    p = mio(pid)
    if request.method == "POST":
        datos, err = leer_form()
        if err:
            flash(err, "error")
        else:
            db().execute("UPDATE productos SET nombre=?,categoria=?,cantidad=?,unidad=?,"
                         "minimo=?,caducidad=? WHERE id=? AND usuario_id=?",
                         (*datos, pid, session["uid"]))
            db().commit()
            flash("Producto actualizado.", "ok")
            return redirect(url_for("inventario"))
        p = request.form
    return render_template("form.html", p=p, titulo="Editar producto")

@app.route("/producto/<int:pid>/eliminar", methods=["POST"])
@login_required
def eliminar(pid):
    mio(pid)
    db().execute("DELETE FROM productos WHERE id=? AND usuario_id=?", (pid, session["uid"]))
    db().commit()
    flash("Producto eliminado.", "ok")
    return redirect(url_for("inventario"))

# ---------- I3: alertas, sugerencias y compras ----------
@app.route("/alertas")
@login_required
def alertas():
    prods = [dict(r, est=estado(r["caducidad"])) for r in db().execute(
        "SELECT * FROM productos WHERE usuario_id=? AND cantidad>0", (session["uid"],))]
    vencidos = [p for p in prods if p["est"][0] == "vencido"]
    por_vencer = sorted((p for p in prods if p["est"][0] == "por vencer"),
                        key=lambda p: p["est"][1])
    bajos = [dict(r) for r in db().execute(
        "SELECT * FROM productos WHERE usuario_id=? AND cantidad<=minimo ORDER BY nombre",
        (session["uid"],))]
    return render_template("alertas.html", vencidos=vencidos, por_vencer=por_vencer,
                           bajos=bajos, dias=DIAS_AVISO)

@app.route("/compras", methods=["GET", "POST"])
@login_required
def compras():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            cant = float(request.form.get("cantidad", 1))
        except ValueError:
            cant = 0
        if nombre and cant > 0:
            db().execute("INSERT INTO compras(usuario_id,nombre,cantidad) VALUES(?,?,?)",
                         (session["uid"], nombre, cant))
            db().commit()
        else:
            flash("Escribe un nombre y una cantidad mayor a 0.", "error")
        return redirect(url_for("compras"))
    lista = db().execute("SELECT * FROM compras WHERE usuario_id=? ORDER BY comprado,nombre",
                         (session["uid"],)).fetchall()
    return render_template("compras.html", lista=lista)

@app.route("/compras/generar", methods=["POST"])
@login_required
def generar():
    u = session["uid"]
    pendientes = {r[0].lower() for r in db().execute(
        "SELECT nombre FROM compras WHERE usuario_id=? AND comprado=0", (u,))}
    n = 0
    for p in db().execute("SELECT * FROM productos WHERE usuario_id=? AND cantidad<=minimo", (u,)):
        if p["nombre"].lower() in pendientes:
            continue
        db().execute("INSERT INTO compras(usuario_id,nombre,cantidad) VALUES(?,?,?)",
                     (u, p["nombre"], max(p["minimo"] * 2 - p["cantidad"], 1)))
        n += 1
    db().commit()
    flash(f"Se agregaron {n} producto(s) con existencia baja.", "ok")
    return redirect(url_for("compras"))

@app.route("/compras/<int:cid>/<accion>", methods=["POST"])
@login_required
def compra_accion(cid, accion):
    u = session["uid"]
    if accion == "toggle":
        db().execute("UPDATE compras SET comprado=1-comprado WHERE id=? AND usuario_id=?", (cid, u))
    elif accion == "borrar":
        db().execute("DELETE FROM compras WHERE id=? AND usuario_id=?", (cid, u))
    else:
        abort(404)
    db().commit()
    return redirect(url_for("compras"))

# ---------- Plantillas ----------
def fmt(n):
    return int(n) if float(n).is_integer() else n
app.jinja_env.filters["n"] = fmt

T = {}
T["base.html"] = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Despensa Inteligente</title>
<style>
:root{--bg:#f6f5f0;--c:#fff;--t:#1f2a24;--m:#6b756e;--p:#2f7d4f;--b:#e2e0d6;--r:#c0392b;--a:#b9770e}
@media(prefers-color-scheme:dark){:root{--bg:#161a17;--c:#202621;--t:#e8ece9;--m:#9aa59d;--p:#5bbf84;--b:#323a34;--r:#ec7063;--a:#e5a54a}}
*{box-sizing:border-box}body{margin:0;font:16px system-ui,sans-serif;background:var(--bg);color:var(--t)}
nav{display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:12px 16px;background:var(--c);border-bottom:1px solid var(--b)}
nav b{margin-right:auto}nav a{color:var(--t);text-decoration:none;padding:6px 10px;border-radius:8px}nav a:hover{background:var(--bg)}
main{max-width:900px;margin:0 auto;padding:20px 16px}h1{margin-top:0}
.card{background:var(--c);border:1px solid var(--b);border-radius:12px;padding:16px;margin-bottom:16px}
input,select{padding:9px;border:1px solid var(--b);border-radius:8px;background:var(--bg);color:var(--t);font:inherit;width:100%}
label{display:block;font-size:14px;color:var(--m);margin:10px 0 4px}
.btn{background:var(--p);color:#fff;border:0;border-radius:8px;padding:9px 14px;font:inherit;cursor:pointer;text-decoration:none;display:inline-block}
.btn.s{background:transparent;color:var(--t);border:1px solid var(--b)}.btn.d{background:var(--r)}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:end}.row>*{flex:1;min-width:120px}.row>.btn{flex:0}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:9px 6px;border-bottom:1px solid var(--b);font-size:15px}
.tag{font-size:12px;padding:2px 8px;border-radius:99px;border:1px solid currentColor}
.vencido{color:var(--r)}.por{color:var(--a)}.ok{color:var(--p)}.sin{color:var(--m)}
.msg{padding:10px 14px;border-radius:8px;margin-bottom:12px}.msg.ok{background:#2f7d4f22}.msg.error{background:#c0392b22;color:var(--r)}
.tabla{overflow-x:auto}form.i{display:inline}.m{color:var(--m)}.tachado{text-decoration:line-through;color:var(--m)}
</style></head><body>
<nav><b>🥫 Despensa Inteligente</b>
{% if session.uid %}<a href="{{url_for('despensa')}}">Despensa</a><a href="{{url_for('inventario')}}">Inventario</a><a href="{{url_for('alertas')}}">Alertas</a>
<a href="{{url_for('compras')}}">Compras</a><a href="{{url_for('logout')}}">Salir ({{session.correo}})</a>
{% else %}<a href="{{url_for('login')}}">Entrar</a><a href="{{url_for('registro')}}">Registro</a>{% endif %}</nav>
<main>{% for c,m in get_flashed_messages(with_categories=true) %}<div class="msg {{c}}">{{m}}</div>{% endfor %}
{% block c %}{% endblock %}</main></body></html>"""

T["auth.html"] = """{% extends 'base.html' %}{% block c %}
<div class="card" style="max-width:380px;margin:30px auto"><h1>{{titulo}}</h1>
<form method="post"><label>Correo</label><input name="correo" type="email" required autofocus>
<label>Contraseña (8 a 64 caracteres)</label><input name="password" type="password" required minlength="8" maxlength="64">
<p><button class="btn">{{boton}}</button></p></form></div>{% endblock %}"""

T["inventario.html"] = """{% extends 'base.html' %}{% block c %}
<h1>Inventario</h1>
<form class="card row" method="get"><div><label>Buscar por nombre</label><input name="q" value="{{q}}"></div>
<div><label>Categoría</label><select name="categoria"><option value="">Todas</option>
{% for c in cats %}<option {{'selected' if c==cat}}>{{c}}</option>{% endfor %}</select></div>
<button class="btn s">Filtrar</button><a class="btn" href="{{url_for('nuevo')}}">+ Producto</a></form>
<div class="card tabla">{% if prods %}<table><tr><th>Producto</th><th>Categoría</th><th>Cantidad</th><th>Caducidad</th><th></th></tr>
{% for p in prods %}<tr><td>{{p.nombre}}</td><td>{{p.categoria}}</td>
<td>{{p.cantidad|n}} {{p.unidad}}{% if p.cantidad<=p.minimo %} <span class="tag vencido">bajo</span>{% endif %}</td>
<td>{% set e=p.est %}{% if e[0]=='vencido' %}<span class="tag vencido">vencido</span>
{% elif e[0]=='por vencer' %}<span class="tag por">{{e[1]}} d</span>
{% elif e[0]=='ok' %}<span class="tag ok">{{p.caducidad}}</span>{% else %}<span class="m">—</span>{% endif %}</td>
<td><a class="btn s" href="{{url_for('editar',pid=p.id)}}">Editar</a>
<form class="i" method="post" action="{{url_for('eliminar',pid=p.id)}}" onsubmit="return confirm('¿Eliminar {{p.nombre|e}}?')">
<button class="btn d">✕</button></form></td></tr>{% endfor %}</table>
{% else %}<p class="m">No hay productos. Agrega el primero.</p>{% endif %}</div>{% endblock %}"""

T["form.html"] = """{% extends 'base.html' %}{% block c %}<h1>{{titulo}}</h1>
<form class="card" method="post"><label>Nombre</label><input name="nombre" value="{{p['nombre']}}" required>
<div class="row"><div><label>Categoría</label><input name="categoria" value="{{p['categoria'] or 'General'}}"></div>
<div><label>Unidad</label><input name="unidad" value="{{p['unidad'] or 'pzas'}}"></div></div>
<div class="row"><div><label>Cantidad</label><input name="cantidad" type="number" step="any" min="0" value="{{p['cantidad'] if p['cantidad'] is not none else 1}}"></div>
<div><label>Mínimo (alerta)</label><input name="minimo" type="number" step="any" min="0" value="{{p['minimo'] if p['minimo'] is not none else 1}}"></div>
<div><label>Caducidad</label><input name="caducidad" type="date" value="{{p['caducidad'] or ''}}"></div></div>
<p><button class="btn">Guardar</button> <a class="btn s" href="{{url_for('inventario')}}">Cancelar</a></p></form>{% endblock %}"""

T["alertas.html"] = """{% extends 'base.html' %}{% block c %}<h1>Alertas y sugerencias</h1>
{% macro lista(items, vacio) %}{% if items %}<ul>{% for p in items %}<li><b>{{p.nombre}}</b> — {{p.cantidad|n}} {{p.unidad}}
{% if p.est and p.est[1] is not none %}<span class="m">({{ 'venció hace ' ~ (-p.est[1]) ~ ' d' if p.est[1]<0 else 'caduca en ' ~ p.est[1] ~ ' d' }})</span>{% endif %}</li>{% endfor %}</ul>
{% else %}<p class="m">{{vacio}}</p>{% endif %}{% endmacro %}
<div class="card"><h3 class="vencido">Vencidos</h3>{{lista(vencidos,'Nada vencido 🎉')}}</div>
<div class="card"><h3 class="por">Por vencer (próximos {{dias}} días)</h3>{{lista(por_vencer,'Nada por vencer pronto.')}}
{% if por_vencer %}<p class="m">💡 Sugerencia de consumo: usa primero lo que caduca antes (orden de la lista).</p>{% endif %}</div>
<div class="card"><h3>Existencia baja</h3>{{lista(bajos,'Todo en orden.')}}
{% if bajos %}<form method="post" action="{{url_for('generar')}}"><button class="btn">Generar lista de compras</button></form>{% endif %}</div>{% endblock %}"""

T["compras.html"] = """{% extends 'base.html' %}{% block c %}<h1>Lista de compras</h1>
<form class="card row" method="post"><div><label>Producto</label><input name="nombre" required></div>
<div><label>Cantidad</label><input name="cantidad" type="number" step="any" min="0.01" value="1"></div>
<button class="btn">Agregar</button></form>
<form method="post" action="{{url_for('generar')}}" style="margin-bottom:16px"><button class="btn s">⚡ Generar desde existencias bajas</button></form>
<div class="card">{% if lista %}<table>{% for c in lista %}<tr><td class="{{'tachado' if c.comprado}}">{{c.nombre}} × {{c.cantidad|n}}</td>
<td style="text-align:right"><form class="i" method="post" action="{{url_for('compra_accion',cid=c.id,accion='toggle')}}"><button class="btn s">{{'Deshacer' if c.comprado else '✓ Comprado'}}</button></form>
<form class="i" method="post" action="{{url_for('compra_accion',cid=c.id,accion='borrar')}}"><button class="btn d">✕</button></form></td></tr>{% endfor %}</table>
{% else %}<p class="m">La lista está vacía.</p>{% endif %}</div>{% endblock %}"""

app.jinja_loader = DictLoader(T)

init_db()
if __name__ == "__main__":
    URL = "http://127.0.0.1:5000"
    # Abre el navegador una sola vez (el recargador de Flask arranca el proceso dos veces)
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.5, lambda: webbrowser.open(URL)).start()
    app.run(host="127.0.0.1", port=5000, debug=True)
