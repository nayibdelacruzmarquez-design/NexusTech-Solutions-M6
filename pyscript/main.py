import asyncio
import json
import js
from js import fetch
from pyodide.ffi import create_proxy

async def fetch_remote_data_async():
    """Lógica asíncrona que consume la API REST y dibuja en el DOM."""
    status_el = js.document.getElementById("status-msg")
    table_body_el = js.document.getElementById("inventory-table-body")

    status_el.innerText = "⏳ Ejecutando petición HTTP asíncrona desde Python (PyScript)..."

    try:
        response = await fetch("https://fakestoreapi.com/products?limit=5")
        json_data = await response.json()

        products = json.loads(js.JSON.stringify(json_data))

        html_rows = ""
        for item in products:
            html_rows += f"""
            <tr class="hover:bg-slate-700/50 transition-colors">
                <td class="p-3 font-mono text-indigo-400">#{item.get('id')}</td>
                <td class="p-3 font-medium text-slate-200">{str(item.get('title'))[:30]}...</td>
                <td class="p-3"><span class="bg-slate-700 px-2 py-1 rounded text-xs">{item.get('category')}</span></td>
                <td class="p-3 font-semibold text-emerald-400">${item.get('price'):.2f}</td>
            </tr>
            """

        table_body_el.innerHTML = html_rows
        status_el.innerText = "✅ ¡Datos obtenidos asíncronamente y renderizados en el DOM por Python!"

    except Exception as err:
        status_el.innerText = f"❌ Error al consultar la API: {str(err)}"

def on_fetch_click(event):
    """Callback para el evento de clic que agenda la corrutina en el loop de asyncio."""
    asyncio.ensure_future(fetch_remote_data_async())

def clear_dashboard(event=None):
    """Limpia el DOM."""
    js.document.getElementById("inventory-table-body").innerHTML = (
        '<tr><td colspan="4" class="p-4 text-center text-slate-500">Sin datos cargados. Haz clic en el botón superior.</td></tr>'
    )
    js.document.getElementById("status-msg").innerText = "Dashboard reiniciado."

# Vinculación explícita de Event Listeners del DOM con Python
btn_fetch = js.document.getElementById("btn-fetch")
btn_clear = js.document.getElementById("btn-clear")

if btn_fetch:
    btn_fetch.addEventListener("click", create_proxy(on_fetch_click))

if btn_clear:
    btn_clear.addEventListener("click", create_proxy(clear_dashboard))