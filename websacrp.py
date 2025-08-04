from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')

def home():
    name="Virat_Kohli"
    url = f"https://en.wikipedia.org/wiki/{name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract summary paragraphs
    summary_paragraphs = []
    for para in soup.select("p"):
        text = para.get_text().strip()
        if text and not text.lower().startswith("coordinates"):
            summary_paragraphs.append(text)
        if len(summary_paragraphs) >= 4:
            break

    # Extract main image
    image_url = ""
    infobox = soup.find("table", {"class": "infobox"})
    if infobox:
        img = infobox.find("img")
        if img:
            image_url = "https:" + img["src"]

  

    return render_template("about.html", summary=summary_paragraphs, image_url=image_url,name=name)


if __name__ == "__main__":
    app.run(debug=True)
