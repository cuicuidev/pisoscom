from . import app, data, model, about

ROUTES = {
    'App': app.app,
    'Datos': data.data,
    'Modelo': model.model,
    'Autores': about.about,
}