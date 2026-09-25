from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/", methods=["GET", "POST"])
def index():
    blurb = None
    title = ""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            resp = client.chat.completions.create(
                model=os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b"),
                messages=[
                    {"role": "system", "content": "Write one punchy one-line bookshop shelf-talker blurb for the given title. Under 20 words. No surrounding quotes."},
                    {"role": "user", "content": title}
                ],
                max_tokens=60
            )
            blurb = resp.choices[0].message.content.strip()
    return render_template("index.html", blurb=blurb, title=title)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
