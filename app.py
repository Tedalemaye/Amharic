from flask import Flask, request, render_template_string
from gtts import gTTS
import pygame
import io

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Amharic Text-to-Speech</title>
</head>
<body>
    <h1>Amharic Text-to-Speech</h1>
    <form method="POST">
        <textarea name="text" rows="4" cols="50" placeholder="Paste your Amharic text here...">ሰላም እንዴት ነህ?</textarea>
        <br>
        <button type="submit">Read Aloud</button>
    </form>
    <div id="status"></div>
    <audio id="player" controls style="display:none;"></audio>
    <script>
    document.querySelector('form').onsubmit = function(e) {
        e.preventDefault();
        document.getElementById('status').innerHTML = "Reading text aloud...";
        fetch('/', {
            method: 'POST',
            body: new FormData(this),
        }).then(response => response.blob())
        .then(blob => {
            var url = window.URL.createObjectURL(blob);
            var player = document.getElementById('player');
            player.src = url;
            player.style.display = 'block';
            player.play();
            document.getElementById('status').innerHTML = "Playback complete.";
        });
    };
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            try:
                tts = gTTS(text=text, lang='am', slow=False, lang_check=False)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                return audio_fp.getvalue(), {'Content-Type': 'audio/mpeg'}
            except Exception as e:
                return str(e), 400
        else:
            return "Please enter Amharic text.", 400
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
