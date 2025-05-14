from flask import Flask, request, render_template_string, flash
import openai
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Setup OpenAI
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY not set")
openai.api_key = openai_api_key

@app.route("/", methods=["GET", "POST"])
def index():
    content = ""
    description = ""
    language = ""

    if request.method == "POST":
        try:
            description = request.form.get("description", "").strip()
            language = request.form.get("language", "English")

            if not description:
                flash("Please provide a tattoo description.", "danger")
            else:
                content = generate_marketing_content(description, language)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tattoo Caption + Marketing Generator</title>
        <style>
            body { font-family: sans-serif; padding: 2rem; background: #f5f5f5; }
            input, select, button, textarea { margin-top: 1rem; width: 100%; padding: 10px; }
            .result { margin-top: 2rem; background: #fff; padding: 1rem; border-radius: 6px; }
        </style>
    </head>
    <body>
        <h2>Tattoo Caption + Marketing Generator</h2>
        <form method="post">
            <label>Describe your tattoo design:</label>
            <input name="description" placeholder="e.g. realistic rabbit with flowers, black and grey style" required>

            <label>Select language for the output:</label>
            <select name="language">
              <option value="English">English</option>
              <option value="Dutch">Dutch</option>
            </select>

            <button type="submit">Generate Marketing Content</button>
        </form>

        {% if output %}
        <div class="result">
            <h3>Generated Content:</h3>
            <pre>{{ output }}</pre>
        </div>
        {% endif %}
    </body>
    </html>
    """, output=content)

def generate_marketing_content(description, language):
    prompt = f"""
You are a marketing expert for a tattoo brand. Based on the following tattoo description, generate the following in {language}:

1. A catchy Instagram caption (max 2 sentences)
2. A Facebook post caption (slightly longer, informal, with call-to-action)
3. A Pinterest title
4. A short Pinterest description
5. 20 Pinterest hashtags
6. Alt-text for the image
7. An SEO-friendly product title (for Etsy/Whop)

Tattoo description: {description}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    return response["choices"][0]["message"]["content"]
