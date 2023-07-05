from django.urls import path
from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class Router(SimpleRouter):
    routes = [
        Route(
            url="{prefix}{trailing_slash}",
            mapping={
                "get": "list",
                "post": "create"
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        DynamicRoute(
            url="{prefix}/{url_path}{trailing_slash}",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={}
        ),
        Route(
            url="{prefix}/{lookup}{trailing_slash}",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy"
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"}
        ),
        DynamicRoute(
            url="{prefix}/{lookup}/{url_path}{trailing_slash}",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={}
        )
    ]

    def get_lookup_regex(self, view_set, lookup_prefix=''):
        return f"<{view_set.lookup_url_converter}:{view_set.lookup_url_kwarg}>"

    def get_urls(self):
        patterns = []

        for prefix, view_set, basename in self.registry:
            for route in self.get_routes(view_set):
                mapping = self.get_method_map(view_set, route.mapping)
                if not mapping:
                    continue

                format_kwargs = {
                    "prefix": prefix,
                    "trailing_slash": self.trailing_slash
                }

                if route.detail:
                    format_kwargs.update({"lookup": self.get_lookup_regex(view_set)})

                pattern = route.url.format(**format_kwargs)

                if not prefix and pattern[:1] == "/":
                    pattern = pattern[1:]

                kwargs = route.initkwargs.copy()
                kwargs.update({
                    "basename": basename,
                    "detail": route.detail,
                })

                view = view_set.as_view(mapping, **kwargs)
                name = route.name.format(basename=basename)
                patterns.append(path(pattern, view, name=name))

        return patterns
