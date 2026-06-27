import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import streamlit.components.v1 as components
import base64
import cv2
import os

def load_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# =========================
# ----- LOAD MODEL --------
# =========================
@st.cache_resource
def load_tflite():

    interpreter = tf.lite.Interpreter(
        model_path="leafnet_dual_branch.tflite"
    )

    interpreter.allocate_tensors()

    return interpreter


try:
    interpreter = load_tflite()
    st.success("Model TFLite berhasil dimuat")
except Exception as e:
    st.exception(e)
    st.stop()

LABELS = [
    "Acalypha siamensis", "Andrographis paniculata", "Cananga odorata", "Capsicum sp", "Catharanthus roseus",
    "Dracaena angustifolia", "Ficus microcarpa", "Flueggea virosa", "Gardenia jasminoides", "Leucaena leucocephala",
    "Moringa oleifera", "Orthosiphon aristatus", "Pandanus amaryllifolius", "Phyllanthus amarus",
    "Physalis angulata", "Rosa sp", "Solanum nigrum", "Syzygium polyanthum", "Vernonia amygdalina", "Ziziphus mauritiana"
]

# =========================
# ----- DATABASE DINAMIS --------
# =========================
herbal_info = {
    "Andrographis paniculata": {
        "nama_umum": ["Sambiloto", "Ki pait", "Ampadu tanah", "Ki oray"],
        "status": "Tanaman herbal antidiabetes",
        "informasi": """
            Sambiloto terkenal sebagai herbal dengan kandungan andrographolide (AGL)
            yang sangat pahit, tetapi berkhasiat dalam mengendalikan kadar gula darah dan 
            bersifat antiinflamasi. AGL mampu meningkatkan produksi insulin dan  penyerapan 
            glukosa sehingga bisa mengurangi kadar gula dalam darah. 
        """,
        "tautan_artikel": "https://hellosehat.com/diabetes/daun-sambiloto-untuk-diabetes/",
        "tautan_jurnal": "https://jurnal.ikbis.ac.id/index.php/infokes/article/view/371/221 ",
        "cara_mengolah": [
            "Siapkan 25 lembar daun sambiloto dan 110 ml air.",
            "Cuci bersih daun sambiloto di bawah air mengalir.",
            "Rebus daun sambiloto sampai mendidih.",
            "Minum air rebusan daun sambiloto satu kali sehari dengan takaran 100 ml.",
            "Untuk menghindari risiko efek samping, disarankan untuk mengonsumsi dalam jumlah yang wajar dan tidak lebih dari dua kali sehari. Jika memiliki kondisi medis tertentu, konsultasikan terlebih dahulu dengan dokter sebelum mengonsumsi rebusan sambiloto.",
        ]
    },
    
    "Ziziphus mauritiana": {
        "nama_umum": ["Bidara", "Widara", "Bukol", "Kalangga", "Bekul", "Rangga"],
        "status": "Tanaman herbal antidiabetes",
        "informasi": """
            Daun bidara bisa membantu mengendalikan diabetes dengan membuat penggunaan insulin 
            untuk menyerap gula darah lebih efektif. Kandungan saponin dan flavonoid di dalam 
            daun bidara bekerja sebagai antioksidan yang dapat membantu melawan stres oksidatif 
            akibat radikal bebas. Dengan begitu, konsumsi ekstrak daun bidara dapat mendukung 
            pencegahan diabetes, terutama jika disertai pola hidup sehat.
        """,
        "tautan_artikel": "https://hellosehat.com/herbal-alternatif/herbal/daun-bidara/",
        "tautan_jurnal": "https://doi.org/10.26740/icaj.v6i2.32598",
        "cara_mengolah": [
            "Siapkan 10 lembar daun bidara tua, setengah buah jeruk nipis, dan gula secukupnya.",
            "Cuci bersih daun sambiloto di bawah air mengalir.",
            "Rebus 600ml air hingga mendidih lalu masukkan daun bidara.",
            "Masak selama 20 menit dengan api kecil.",
            "Peras jeruk nipis. Tambahkan gula sesuai selera.",
            "Untuk menghindari risiko efek samping, disarankan untuk mengonsumsi dalam jumlah yang wajar. Jika memiliki kondisi medis tertentu, konsultasikan terlebih dahulu dengan dokter sebelum mengonsumsi rebusan ini.",
        ]
    },

    "Pandanus amaryllifolius": {
        "nama_umum": ["Pandan wangi", "Pandan", "Pandan rampe", "Pandan arrum"],
        "status": "Tanaman herbal antidiabetes",
        "informasi": """
            Pandanus amaryllifolius adalah tanaman tropis yang umum dikenal sebagai pandan. Daun pandan mengandung senyawa seperti flavonoid, tanin, dan polifenol. Menurut sebuah studi dalam jurnal Pharmacognosy Magazine, ekstrak pandan mampu merangsang produksi hormon insulin dari pankreas.
        """,
        "tautan_artikel": "https://www.halodoc.com/artikel/manfaat-daun-pandan-dan-efek-sampingnya-bagi-tubuh?srsltid=AfmBOoq7fJ-Up5emjKX-zFlcgvMiiFUf-myDu9zotaOuc1uwwwfuYXun",
        "tautan_jurnal": "https://ejurnalmalahayati.ac.id/index.php/kebidanan/article/view/3024/pdf",
        "cara_mengolah": [
            "Siapkan 3-4 lembar daun pandan(segar atau kering), 500 ml air, dan pemanis alami(jika diperlukan).",
            "Cuci bersih daun pandan di bawah air mengalir lalu potong menjadi beberapa bagian.",
            "Rebus 500ml air hingga mendidih lalu masukkan potongan daun pandan.",
            "Biarkan daun pandan direbus selama 10-15 menit hingga air berubah warna menjadi hijau kekuningan.",
            "Saring air rebusan dan tuangkan ke dalam gelas (tambahkan pemanis alami jika diperlukan).",
            "Untuk menghindari risiko efek samping, disarankan untuk mengonsumsi dalam jumlah yang wajar. Jika memiliki kondisi medis tertentu, konsultasikan terlebih dahulu dengan dokter sebelum mengonsumsi rebusan ini.",
        ]
    },
}

def get_leaf_mask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(
        gray,
        240,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:
        largest = max(contours, key=cv2.contourArea)

        clean_mask = np.zeros_like(mask)

        cv2.drawContours(
            clean_mask,
            [largest],
            -1,
            255,
            -1
        )

        mask = clean_mask

    kernel = np.ones((5,5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    return mask

def make_rgb_input(image):

    img = np.array(image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = cv2.resize(
        img,
        (256,256),
        interpolation=cv2.INTER_CUBIC
    )

    mask = get_leaf_mask(img)

    img[mask == 0] = 0

    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    ).astype(np.float32)

    mean = np.array(
        [0.485,0.456,0.406]
    ) * 255

    std = np.array(
        [0.229,0.224,0.225]
    ) * 255

    img = (img - mean) / std

    return np.expand_dims(img,0)

def make_vein_input(image):

    img = np.array(image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = cv2.resize(
        img,
        (256,256),
        interpolation=cv2.INTER_CUBIC
    )

    mask = get_leaf_mask(img)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.bitwise_and(
        gray,
        gray,
        mask=mask
    )

    gray = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8,8)
    )

    vein = clahe.apply(gray)

    vein = cv2.bilateralFilter(
        vein,
        7,
        50,
        50
    )

    blur_large = cv2.GaussianBlur(
        vein,
        (21,21),
        0
    )

    highpass = cv2.subtract(
        vein,
        (blur_large * 0.7).astype(np.uint8)
    )

    sobelx = cv2.Sobel(
        highpass,
        cv2.CV_32F,
        1,
        0,
        ksize=3
    )

    sobely = cv2.Sobel(
        highpass,
        cv2.CV_32F,
        0,
        1,
        ksize=3
    )

    sobel = cv2.magnitude(
        sobelx,
        sobely
    )

    sobel = cv2.normalize(
        sobel,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    ).astype(np.uint8)

    vein = cv2.addWeighted(
        highpass,
        0.45,
        sobel,
        0.75,
        0
    )

    vein = cv2.normalize(
        vein,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    _, vein = cv2.threshold(
        vein,
        35,
        255,
        cv2.THRESH_TOZERO
    )

    vein[mask == 0] = 0

    vein = vein.astype(np.float32) / 255.0

    vein = np.stack(
        [vein, vein, vein],
        axis=-1
    )

    return np.expand_dims(
        vein,
        0
    )
    
# =========================
# ----- PREDIKSI ---
# =========================
def predict(image):

    rgb_input = make_rgb_input(image).astype(np.float32)
    vein_input = make_vein_input(image).astype(np.float32)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    for inp in input_details:

        name = inp["name"].lower()

        if "rgb" in name:
            interpreter.set_tensor(
                inp["index"],
                rgb_input
            )

        elif "vein" in name:
            interpreter.set_tensor(
                inp["index"],
                vein_input
            )

    interpreter.invoke()

    pred = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    top_idx = np.argsort(pred)[::-1]

    top5 = []

    for idx in top_idx[:5]:
        top5.append(
            (
                LABELS[idx],
                float(pred[idx])
            )
        )

    return top5

# =========================
# ------ USER INTERFACE -------
# =========================
st.set_page_config(page_title="Sistem Identifikasi Herbal Antidiabetes Berbasis LeafNet 🌿 ", layout="wide")

# --- GLOBAL ADAPTIVE CSS ---
st.markdown("""
<style>
/* ===============================
   VARIABEL WARNA ADAPTIF GLOBAL
   =============================== */
:root {
    /* Light mode */
    --bg-box: #f1f1f1;
    --border-box: #d0d0d0;

    --bg-uploader: #f8f8f8;
    --border-uploader: #bbb;
}

@media (prefers-color-scheme: dark) {
    :root {
        /* Dark mode */
        --bg-box: #2a2a2a;
        --border-box: #444;

        --bg-uploader: #1f1f1f;
        --border-uploader: #555;
    }
}

/* ===============================
   INFO BOX (nama ilmiah/umum)
   =============================== */
.info-box, .adaptive-box {
    background: var(--bg-box) !important;
    border: 1px solid var(--border-box) !important;
    padding: 18px;
    border-radius: 12px;
    color: inherit !important;
}

/* ===============================
   FILE UPLOADER BOX
   =============================== */
[data-testid="stFileUploader"] section {
    background: var(--bg-uploader) !important;
    border: 3px dashed var(--border-uploader) !important;
    padding: 60px !important;
    border-radius: 20px !important;
    min-height: 260px !important;
}

/* Agar teks + ikon uploader terlihat */
[data-testid="stFileUploader"] * {
    color: inherit !important;
}

/* Kolom tetap rata atas */
div[data-testid="column"] > div {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

/* Section title */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 25px;
}

/* DISCLAIMER BOX ADAPTIVE */
.disclaimer-box {
    padding: 12px 18px;
    border-radius: 10px;
    margin-top: 60px;
    font-size: 15px;
    line-height: 1.45;
}

/* Light Mode */
@media (prefers-color-scheme: light) {
    .disclaimer-box {
        background: #f8f8f8;
        color: #333;
        border: 1px solid #ddd;
    }
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
    .disclaimer-box {
        background: #2a2a2a;
        color: #e2e2e2;
        border: 1px solid #444;
    }
}

/* FOOTER */
.custom-footer {
    padding: 10px 0 25px 0;
    text-align: center;
    background: none !important;   /* TANPA KOTAK */
    border: none !important;
    color: inherit !important;     /* Ikut tema */
}
</style>
""", unsafe_allow_html=True)


# ---- HEADER ----
logo_base64 = load_base64("images/diaherb_logo.png")
components.html(f"""
    <div style="
        padding:0 20px; 
        width:100%; 
        display:flex; 
        align-items:center;
    ">
        <img src="data:image/png;base64,{logo_base64}"
             style="height:100px; width:auto;
             filter: drop-shadow(0px 0px 4px rgba(0,0,0,0.35));">
    </div>
    <hr>
""", height=100)


# -------------------------------
# PAGE SELECTOR
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "upload"
    
# =======================
# === HALAMAN UPLOAD ====
# =======================
if st.session_state.page == "upload":
    
    st.markdown("""
        <h2 style="margin:0px; font-size:45px; font-weight:600;">Sistem Identifikasi Daun Herbal Antidiabetes Berbasis Model LeafNet</h2>
        <p style="font-size:18px; margin-bottom:70px; width:95%;">DiaHerb merupakan sebuah 
        sistem berbasis teknologi yang dikembangkan untuk mengidentifikasi tanaman herbal 
        antidiabetes berdasarkan citra daun. DiaHerb bertujuan mengidentifikasi tanaman herbal 
        antidiabetes secara tepat untuk mendukung penelitian dan edukasi masyarakat, serta 
        mempromosikan potensi tanaman herbal lokal Indonesia. Sistem ini dibangun berbasis Deep 
        Learning menggunakan Model LeafNet yang diintegrasikan dengan Transfer Learning untuk menganalisis ciri pada daun.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.6,1.2])

    with col1:
        # CUSTOM CSS – UBAH FILE UPLOADER JADI KOTAK BESAR
        st.markdown("""
        <style>
        [data-testid="stFileUploader"] section {
            border: 3px dashed #999 !important;
            padding: 60px !important;
            border-radius: 20px !important;
            background: #fafafa;
            min-height: 260px !important;
        }
        /* Pastikan kolom kiri & kanan sejajar di atas */
        div[data-testid="column"] > div {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        </style>
        """, unsafe_allow_html=True)
        
        uploaded_img = st.file_uploader("", type=["jpg","jpeg","png", "webp"])

        img = None 
        
        # PREVIEW GAMBAR
        if uploaded_img is not None:
            try:
                img = Image.open(uploaded_img)
                st.markdown("##### 📌 Preview Gambar:")
                st.image(img, width=320)
            except Exception as e:
                st.error(f"Format gambar tidak dapat dibaca: {e}")
        
        # =============================
        # TOMBOL IDENTIFIKASI
        # =============================
        if st.button("🔍 Identifikasi Daun", use_container_width=True):
            if uploaded_img:
                st.session_state.image = uploaded_img
                st.session_state.page = "result"
                st.rerun()
            else:
                st.warning("Silakan unggah gambar terlebih dahulu.")

    # =============================
    # TIPS PENGAMBILAN GAMBAR
    # =============================
    st.markdown("""
    <style>
        /* Rapatkan jarak antar gambar dalam kolom */
        div[data-testid="column"] div:has(img) {
            padding-right: 5px !important;
            padding-left: 5px !important;
            margin-right: 0 !important;
            margin-left: 0 !important;
        }
    
        /* Hilangkan margin top berlebih pada gambar */
        div[data-testid="column"] div:has(img) {
            margin-top: 5px !important;
        }
    
    </style>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <b style="font-size:18px; font-weight:600; margin-left:30px; margin-top:30px;">Tips pengambilan gambar</b>
            <ul style="margin-left:30px;">
                <li>Foto 1 helai daun saja.</li>
                <li>Pastikan helai daun berada tepat di tengah frame kamera.</li>
                <li>Pastikan pencahayaan mencukupi agar model dapat melihat venasi/urat daun.</li>
                <li>Latar belakang daun wajib polos dan berwarna cerah (diutamakan putih).</li>
                <li>Foto objek tidak terlalu jauh.</li>
                <li>Foto dari sisi atas atau bawah helai daun.</li>
            </ul>
    
            <b style="font-size:18px; font-weight:600; margin-left:30px;">Contoh gambar yang baik</b>
        """, unsafe_allow_html=True)

        # Gambar contoh: 3 atau 4
        offset_col, *ex_cols = st.columns([0.2, 1, 1, 1, 1])
        
        example_paths = [
            "images/IMG_20251028_152831.jpg",
            "images/IMG_20251029_170845.jpg",
            "images/IMG_20251031_131056.jpg",
            "images/IMG_20251114_161441.jpg"
        ]
        
        for col, path in zip(ex_cols, example_paths):
            with col:
                st.image(path, width=150)

# =======================
# === HALAMAN HASIL =====
# =======================
elif st.session_state.page == "result":

    st.markdown("""
        <h2 style="margin-bottom:30px; font-size:50px; font-weight:600; text-align:center;">
            Hasil Identifikasi
        </h2>
    """, unsafe_allow_html=True)

    img = Image.open(st.session_state.image)
    top5 = predict(img)

    pred_name = top5[0][0]
    conf = top5[0][1]

    # ambil data dari database
    data = herbal_info.get(pred_name, None)

    colA, colB = st.columns([1.5,1])

    # =====================================
    # KOLOM A — GAMBAR + INFO BOX (KIRI)
    # =====================================
    with colA:
        colA1, colA2 = st.columns([1, 1.2])
        
        # --- KIRI: Gambar ---
        with colA1:
            st.image(img, caption="Gambar yang diunggah", use_column_width=True)

        # --- CSS untuk info box ---
        st.markdown("""
            <style>
            .info-box {
                background: var(--bg-box);
                border: 1px solid var(--border-box);
                padding: 18px;
                border-radius: 12px;
                min-height: 340px;
            }
            .section-title {
                font-size: 20px;
                font-weight: 600;
                margin-top: 25px;
            }
            </style>
        """, unsafe_allow_html=True)

        # --- KANAN: Box Info ---
        with colA2:
            # buat list nama umum dalam HTML
            if data and "nama_umum" in data:
                list_html = "<ul style='margin-top:5px;'>"
                for nm in data["nama_umum"]:
                    list_html += f"<li>{nm}</li>"
                list_html += "</ul>"
            else:
                list_html = "<ul><li>Tidak tersedia</li></ul>"
        
            # HTML box lengkap
            html_box = f"""
                <div class="info-box">
                    <b class="section-title">Nama Ilmiah:</b><br>
                    <span style="font-size:40px; font-weight:300;"><i>{pred_name}</i></span>
                    <br><br>
                    <b class="section-title">Nama Umum:</b>
                    {list_html}
                </div>
            """
            st.markdown(html_box, unsafe_allow_html=True)

    # =====================================
    # KOLOM B — STATUS + CONFIDENCE (KANAN)
    # =====================================
    with colB:
        st.markdown(f"""
            <div class="adaptive-box">
                <b class='section-title'>Status</b><br>
                <b style="color:#018790; font-weight:400;">{data['status'] if data else "Bukan herbal antidiabetes"}</b><br><br>
                <b>Tingkat kepercayaan sistem: </b> 
                <b style="color:#018790;">{conf * 100:.2f}% </b>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Top-5 Prediksi")

    for i,(label,score) in enumerate(top5,1):

        st.write(
            f"{i}. {label} — {score*100:.2f}%"
        )

        st.progress(float(score))

    # === Informasi ===
    st.markdown("<div class='section-title'>Informasi herbal:</div>", unsafe_allow_html=True)
    st.markdown(data["informasi"] if data else "Tidak ada informasi.", unsafe_allow_html=True)

    # === Tautan Artikel ===
    st.markdown("<div class='section-title'>Tautan ke artikel terkait: </div>", unsafe_allow_html=True)
    st.markdown(
        f"<a href='{data['tautan_artikel']}' target='_blank'>{data['tautan_artikel']}</a>"
        if data else "Tidak ada link.",
        unsafe_allow_html=True
    )

    # === Tautan Jurnal Penelitian ===
    st.markdown("<div class='section-title'>Tautan ke jurnal penelitian:</div>", unsafe_allow_html=True)
    st.markdown(
        f"<a href='{data['tautan_jurnal']}' target='_blank'>{data['tautan_jurnal']}</a>"
        if data else "Tidak ada link.",
        unsafe_allow_html=True
    )

    # === Cara Mengolah ===
    st.markdown("<div class='section-title', style='margin-bottom:10px;'>Cara mengolah herbal:</div>", unsafe_allow_html=True)
    if data:
        for langkah in data["cara_mengolah"]:
            st.markdown(f"- {langkah}")
    else:
        st.markdown("- Tidak ada data.")

    # Jarak & tombol kembali
    st.markdown("<div style='height:70px;'></div>", unsafe_allow_html=True)
    st.button("⬅️ Kembali", on_click=lambda: (st.session_state.update({"page": "upload"}), st.rerun()))

# ---- DISCLAIMER BOX ----
st.markdown("""
<div class="disclaimer-box">
    <strong><b style="font-size:18px; font-weight:700;">Catatan penafian / <i>disclaimer notice</i> : </b></strong><br>
    <i>Sistem ini dikembangkan sebagai bagian dari penyusunan tugas akhir.
    Hasil prediksi bersifat estimasi dan tidak dimaksudkan sebagai acuan medis atau botani yang bersifat final.
    Validasi tetap disarankan melalui ahli terkait.</i>
</div>
""", unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("""
<div class="custom-footer">
    <hr>
    ©2025 | Tugas Akhir Skripsi | 211401034
</div>
""", unsafe_allow_html=True)
