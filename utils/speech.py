import streamlit.components.v1 as components

def speak_text(text, lang_code="en-IN"):

    clean_text = (
        text.replace("'", "")
        .replace('"', "")
        .replace("\n", " ")
    )

    js_code = f"""
    <script>

    window.speechSynthesis.cancel();

    var msg = new SpeechSynthesisUtterance(
        `{clean_text}`
    );

    msg.lang = "{lang_code}";
    msg.rate = 0.9;

    window.speechSynthesis.speak(msg);

    </script>
    """

    components.html(js_code, height=0)