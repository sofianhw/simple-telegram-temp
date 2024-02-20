# Paypal
poetry run python paypal.py

# Telegram

## Change Directory
cd sandbox

## Init DB
poetry run -C .. python initdb.py

## Start Bot
poetry run -C .. python main.py

# Notes
Paypal will use env in root folder, and telegram bot will use env in its folder.