from flask import Flask, request, render_template_string
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Meme Generator</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        input[type="text"], input[type="file"] { width: 100%; margin-bottom: 10px; padding: 8px; }
        input[type="submit"] { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .result { margin-top: 20px; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; }
        .btn-download { display: inline-block; margin-top: 10px; padding: 10px 20px; background-color: #008CBA; color: white; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Meme Generator</h1>

        <!-- The Form -->
        <form method="post" enctype="multipart/form-data">
            <p>Upload Image:</p>
            <input type="file" name="image" required accept="image/*">

            <p>Top Text:</p>
            <input type="text" name="upper" placeholder="TOP TEXT">

            <p>Bottom Text:</p>
            <input type="text" name="lower" placeholder="BOTTOM TEXT">

            <input type="submit" value="Generate Meme">
        </form>

        <!-- The Result (Only shows if img_data is present) -->
        {% if img_data %}
        <div class="result">
            <h2>Your Meme:</h2>
            <img src="data:image/jpeg;base64,{{ img_data }}" alt="Generated Meme">
            <br>
            <a href="data:image/jpeg;base64,{{ img_data }}" download="meme.jpg" class="btn-download">Download Meme</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''


def get_font():
    try:
        return ImageFont.truetype("arial.ttf", 65)
    except IOError:
        return ImageFont.load_default()


@app.route('/', methods=['GET', 'POST'])
def home():
    img_data = None

    if request.method == 'POST':
        file = request.files['image']
        text_upper = request.form.get('upper', '')
        text_lower = request.form.get('lower', '')

        if file:
            img = Image.open(file.stream)
            draw = ImageDraw.Draw(img)
            font = get_font()

            if text_upper:
                draw.text(
                    (img.size[0] / 2, 30),
                    text_upper,
                    font=font,
                    fill="white",
                    stroke_width=4,
                    stroke_fill="black",
                    anchor="mt"
                )

            if text_lower:
                draw.text(
                    (img.size[0] / 2, img.size[1] - 30),
                    text_lower,
                    font=font,
                    fill="white",
                    stroke_width=4,
                    stroke_fill="black",
                    anchor="mb"
                )

            buffer = io.BytesIO()
            img.convert('RGB').save(buffer, format="JPEG")
            buffer.seek(0)

            img_data = base64.b64encode(buffer.getvalue()).decode()

    return render_template_string(HTML_TEMPLATE, img_data=img_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
