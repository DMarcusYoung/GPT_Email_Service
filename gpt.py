import openai
import os
from dotenv import load_dotenv

load_dotenv()

def emailSummary(emails):
    summaries = []
    for e in emails:
        subject, sender, body = e
        if not subject:
            print('No Message found.')
            summaries.append(None)
            continue
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        summary = openai.ChatCompletion.create(
            # model="gpt-4",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Summarize this email for me: " + str(body)},
            ]
        )
        print(summary)
        summaries.append(summary)

        
    rank = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Rank those emails by importance:" + str(summaries)},
        ]
    )
    print(rank)

    return summaries