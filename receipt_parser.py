
import ollama
from PIL import Image
import io
import ollama
import os
from dotenv import load_dotenv

load_dotenv()


prompt = """このレシート画像を解析し、生テキストを以下のJSONフォーマットで出力してください。
                    不明な部分はnullとしてください。
                    JSON以外のテキストは含めないでください。
                    {
                      "store_name": "店舗名",
                      "date": "YYYY/MM/DD hh:mm",
                      "items": [{"name": "商品名", "price": 数値}],
                      "total_amount": 数値
                    }"""

# prompt = "Analyze the receipt and output the result in JSON format with keys: store_name, date, items, total_amount."
model = "qwen3.5:4b"

client = ollama.Client(os.getenv("OLLAMA_URL", "http://localhost:11434"))


def parse_receipt(image_bytes):
    response = client.generate(
        model=model,
        prompt=prompt,
        images=[image_bytes],
        stream=False,
        options={
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "min_p": 0.0,
            "presence_penalty": 1.5,
            "repeat_penalty": 1.0,
        }
    )

    raw_text = response['response']
    # json部分を取り出す
    start = raw_text.find('{')
    end = raw_text.rfind('}') + 1
    raw_text = raw_text[start:end]
    # JSON判定
    import json
    try:
        json.loads(raw_text)
        return raw_text
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw_text": raw_text}
