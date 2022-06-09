from typing import Optional
from os import path

class Router:
    _protected_routes: list = ['/pages/home.html', 
                               '/pages/service1.html', 
                               '/pages/service2.html', 
                               '/pages/service3.html']
    
    def handle_route(self, route: str) -> Optional[str]:
        if route == "/":
            return "/pages/index.html"
        if path.exists(route):
            return route
        return None
    
    def is_protected(self, route: str) -> bool:
        return route in self._protected_routes