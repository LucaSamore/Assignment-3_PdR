from os import path
from typing import Optional

class Router:
    _protected_routes: list = ['/pages/home.html', 
                               '/pages/service1.html', 
                               '/pages/service2.html', 
                               '/pages/service3.html']
    
    def handle_route(self, route: str) -> Optional[str]:
        if route == "/":
            return "/pages/index.html"
        return self.find_page(route)
    
    def find_page(self, pagePath: str) -> Optional[str]:
        
        return pagePath
        
        """
        if path.exists(pagePath):
            return pagePath
        return None
        """
    
    def is_protected(self, route: str) -> bool:
        return route in self._protected_routes