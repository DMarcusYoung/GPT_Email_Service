import openai

def emailSummary(email):
    subject, sender, body = email
    openai.api_key = "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"
    res = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize this email for me: " + str(body)},
        ]
    )
    print(res)

# emailSummary("Hello, I am a Nigerian prince. I have $1")