from todolist.views.index import index

routes = [
    ('GET', '/', index, 'index'),
]


def register_routes(app):
    for method, path, view, name in routes:
        app.router.add_route(method, path, view, name=name)
