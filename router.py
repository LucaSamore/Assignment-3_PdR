class Router:
    _protected_routes: list[str] = ['/pages/home.html', 
                               '/pages/service1.html', 
                               '/pages/service2.html', 
                               '/pages/service3.html']
    
    def handle_route(self, route: str) -> str:
        if route == "/":
            return "/pages/index.html"
        return route
    
    def is_protected(self, route: str) -> bool:
        return route in self._protected_routes