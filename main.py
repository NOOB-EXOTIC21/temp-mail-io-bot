import telebot
import requests
import json
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6821301614:AAHpTiaOl2t0xXWCSBbn0c1gyQAguuufGEY')



@bot.message_handler(commands=['mails'])
def handle_mails(message):
    try:
        email_address = message.text.split(' ')[1]
        url = f"https://api.internal.temp-mail.io/api/v3/email/{email_address}/messages"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Application-Name': 'web',
            'Application-Version': '2.3.5',
            'Origin': 'https://temp-mail.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Referer': 'https://temp-mail.io/',
            'Connection': 'keep-alive',
            'Cookie': '__gads=ID=0a13956fc1df5715:T=1701595691:RT=1701607628:S=ALNI_MaHQN0S8jUAQtz6hkvTgNAAzbHyvQ; __gpi=UID=00000ca301c1cebf:T=1701595691:RT=1701607628:S=ALNI_MbHz2cRqu0aP4fUmbhXgGbZtrUMmQ; _ga=GA1.2.1538859660.1701595692; _gid=GA1.2.918112371.1701595693; _ga_3DVKZSPS3D=GS1.2.1701607623.3.1.1701608711.60.0.0; _gat=1',
            'TE': 'trailers'
        }
        response = requests.get(url, headers=headers)

        # Parse the JSON response
        data = response.json()

        # Check if there are emails in the response
        if not data:
            bot.send_message(message.chat.id, "No emails found for the given address.")
            return

        # Format and send the response to the user
        formatted_response = "Emails:\n"
        for email in data:
            formatted_response += f"ID: {email.get('id', 'N/A')}\n"
            formatted_response += f"From: {email.get('from', 'N/A')}\n"
            formatted_response += f"To: {email.get('to', 'N/A')}\n"
            formatted_response += f"Subject: {email.get('subject', 'N/A')}\n"
            formatted_response += f"Body Text: {email.get('body_text', 'N/A')}\n"
            formatted_response += "\n------------------------\n"

        bot.send_message(message.chat.id, formatted_response)

    except IndexError:
        bot.send_message(message.chat.id, "Invalid command format. Use /mails <email_address>")

@bot.message_handler(commands=['new'])
def handle_new(message):
    try:
        url = "https://api.internal.temp-mail.io/api/v3/email/new"
        payload = json.dumps({"min_name_length": 10, "max_name_length": 10})
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8',
            'Application-Name': 'web',
            'Application-Version': '2.3.5',
            'Origin': 'https://temp-mail.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Referer': 'https://temp-mail.io/',
            'Connection': 'keep-alive',
            'Cookie': '__gads=ID=0a13956fc1df5715:T=1701595691:RT=1701607628:S=ALNI_MaHQN0S8jUAQtz6hkvTgNAAzbHyvQ; __gpi=UID=00000ca301c1cebf:T=1701595691:RT=1701607628:S=ALNI_MbHz2cRqu0aP4fUmbhXgGbZtrUMmQ; _ga=GA1.2.1538859660.1701595692; _gid=GA1.2.918112371.1701595693; _ga_3DVKZSPS3D=GS1.2.1701607623.3.1.1701608711.60.0.0; _gat=1',
            'TE': 'trailers'
        }
        response = requests.post(url, headers=headers, data=payload)

        # Parse the JSON response
        data = response.json()

        # Send a formatted response to the user
        if 'email' in data and 'token' in data:
            email = data['email']
            token = data['token']
            bot.send_message(message.chat.id, f"New email created: {email} \nToken: {token}")
        else:
            bot.send_message(message.chat.id, "Failed to create a new email.")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    try:
        # Extract email and token from the command
        params = message.text.split(' ')
        email = params[1]
        tokenz = params[2]

        url = f"https://api.internal.temp-mail.io/api/v3/email/{email}"
        payload = json.dumps({"token": tokenz})
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Access-Control-Request-Method': 'DELETE',
            'Access-Control-Request-Headers': 'application-name,application-version,content-type',
            'Referer': 'https://temp-mail.io/',
            'Origin': 'https://temp-mail.io',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers',
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers, data=payload)

        # Send the response to the user
        bot.send_message(message.chat.id, response.text)

    except IndexError:
        bot.send_message(message.chat.id, "Invalid command format. Use /delete <email> <token>")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['help'])
def handle_delete(message):
   bot.send_message(message.chat.id, f"Welcome to Temp mail  Bot \n /new - to create new mail \n /delete  delete mail \n /delete <email> <token> \n /mails <email_address>")
# Start the bot
bot.polling()
