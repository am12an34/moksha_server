from rest_framework.renderers import JSONRenderer
from .cryptojs import encrypt
import environ
import json

env = environ.Env()
environ.Env.read_env()


class CryptoRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            # Get the response status code
            status_code = renderer_context.get('response').status_code if renderer_context and 'response' in renderer_context else 200

            # Process response

            # Render the JSON
            json_rendered = super().render(data, accepted_media_type, renderer_context)

            # Encrypt the response
            try:
                encrypted = encrypt(json_rendered, env('PAYLOAD_SECRET')).decode()
                return encrypted
            except Exception as e:
                # Encryption failed
                # If encryption fails, return plain JSON
                return json_rendered

        except Exception as e:
            # Renderer error occurred
            # If anything fails, return a simple JSON error
            return json.dumps({"error": "Error rendering response"}).encode()
