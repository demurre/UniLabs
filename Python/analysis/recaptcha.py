import webbrowser
import os
from typing import Tuple
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    requests = None

load_dotenv()



class GoogleReCAPTCHA:
    """Create .env file with your RECAPTCHA_SITE_KEY and RECAPTCHA_SECRET_KEY"""
    SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY", "")
    SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "")

    VERIFICATION_URL = "https://www.google.com/recaptcha/api/siteverify"

    RECAPTCHA_VERSION = "v2"

    def __init__(self):
        """Initializes reCAPTCHA."""
        self.is_verified = False
        self.token = None
        self.verification_result = None

    @staticmethod
    def get_html_script() -> str:
        """
        Returns HTML/JavaScript code for embedding on page.
        """
        html = f"""
        <!-- Google reCAPTCHA v2 Checkbox -->
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        
        <form>
            <div class="g-recaptcha" 
                 data-sitekey="{GoogleReCAPTCHA.SITE_KEY}"
                 data-callback="onRecaptchaSuccess"
                 data-expired-callback="onRecaptchaExpired">
            </div>
            
            <script>
                function onRecaptchaSuccess(token) {{
                    console.log("reCAPTCHA token: " + token);
                    // Send token to server for verification
                    document.getElementById("recaptcha_token").value = token;
                }}
                
                function onRecaptchaExpired() {{
                    console.log("reCAPTCHA expired");
                }}
            </script>
            
            <input type="hidden" id="recaptcha_token" name="recaptcha_token" value="">
        </form>
        """
        return html

    @staticmethod
    def get_recaptcha_info() -> dict:
        """
        Returns information about reCAPTCHA for demonstration.
        """
        return {
            "type": "Google reCAPTCHA v2 Checkbox",
            "version": GoogleReCAPTCHA.RECAPTCHA_VERSION,
            "description": "Requires user to confirm they are human",
            "setup_url": "https://www.google.com/recaptcha/admin",
            "documentation": "https://developers.google.com/recaptcha",
            "how_to_verify": {
                "1": "Get Site Key and Secret Key from Google Console",
                "2": "Embed JavaScript in form with Site Key",
                "3": "When form is submitted, get token",
                "4": "Send token to server for verification",
                "5": "Verify token using Secret Key",
            },
        }

    @staticmethod
    def open_setup_guide():
        """Opens the reCAPTCHA setup guide in browser."""
        setup_url = "https://www.google.com/recaptcha/admin"
        webbrowser.open(setup_url)
        return f"Opened reCAPTCHA setup page: {setup_url}"

    @staticmethod
    def get_verification_code_example() -> str:
        """
        Returns a code example for token verification on server (Python).
        """
        code = """
import requests

def verify_recaptcha(token, secret_key):
    '''
    Verifies reCAPTCHA token on the server.
    '''
    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    
    payload = {
        'secret': secret_key,
        'response': token
    }
    
    try:
        response = requests.post(verification_url, data=payload)
        result = response.json()
        
        # Successful verification if success=true and score > 0.5 (for v3)
        if result.get('success'):
            return True, "reCAPTCHA verified successfully"
        else:
            return False, "reCAPTCHA verification failed"
            
    except Exception as e:
        return False, f"Error during verification: {str(e)}"

# Usage:
is_valid, message = verify_recaptcha(token, SECRET_KEY)
        """
        return code

    def verify_token(self, token: str) -> Tuple[bool, str]:
        """
        Verifies reCAPTCHA token on the server (real verification).
        """
        if not requests:
            return (
                False,
                "Requests module not installed. Install it: pip install requests",
            )

        if not token:
            return False, "Token not received"

        payload = {"secret": self.SECRET_KEY, "response": token}

        try:
            response = requests.post(self.VERIFICATION_URL, data=payload, timeout=10)
            result = response.json()

            if result.get("success"):
                self.is_verified = True
                self.token = token
                self.verification_result = result
                return True, "reCAPTCHA verified successfully"
            else:
                errors = result.get("error-codes", [])
                return False, f"reCAPTCHA verification failed: {', '.join(errors)}"

        except requests.Timeout:
            return False, "Error: Timeout connecting to Google"
        except requests.RequestException as e:
            return False, f"Error during verification: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def simulate_verification(self, show_warning: bool = True) -> Tuple[bool, str]:
        """
        Simulates reCAPTCHA verification for demonstration.
        In a real project, real verification on the server is required.
        """
        if show_warning:
            info = self.get_recaptcha_info()
            message = (
                f"reCAPTCHA Demonstration\n"
                f"Type: {info['type']}\n"
                f"Version: {info['version']}\n\n"
                f"This module shows how to integrate Google reCAPTCHA.\n"
                f"For real integration you need to:\n"
                f"1. Register at {info['setup_url']}\n"
                f"2. Get Site Key and Secret Key\n"
                f"3. Embed JavaScript in the form\n"
                f"4. Verify token on the server\n\n"
                f"Read documentation: {info['documentation']}"
            )
            return True, message
        else:
            self.is_verified = True
            return True, "reCAPTCHA verified (demonstration)"

    def reset(self):
        """Resets verification state."""
        self.is_verified = False
        self.token = None
        self.verification_result = None


recaptcha = GoogleReCAPTCHA()
