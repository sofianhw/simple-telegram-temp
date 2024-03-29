import uvicorn
from fastapi import FastAPI, Request
from db_utils import deposit, record_transaction
from standalone import send_chat

app = FastAPI()

@app.post("/paypal-webhook")
async def paypal_webhook(request: Request):
    # Receive the request as JSON
    data = await request.json()
    print(data)
    # Check if the event is a completed order
    if data['event_type'] == 'CHECKOUT.ORDER.APPROVED':
        # Handle the completed order
        # Implement your logic here
        print("Order completed!")
        custom_id = data['resource']['purchase_units'][0]['custom_id']
        user_id, bot_id, date = custom_id.split('-')
        amount = int(float(data['resource']['purchase_units'][0]['amount']['value']))
        quota = amount * 3
        try:
            print(f"user = {user_id} top up ${amount} get {quota} to {bot_id} on {date}")
            record_transaction(user_id, amount, quota, bot_id)
            deposit(user_id, quota, bot_id)
            send_chat(user_id, f"Thanks for top up ${amount} for {amount*3} chats, you can check your current balance with /balance .")
        except:
            return {"error": f"{bot_id} is Not Found"}
        # Return a success response
        return {"status": "success"}
    else:
        # If the event is not what we're looking for, ignore it
        return {"status": "ignored"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8111)