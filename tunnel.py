from pyngrok import ngrok

# Start ngrok tunnel to port 8502
public_url = ngrok.connect(8502)
print(f"Public URL: {public_url}")

# Keep the tunnel open
input("Press Enter to stop the tunnel...")
ngrok.disconnect(public_url)
