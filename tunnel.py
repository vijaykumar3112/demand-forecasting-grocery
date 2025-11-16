from pyngrok import ngrok

# Start ngrok tunnel to port 8503
public_url = ngrok.connect(8503)
print(f"Public URL: {public_url}")

# Keep the tunnel open
input("Press Enter to stop the tunnel...")
ngrok.disconnect(public_url)
