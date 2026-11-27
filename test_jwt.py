from app.core.security import ( 
    create_access_token,
    verify_access_token,
)

token = create_access_token(
    data={"sub":"1"}
)

print("Generated token: ",token)

payload = verify_access_token(token)

print("Decoded payload:", payload)
print("User ID:", payload["sub"])