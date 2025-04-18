class AllowAnyHostMiddleware:
    """
    Middleware that allows any host header.
    This is useful for development environments where you might be using
    non-standard hostnames like 'AMAN_LAPTOP:8000'.
    
    WARNING: This should never be used in production as it bypasses
    Django's host validation, which is a security feature.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Store the original get_host method
        original_get_host = request.get_host
        
        # Define a new get_host method that doesn't validate the host
        def get_host_without_validation():
            host = request.META.get('HTTP_HOST', '')
            if not host:
                host = request.META.get('SERVER_NAME', '')
                port = request.META.get('SERVER_PORT', '')
                if port and port != '80' and port != '443':
                    host = f'{host}:{port}'
            return host
        
        # Replace the get_host method with our custom one
        request.get_host = get_host_without_validation
        
        # Process the request
        response = self.get_response(request)
        
        # Restore the original get_host method
        request.get_host = original_get_host
        
        return response
