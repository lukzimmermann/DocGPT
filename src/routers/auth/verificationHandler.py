import datetime
import enum
import os
from secrets import token_urlsafe
from dotenv import load_dotenv
from fastapi import HTTPException, status
from postgres import PostgresDB
from utils.mail import send_mail
from utils.singelton import singleton

load_dotenv()

verification_page = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      body {
        background-color: #1a1a1a; /* Dark background color */
        color: #fff; /* White text color */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        font-family: Arial, sans-serif;
      }
      .container {
        padding: 20px;
        background-color: #333; /* Dark gray container background */
        border-radius: 2em;
        text-align: center;
      }
      a {
        color: #3498db; /* Blue link color */
        text-decoration: none;
      }
      a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h3>Email Verification Successful</h1>
      <p>Your email has been successfully verified.</p>
      <p>Click <a href="login.html">here</a> to go to the login page.</p>
    </div>
  </body>
</html>
"""

no_valid_token_page = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      body {
        background-color: #1a1a1a; /* Dark background color */
        color: #fff; /* White text color */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        font-family: Arial, sans-serif;
      }
      .container {
        padding: 20px;
        background-color: #333; /* Dark gray container background */
        border-radius: 2em;
        text-align: center;
      }
      a {
        color: #3498db; /* Blue link color */
        text-decoration: none;
      }
      a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h3>No verification possible</h1>
    </div>
  </body>
</html>
"""

class VerificationItem():
        def __init__(self, email: str, token: str) -> None:
            self.email = email
            self.token = token

@singleton
class VerificationHandler():

    def __init__(self) -> None:
        self.verification_list: list[VerificationItem] = []

    def send_verification(self, email: str):
        try:
            token = token_urlsafe(64)
            base_url = os.getenv("BASE_API_URL")
            verification_url = f"{base_url}verification/{token}"

            body = f"""
               <html>
                 <body>
                   <h3>Hello</h3>
                   <p>Please verify your E-Mail Address with the following link:</p>
                   <a href="{verification_url}">Verification-Link</a>
                   <p></p>
                   <p></p>
                   <p>Have fun...</p>
                 </body>
               </html>
               """
            send_mail(email, "ZHAW GPT verification", body)
            self.verification_list.append(VerificationItem(email, token))

        except:
             return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Can not send verification mail")
        
    def verify_email(self, token: str):
        for item in self.verification_list:
            if item.token == token:
                pg = PostgresDB()
                pg.connect()

                data = (item.email,)
                pg.executeQuery("""
                                UPDATE users
                                SET is_verified = True
                                WHERE email = %s
                                """, data)
                pg.disconnect()

                return verification_page
          
        return no_valid_token_page