# Boxcar Apartment Availability Monitor

This Python script monitors [Boxcar Apartments](https://boxcar.tarragon.com/floorplans) for **non-MFTE** unit availability and sends real-time SMS alerts via Twilio when a qualifying unit becomes available.

## Features

- Filters out MFTE/income-restricted floorplans
- Detects real-time unit availability
- Sends SMS alerts using Twilio
- Designed to run persistently with `nohup`
- Environment variables used for API credentials

## Requirements

- Python 3.8+
- Google Chrome + ChromeDriver
- Twilio account (with a verified phone number)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/boxcar-bot.git
   cd boxcar-bot
   ```

2. Create an env with your credentials:
   TWILIO_SID=your_account_sid
   TWILIO_AUTH=your_auth_token
   TWILIO_FROM=your_twilio_number
   TWILIO_TO=your_verified_phone_number

3. Install requirements
   pip install selenium twilio python-dotenv
