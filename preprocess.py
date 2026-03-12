# preprocess.py
from PIL import Image
import io

def prepare_image(uploaded_file, max_size=(1024, 1024), threshold=96):
    img = Image.open(uploaded_file)
    
    # グレースケールに変換
    img = img.convert("L")

    
    # リサイズ
    # img = img.resize((min(img.width, max_size[0]), min(img.height, max_size[1])), Image.Resampling.LANCZOS)
    
    # RGB変換（JPEG保存用）
    # img = img.convert("RGB")
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=50)
    return buf.getvalue()