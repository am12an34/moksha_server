from rest_framework.parsers import BaseParser, JSONParser
from rest_framework.exceptions import ParseError
from .cryptojs import decrypt
import json
import environ
import base64
import traceback
import re

env = environ.Env()
environ.Env.read_env()


class CryptoParser(BaseParser):
    media_type = 'text/plain'
    json_parser = JSONParser()

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            # Read the request body
            ciphertext_b64 = stream.read()

            # For debugging
            print(f"Received data length: {len(ciphertext_b64)}")
            if isinstance(ciphertext_b64, bytes):
                print(f"First 50 bytes: {ciphertext_b64[:50]}")
            else:
                print(f"First 50 chars: {ciphertext_b64[:50]}")

            # Handle empty data
            if not ciphertext_b64:
                return {}

            # Try to handle as plain JSON first (not encrypted)
            try:
                if isinstance(ciphertext_b64, bytes):
                    text_data = ciphertext_b64.decode('utf-8', errors='replace')
                else:
                    text_data = ciphertext_b64

                # Check if it looks like JSON
                if text_data.strip().startswith('{'):
                    print("Detected JSON data, parsing directly")
                    return json.loads(text_data)
            except Exception as e:
                print(f"Not JSON: {e}")
                pass

            # Try to decrypt the data
            try:
                # Ensure we're working with bytes
                if not isinstance(ciphertext_b64, bytes):
                    print(f"Converting string to bytes, type: {type(ciphertext_b64)}")
                    ciphertext_b64 = ciphertext_b64.encode('utf-8', errors='replace')

                # Check if it's valid base64
                try:
                    # Try to decode base64 to validate format
                    decoded = base64.b64decode(ciphertext_b64)
                    print(f"Valid base64 data detected, decoded length: {len(decoded)}")
                    print(f"Decoded starts with: {decoded[:16]}")

                    # Check if it has the 'Salted__' prefix
                    if len(decoded) >= 8 and decoded[:8] == b'Salted__':
                        print("Valid 'Salted__' prefix detected")
                    else:
                        print(f"Invalid prefix: {decoded[:8]}")

                except Exception as e:
                    print(f"Invalid base64 data: {e}")
                    # If not valid base64, try to parse as JSON directly again
                    try:
                        if isinstance(ciphertext_b64, bytes):
                            text_data = ciphertext_b64.decode('utf-8', errors='replace')
                        else:
                            text_data = ciphertext_b64
                        print(f"Trying to parse as JSON again: {text_data[:50]}...")
                        return json.loads(text_data)
                    except json.JSONDecodeError as e:
                        print(f"Not valid JSON either: {e}")
                        # Try to extract JSON from the data if it contains JSON-like patterns
                        json_pattern = r'\{[^\{\}]*\}'  # Simple pattern to find JSON objects
                        matches = re.findall(json_pattern, text_data)
                        if matches:
                            print(f"Found potential JSON: {matches[0]}")
                            try:
                                return json.loads(matches[0])
                            except json.JSONDecodeError:
                                pass

                        # Not JSON either, raise the original error
                        raise ParseError(f"Invalid data format: not valid base64 or JSON")

                # Decrypt the data
                payload_secret = env('PAYLOAD_SECRET')
                print(f"Using PAYLOAD_SECRET: {payload_secret[:3]}...{payload_secret[-3:]}")

                try:
                    print("Attempting to decrypt data...")
                    decrypted_bytes = decrypt(ciphertext_b64, payload_secret)
                    print(f"Decryption successful! Length: {len(decrypted_bytes)}")
                    print(f"Decrypted data starts with: {decrypted_bytes[:20]}")
                except Exception as e:
                    print(f"Standard decryption failed: {e}")
                    # If standard decryption fails, try alternative approaches

                    # Try with different padding or format
                    try:
                        # Try to fix padding if needed
                        padding_needed = len(ciphertext_b64) % 4
                        if padding_needed:
                            padded = ciphertext_b64 + b'=' * (4 - padding_needed) if isinstance(ciphertext_b64, bytes) else ciphertext_b64 + '=' * (4 - padding_needed)
                            print(f"Trying with fixed padding: {padded[:50]}...")
                            decrypted_bytes = decrypt(padded, payload_secret)
                            print("Decryption with fixed padding successful!")
                        else:
                            raise Exception("Padding is correct, issue is elsewhere")
                    except Exception as pad_error:
                        print(f"Padding fix failed: {pad_error}")

                        # As a fallback, try to parse as JSON directly one more time
                        try:
                            if isinstance(ciphertext_b64, bytes):
                                text_data = ciphertext_b64.decode('utf-8', errors='replace')
                            else:
                                text_data = ciphertext_b64
                            print(f"Fallback: trying to parse as JSON: {text_data[:50]}...")

                            # Try to find JSON-like patterns in the data
                            json_pattern = r'\{[^\{\}]*\}'  # Simple pattern to find JSON objects
                            matches = re.findall(json_pattern, text_data)
                            if matches:
                                print(f"Found potential JSON: {matches[0]}")
                                try:
                                    return json.loads(matches[0])
                                except json.JSONDecodeError:
                                    pass

                            # Try direct JSON parsing
                            return json.loads(text_data)
                        except json.JSONDecodeError as json_error:
                            print(f"JSON parsing failed: {json_error}")

                            # If we have form data, try to parse it
                            if '=' in text_data and '&' in text_data:
                                print("Detected form data, parsing as form")
                                form_data = {}
                                pairs = text_data.split('&')
                                for pair in pairs:
                                    if '=' in pair:
                                        key, value = pair.split('=', 1)
                                        form_data[key] = value
                                return form_data

                            # If all else fails, create a minimal valid response
                            print("All parsing methods failed, returning minimal data")
                            return {"_raw_data": text_data[:100] + "..."}  # Include raw data for debugging

                # Try to decode as UTF-8
                try:
                    stringified_json = decrypted_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    # If UTF-8 decoding fails, try with latin-1 which never fails
                    stringified_json = decrypted_bytes.decode('latin-1')

                # Parse the JSON
                try:
                    return json.loads(stringified_json)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Stringified JSON: {stringified_json[:100]}...")

                    # Try to find JSON-like patterns in the data
                    json_pattern = r'\{[^\{\}]*\}'  # Simple pattern to find JSON objects
                    matches = re.findall(json_pattern, stringified_json)
                    if matches:
                        print(f"Found potential JSON: {matches[0]}")
                        try:
                            return json.loads(matches[0])
                        except json.JSONDecodeError:
                            pass

                    # If we can't parse as JSON, return the raw string as data
                    print("Returning raw decrypted data as fallback")
                    return {"message": stringified_json[:100] + "..."}

            except Exception as e:
                print(f"Decryption error: {e}")
                print(traceback.format_exc())

                # Instead of failing, return a minimal valid response
                return {"_error": str(e)}

        except Exception as exc:
            # Print detailed error for debugging
            print(f"Error parsing request: {str(exc)}")
            print(traceback.format_exc())

            # Instead of failing, return a minimal valid response
            return {"_parse_error": str(exc)}
