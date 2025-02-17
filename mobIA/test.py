from google import genai

client = genai.Client(api_key="AIzaSyDmnQ4CIwSSPCkiTYtW0hZVtNeDqQSEcxM")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)
