from flask import Flask, request, render_template, jsonify, flash
import openai
import os
import logging
import json

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize OpenAI client
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OpenAI API key not found in environment variables")

client = openai.OpenAI(api_key=openai_api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            description = request.form.get("description", "").strip()
            language = request.form.get("language", "English")

            if not description:
                flash("Please provide a tattoo description.", "danger")

            content = generate_marketing_content(description, language)
            return render_template("index.html", output=content, description=description, language=language)

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("index.html")

    return render_template("index.html")


def generate_marketing_content(description, language):
    """Generate tattoo marketing content using OpenAI's API"""
    try:
        prompt = f"""
        You are a marketing expert for a tattoo brand. Based on the following tattoo description, generate the following in {language}:

        1. Instagram Caption: A catchy Instagram caption (max 2 sentences)
        2. Facebook Post: A Facebook post caption (slightly longer, informal, with call-to-action)
        3. Pinterest Title: A concise Pinterest title
        4. Pinterest Description: A short Pinterest description
        5. Pinterest Hashtags: 20 Pinterest hashtags
        6. Alt Text: Alt-text for the image
        7. SEO Title: An SEO-friendly product title (for Etsy/Whop)

        Tattoo description: {description}

        Format your response in JSON with the following keys: instagram_caption, facebook_post, pinterest_title, pinterest_description, pinterest_hashtags, alt_text, seo_title
        """

        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        content = json.loads(response.choices[0].message.content)
        return content
    
    except openai.APIError as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        raise Exception(f"OpenAI API Error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise Exception(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
