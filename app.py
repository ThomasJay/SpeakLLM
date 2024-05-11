from flask import Flask, request

from elevenlabs.client import ElevenLabs
from elevenlabs import play
from elevenlabs import stream

from langchain_community.llms import Ollama

client = ElevenLabs()  # Defaults to ELEVEN_API_KEY

cached_llm = Ollama(model="llama3", base_url="http://localhost:11434")

app = Flask(__name__)


# audio = client.generate(
#     text="Hello World",
#     voice="Rachel",
#     model="eleven_multilingual_v2",
# )
# play(audio)

# audio_stream = client.generate(text="Hello World", stream=True)
# stream(audio_stream)


@app.route("/llm", methods=["POST"])
def llmPost():
    print("Post /llm called")
    json_content = request.json
    query = json_content.get("query")

    audio_stream = client.generate(text="You asked: " + query, stream=True)
    stream(audio_stream)

    response = cached_llm.invoke(query)

    print(response)

    audio_stream = client.generate(text=response, stream=True)
    stream(audio_stream)

    response_answer = {"answer": response}

    return response_answer


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    start_app()

