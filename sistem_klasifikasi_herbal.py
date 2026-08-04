import React, { useState } from "react";
import { 
  Upload, 
  ArrowLeft, 
  RotateCcw,
  BookOpen, 
  Leaf, 
  AlertTriangle, 
  CheckCircle2, 
  Info,
  ChevronRight,
  ExternalLink
} from "lucide-react";

// Types for Herb Data
interface HerbDetail {
  nama_umum: string[];
  status: string;
  informasi: string;
  tautan_artikel: string;
  tautan_jurnal: string;
  cara_mengolah: string[];
  catatan: string;
}

// Full database of 20 classes mapped exactly from python code
const herbalInfo: Record<string, HerbDetail> = {
  "Acalypha siamensis": {
    nama_umum: ["Teh-tehan", "Teh hutan"],
    status: "Tanaman pembanding",
    informasi: "Teh-tehan adalah tanaman perdu atau semak yang sering digunakan sebagai pagar hidup dekoratif.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Andrographis paniculata": {
    nama_umum: ["Sambiloto", "Ki pait", "Ampadu tanah", "Ki oray"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Sambiloto terkenal sebagai herbal dengan kandungan andrographolide (AGL) yang sangat pahit, tetapi berkhasiat tinggi dalam mengendalikan kadar gula darah dan bersifat antiinflamasi. AGL mampu meningkatkan produksi insulin dan penyerapan glukosa sehingga mengurangi kadar gula dalam darah.",
    tautan_artikel: "https://hellosehat.com/diabetes/daun-sambiloto-untuk-diabetes/",
    tautan_jurnal: "https://jurnal.ikbis.ac.id/index.php/infokes/article/view/371/221",
    cara_mengolah: [
      "Siapkan 25 lembar daun sambiloto segar dan 110 ml air bersih.",
      "Cuci bersih daun sambiloto di bawah air mengalir.",
      "Rebus daun sambiloto sampai air mendidih.",
      "Minum air rebusan daun sambiloto satu kali sehari dengan takaran 100 ml."
    ],
    catatan: "Untuk menghindari risiko efek samping, disarankan untuk mengonsumsi dalam jumlah yang wajar dan tidak lebih dari dua kali sehari. Jika memiliki kondisi medis tertentu, konsultasikan terlebih dahulu dengan dokter."
  },
  "Cananga odorata": {
    nama_umum: ["Kenanga", "Kananga", "Sepalen"],
    status: "Tanaman pembanding",
    informasi: "Kenanga adalah tanaman tropis yang bunganya sangat harum. Dimanfaatkan sebagai bahan utama aromaterapi dan kosmetik.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Capsicum sp": {
    nama_umum: ["Cabai", "Lombok"],
    status: "Tanaman pembanding",
    informasi: "Cabai adalah tanaman hortikultura dari famili terong-terongan yang digunakan sebagai bumbu dapur.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Catharanthus roseus": {
    nama_umum: ["Tapak dara", "Bunga serdadu", "Kembang tembaga"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Ekstrak daun tapak dara dipercaya dapat merangsang sekresi insulin dalam sel beta pankreas dan meningkatkan penggunaan glukosa di jaringan perifer, membantu menjaga kestabilan gula darah.",
    tautan_artikel: "https://hellosehat.com/herbal-alternatif/herbal/manfaat-daun-tapak-dara/",
    tautan_jurnal: "https://jurnal.unpad.ac.id/farmaka/article/view/47508/pdf",
    cara_mengolah: [
      "Siapkan 5-10 lembar daun tapak dara yang masih segar dan 2 gelas air.",
      "Cuci bersih daun tapak dara di bawah air mengalir.",
      "Rebus daun dengan api kecil sampai air berubah warna.",
      "Saring dan biarkan hingga hangat sebelum diminum."
    ],
    catatan: "Disarankan mengonsumsi satu gelas sehari. Konsultasikan dengan dokter untuk rencana pengobatan yang aman."
  },
  "Dracaena angustifolia": {
    nama_umum: ["Suji", "Suji hijau", "Semar"],
    status: "Tanaman pembanding",
    informasi: "Suji hijau adalah tumbuhan perdu tahunan yang daunnya dimanfaatkan sebagai pewarna hijau alami makanan.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Ficus microcarpa": {
    nama_umum: ["Beringin dolar", "Beringin cina"],
    status: "Tanaman pembanding",
    informasi: "Beringin dolar adalah spesies pohon ara tropis yang populer sebagai tanaman hias dan bahan bonsai.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Flueggea virosa": {
    nama_umum: ["Sigar jalak", "Trembilutan"],
    status: "Tanaman pembanding",
    informasi: "Sigar jalak adalah tanaman perdu atau pohon kecil yang banyak digunakan sebagai tanaman pagar.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Gardenia jasminoides": {
    nama_umum: ["Kaca piring", "Melati tanjung"],
    status: "Tanaman pembanding",
    informasi: "Kaca piring adalah tanaman perdu tropis berbunga putih dan beraroma harum lembut.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Leucaena leucocephala": {
    nama_umum: ["Lamtoro", "Petai cina"],
    status: "Tanaman pembanding",
    informasi: "Lamtoro atau petai cina adalah perdu polong-polongan yang digunakan sebagai peneduh, pagar hidup, dan pakan ternak.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Moringa oleifera": {
    nama_umum: ["Kelor", "Merunggai"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Daun kelor memiliki efek hipoglikemik yang membantu menurunkan kadar gula darah dengan meningkatkan sensitivitas insulin dan mengurangi penyerapan glukosa di usus.",
    tautan_artikel: "https://hellosehat.com/diabetes/tipe-2/manfaat-daun-kelor-untuk-diabetes/",
    tautan_jurnal: "https://doi.org/10.35617/jfionline.v12i1.21",
    cara_mengolah: [
      "Siapkan segenggam daun kelor (10-15 gram) dan 600 ml air.",
      "Cuci bersih daun kelor di bawah air mengalir.",
      "Panaskan air hingga mendidih, lalu masukkan daun kelor dan rebus 5-15 menit.",
      "Saring air rebusan untuk diminum. Daun rebusan tetap bisa dikonsumsi sebagai lalapan."
    ],
    catatan: "Mengonsumsi dalam jumlah wajar. Jika memiliki kondisi medis tertentu, konsultasikan dengan dokter."
  },
  "Orthosiphon aristatus": {
    nama_umum: ["Kumis kucing", "Remujung"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Daun kumis kucing kaya flavonoid dan saponin. Flavonoid menghambat pemecahan karbohidrat di usus, sedangkan saponin merangsang pelepasan insulin.",
    tautan_artikel: "https://hellosehat.com/herbal-alternatif/herbal/tanaman-kumis-kucing/",
    tautan_jurnal: "https://doi.org/10.36990/hijp.v7i1.533",
    cara_mengolah: [
      "Siapkan segenggam daun kumis kucing (10-15 gram) dan 500 ml air.",
      "Cuci bersih di bawah air mengalir.",
      "Rebus selama 15-20 menit.",
      "Saring air rebusan dan minum 2-3 kali sehari."
    ],
    catatan: "Gunakan dalam jumlah wajar dan konsultasikan ke dokter untuk pemakaian jangka panjang."
  },
  "Pandanus amaryllifolius": {
    nama_umum: ["Pandan wangi", "Pandan"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Daun pandan mengandung flavonoid, tanin, dan polifenol yang mampu merangsang produksi hormon insulin dari sel beta pankreas.",
    tautan_artikel: "https://share.google/BTrQ3MBtqbTndrJvO",
    tautan_jurnal: "https://ejurnalmalahayati.ac.id/index.php/kebidanan/article/view/3024/pdf",
    cara_mengolah: [
      "Siapkan 3-4 lembar daun pandan segar/kering dan 500 ml air.",
      "Cuci bersih dan potong menjadi beberapa bagian.",
      "Rebus dalam air mendidih selama 10-15 menit hingga air berwarna hijau kekuningan.",
      "Saring air rebusan dan minum hangat."
    ],
    catatan: "Hindari menambahkan gula pasir tinggi kalori; gunakan pemanis alami jika diperlukan."
  },
  "Phyllanthus amarus": {
    nama_umum: ["Meniran"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Meniran memiliki senyawa aktif yang memengaruhi metabolisme glukosa dan mendukung pengelolaan tingkat kadar gula darah secara berkelanjutan.",
    tautan_artikel: "https://www.halodoc.com/artikel/manfaat-pohon-meniran-jaga-imun-ginjal-sehat-alami",
    tautan_jurnal: "https://doi.org/10.36656/jpfh.v2i1.79",
    cara_mengolah: [
      "Siapkan segenggam daun meniran segar (10-15 gram) dan 3 gelas air.",
      "Cuci bersih di bawah air mengalir.",
      "Rebus hingga air menyusut sekitar 1 gelas.",
      "Saring dan konsumsi selagi hangat 1-2 kali sehari."
    ],
    catatan: "Konsultasikan dengan dokter jika sedang mengonsumsi obat-obatan medis rutin."
  },
  "Physalis angulata": {
    nama_umum: ["Ciplukan", "Ceplukan", "Cecendet"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Daun Ciplukan memiliki indeks glikemik rendah dan dapat meningkatkan sensitivitas atau produksi insulin dalam tubuh.",
    tautan_artikel: "https://www.halodoc.com/artikel/pohon-ciplukan-dan-khasiatnya-dari-diabetes-hingga-kanker",
    tautan_jurnal: "https://journal.ukmc.ac.id/index.php/joh/article/view/1141/1081",
    cara_mengolah: [
      "Siapkan 10-15 gram daun ciplukan segar dan 3 gelas air (600 ml).",
      "Cuci bersih daun di bawah air mengalir.",
      "Rebus dengan api sedang (hindari panci aluminium) hingga menyusut jadi 1 gelas.",
      "Saring dan minum 1-2 kali sehari."
    ],
    catatan: "Disarankan merebus dengan wadah stainless steel atau enamel."
  },
  "Rosa sp.": {
    nama_umum: ["Mawar"],
    status: "Tanaman pembanding",
    informasi: "Mawar adalah tumbuhan perdu berkayu dan berduri yang terkenal sebagai tanaman hias populer.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Solanum nigrum": {
    nama_umum: ["Ranti", "Leunca"],
    status: "Tanaman pembanding",
    informasi: "Ranti adalah tanaman suku terung-terungan yang sering dikonsumsi sebagai lalapan atau bahan masakan.",
    tautan_artikel: "",
    tautan_jurnal: "",
    cara_mengolah: [],
    catatan: "Tanaman ini <strong>bukan</strong> merupakan tanaman herbal antidiabetes."
  },
  "Syzygium polyanthum": {
    nama_umum: ["Salam", "Manting", "Ubar serai"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Daun salam mengandung flavonoid, tanin, dan polifenol yang meningkatkan kerja insulin serta menghambat penyerapan gula di usus.",
    tautan_artikel: "https://www.halodoc.com/artikel/daun-salam-khasiat-dan-cara-konsumsi-sehat",
    tautan_jurnal: "https://doi.org/10.3164/jcbn.08-188",
    cara_mengolah: [
      "Siapkan 10-15 lembar daun salam segar dan 600 ml air (3 gelas).",
      "Cuci bersih daun salam.",
      "Rebus dengan api sedang sampai menyusut menjadi 1 gelas (200 ml).",
      "Saring dan minum hangat 2 kali sehari sebelum makan."
    ],
    catatan: "Gunakan wadah perebus yang tidak reaktif terhadap logam."
  },
  "Vernonia amygdalina": {
    nama_umum: ["Daun Afrika", "Daun pahit", "Daun insulin"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Ekstrak daun Afrika mengandung saponin, tanin, flavonoid, dan alkaloid yang terbukti efektif menekan lonjakan glukosa darah pasca makan.",
    tautan_artikel: "https://hellosehat.com/herbal-alternatif/herbal/manfaat-daun-afrika/",
    tautan_jurnal: "https://www.neliti.com/id/publications/460123/potensi-daun-afrika-vernonia-amygdalina-sebagai-antidiabetik",
    cara_mengolah: [
      "Siapkan 5-10 lembar daun Afrika dan 4 gelas air.",
      "Cuci bersih di bawah air mengalir.",
      "Rebus selama 10-15 menit hingga tersisa 2 gelas.",
      "Minum pagi dan sore hari. Dapat ditambahkan sedikit perasan jeruk nipis."
    ],
    catatan: "Minum secara teratur dalam dosis aman."
  },
  "Ziziphus mauritiana": {
    nama_umum: ["Bidara", "Widara", "Bukol"],
    status: "Tanaman herbal antidiabetes",
    informasi: "Kandungan saponin dan flavonoid dalam daun bidara berfungsi sebagai antioksidan kuat untuk meningkatkan efektivitas kerja hormon insulin.",
    tautan_artikel: "https://hellosehat.com/herbal-alternatif/herbal/daun-bidara/",
    tautan_jurnal: "https://doi.org/10.26740/icaj.v6i2.32598",
    cara_mengolah: [
      "Siapkan 10 lembar daun bidara tua, 1/2 buah jeruk nipis, dan 600 ml air.",
      "Cuci bersih daun bidara.",
      "Rebus air hingga mendidih, masukkan daun bidara dan masak 20 menit dengan api kecil.",
      "Tambahkan perasan jeruk nipis dan nikmati selagi hangat."
    ],
    catatan: "Jeruk nipis membantu menambah rasa segar sekaligus mempermudah ekstraksi senyawa aktif."
  }
};

// Map alternate key names
const getHerbData = (name: string): HerbDetail | undefined => {
  if (!name) return undefined;
  if (herbalInfo[name]) return herbalInfo[name];
  if (name === "Phyllanthus niruri") return herbalInfo["Phyllanthus amarus"];
  if (name === "Rosa sp") return herbalInfo["Rosa sp."];
  const clean = name.replace(/\.$/, "");
  if (herbalInfo[clean]) return herbalInfo[clean];
  const withDot = clean + ".";
  if (herbalInfo[withDot]) return herbalInfo[withDot];
  return undefined;
};

interface Prediction {
  label: string;
  score: number;
}

export default function App() {
  const [page, setPage] = useState<"upload" | "result">("upload");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [error, setError] = useState<string | null>(null);

  // File selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith("image/")) {
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        setError(null);
      } else {
        setError("Silakan pilih file foto daun (JPG, PNG, WEBP).");
      }
    }
  };

  const handleExampleSelect = async (path: string) => {
    try {
      setIsProcessing(true);
      setError(null);
      const res = await fetch(path);
      const blob = await res.blob();
      const file = new File([blob], path.split("/").pop() || "sample.jpg", { type: "image/jpeg" });
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setIsProcessing(false);
    } catch (err) {
      console.error(err);
      setError("Gagal memuat contoh gambar sampel.");
      setIsProcessing(false);
    }
  };

  // Run identification
  const handleIdentify = async () => {
    if (!selectedFile) {
      setError("Silakan pilih atau unggah gambar daun terlebih dahulu.");
      return;
    }

    setIsProcessing(true);
    setError(null);

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Gagal mengidentifikasi gambar. Pastikan server aktif.");
      }

      const data = await res.json();
      if (data.predictions && data.predictions.length > 0) {
        setPredictions(data.predictions);
        setPage("result");
      } else {
        throw new Error("Tidak ada hasil prediksi yang valid.");
      }
    } catch (err: any) {
      setError(err.message || "Terjadi kesalahan saat menghubungi server.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGoBack = () => {
    setPage("upload");
    setPredictions([]);
    setError(null);
  };

  const topPrediction = predictions[0];
  const topHerb = topPrediction ? getHerbData(topPrediction.label) : undefined;
  const isAntidiabetic = topHerb?.status === "Tanaman herbal antidiabetes";

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f2f7f4] via-[#ecf3ee] to-[#e6efe9] text-slate-800 font-sans selection:bg-[#0d9488]/20 selection:text-[#064e3b]">
      {/* HEADER COMPONENT */}
      <header className="border-b border-emerald-900/10 bg-white/90 backdrop-blur-md sticky top-0 z-50 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img 
              src="/images/diaherb_logo.png" 
              alt="DiaHerb Logo" 
              className="h-14 w-auto object-contain" 
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />
            <div className="flex flex-col">
              <span className="text-2xl font-bold font-serif text-[#065f46] flex items-center gap-1.5">
                DiaHerb <Leaf className="h-5 w-5 text-[#0d9488] fill-current" />
              </span>
              <span className="text-xs text-slate-500 font-medium hidden sm:inline-block">
                Sistem Identifikasi Daun Herbal Antidiabetes Berbasis LeafNet
              </span>
            </div>
          </div>
          <div className="text-xs font-semibold text-[#047857] bg-[#ecfdf5] border border-[#a7f3d0] px-3.5 py-1.5 rounded-lg shadow-2xs">
            LeafNet Dual-Branch Model • Tugas Akhir 211401034
          </div>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        {page === "upload" ? (
          <div>
            {/* HERO BANNER */}
            <div className="bg-gradient-to-r from-[#064e3b] to-[#0d9488] p-8 md:p-10 rounded-2xl text-white shadow-lg mb-8">
              <span className="bg-white/20 backdrop-blur-xs px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase text-white inline-block mb-3">
                MODEL LEAFNET DUAL-BRANCH
              </span>
              <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3 text-[#f0fdf4]">
                Sistem Identifikasi Daun Herbal Antidiabetes
              </h1>
              <p className="text-sm md:text-base leading-relaxed text-slate-100 max-w-4xl">
                DiaHerb dikembangkan untuk mengidentifikasi spesies tanaman herbal antidiabetes berdasarkan citra daun. 
                Sistem ini memanfaatkan kecerdasan buatan <b>Deep Learning LeafNet</b> yang menggabungkan ekstraksi jaringan tulang daun (<i>Vein Branch</i>) dan fitur visual warna (<i>RGB Branch</i> dengan DenseNet201).
              </p>
            </div>

            {/* TWO-COLUMN LAYOUT */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* UPLOAD COLUMN (LEFT) */}
              <div className="lg:col-span-7 bg-white/95 backdrop-blur-xs border border-emerald-900/10 rounded-2xl p-6 shadow-sm space-y-6">
                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  📷 Unggah Citra Daun
                </h3>

                <div 
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  className="aspect-square sm:aspect-[4/3] max-w-md mx-auto border-2 border-dashed border-[#0d9488]/40 hover:border-[#065f46] rounded-2xl p-6 text-center transition-all cursor-pointer relative bg-emerald-50/20 hover:bg-emerald-50/40 flex flex-col items-center justify-center space-y-4 shadow-2xs group overflow-hidden"
                >
                  <input 
                    type="file" 
                    id="file-upload" 
                    accept="image/*" 
                    className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                    onChange={handleFileChange}
                    disabled={isProcessing}
                  />

                  <div className="p-5 bg-white border border-emerald-100 rounded-2xl shadow-xs text-[#065f46] group-hover:scale-105 transition-transform">
                    <Upload className="h-10 w-10 text-[#065f46]" />
                  </div>
                  <div className="space-y-1.5 px-4">
                    <p className="text-base font-bold text-slate-800">
                      Pilih file foto daun (JPG, PNG, WEBP)
                    </p>
                    <p className="text-xs text-slate-500 max-w-xs mx-auto leading-relaxed">
                      Klik atau seret foto daun ke dalam kotak ini. Diutamakan foto 1 helai daun dengan latar belakang polos terang/putih.
                    </p>
                  </div>
                  <div className="pt-2">
                    <span className="inline-block px-4 py-1.5 bg-[#ecfdf5] border border-[#a7f3d0] text-[#065f46] rounded-full text-xs font-bold">
                      Buka Galeri / Kamera
                    </span>
                  </div>
                </div>

                {error && (
                  <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-800 text-sm font-medium flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-amber-600 shrink-0" />
                    <span>{error}</span>
                  </div>
                )}

                {previewUrl && (
                  <div className="text-center space-y-2 pt-2">
                    <img 
                      src={previewUrl} 
                      alt="Preview Gambar yang Diunggah" 
                      className="max-h-64 md:max-h-72 w-auto mx-auto rounded-xl border border-slate-200 object-contain shadow-2xs"
                    />
                    <p className="text-xs text-slate-400 italic font-medium">
                      Preview Gambar yang Diunggah
                    </p>
                  </div>
                )}

                {selectedFile && (
                  <p className="text-xs text-slate-500 truncate font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-200/80 text-center">
                    File terpilih: {selectedFile.name}
                  </p>
                )}

                <div className="pt-1">
                  <button
                    onClick={handleIdentify}
                    disabled={isProcessing || !selectedFile}
                    className="w-full py-3.5 px-6 rounded-xl bg-[#065f46] hover:bg-[#044e39] active:bg-[#033b2b] text-white font-bold flex items-center justify-center gap-2 shadow-md transition-all disabled:opacity-50 cursor-pointer"
                  >
                    {isProcessing ? (
                      <>
                        <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Menganalisis Citra...
                      </>
                    ) : (
                      <>
                        🔍 Identifikasi Daun Sekarang
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* TIPS & EXAMPLES COLUMN (RIGHT) */}
              <div className="lg:col-span-5 bg-white border border-emerald-900/10 rounded-2xl p-6 shadow-xs space-y-6">
                <div>
                  <h4 className="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
                    📌 Tips Pengambilan Gambar
                  </h4>
                  <ul className="text-xs md:text-sm text-slate-600 space-y-2 pl-4 list-disc leading-relaxed">
                    <li>Foto <b>1 helai daun</b> saja.</li>
                    <li>Pastikan helai daun berada tepat di tengah frame kamera.</li>
                    <li>Pencahayaan terang agar struktur urat/venasi daun terlihat jelas.</li>
                    <li><b>Latar belakang wajib polos</b> dan berwarna terang (diutamakan putih).</li>
                    <li>Foto diambil dari sisi atas atau bawah tegak lurus.</li>
                  </ul>
                </div>

                <hr className="border-slate-100" />

                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                      Contoh Sampel yang Baik:
                    </h4>
                    <span className="text-[10px] font-semibold text-[#065f46] bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      Klik untuk mencoba
                    </span>
                  </div>
                  <div className="grid grid-cols-4 gap-2.5">
                    {[
                      { path: "/images/IMG_20251028_152831.jpg", title: "Sampel 1" },
                      { path: "/images/IMG_20251029_170845.jpg", title: "Sampel 2" },
                      { path: "/images/IMG_20251031_131056.jpg", title: "Sampel 3" },
                      { path: "/images/IMG_20251114_161441.jpg", title: "Sampel 4" }
                    ].map((sample, idx) => (
                      <div 
                        key={idx}
                        onClick={() => handleExampleSelect(sample.path)}
                        className="group relative aspect-square rounded-xl overflow-hidden border border-slate-200 cursor-pointer hover:border-[#065f46] hover:shadow-xs transition-all bg-white"
                        title="Klik untuk memilih sampel ini"
                      >
                        <img 
                          src={sample.path} 
                          alt={sample.title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                        />
                        <div className="absolute inset-0 bg-[#065f46]/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                          <span className="text-[9px] text-white font-bold bg-[#065f46] px-1.5 py-0.5 rounded-md shadow-xs">
                            Pilih
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* RESULT PAGE */
          <div className="space-y-8">
            {/* PAGE TITLE */}
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-center text-[#064e3b]">
              Hasil Identifikasi Daun
            </h2>

            {/* TOP RESULTS SECTION (2 COLUMNS - EQUAL RATIO 2:2 / 50:50) */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
              {/* LEFT COLUMN: UPLOADED IMAGE, SCIENTIFIC NAME & GANTI GAMBAR BUTTON */}
              <div className="lg:col-span-1 space-y-6">
                {/* OUTER BORDER CARD */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs text-center flex flex-col items-center justify-center">
                  {/* INNER LEAF IMAGE BOX */}
                  <div className="w-full bg-slate-50 border border-slate-200/80 rounded-xl p-5 flex items-center justify-center min-h-[320px] md:min-h-[350px]">
                    {previewUrl && (
                      <img 
                        src={previewUrl} 
                        alt="Gambar yang Diunggah" 
                        className="max-h-72 md:max-h-84 w-auto max-w-full rounded-lg object-contain shadow-2xs"
                      />
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-3.5 italic font-medium">
                    Gambar yang Diunggah
                  </p>
                </div>

                {topHerb && (
                  <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                    <div>
                      <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
                        Nama Ilmiah:
                      </span>
                      <div className="font-serif italic text-3xl md:text-4xl font-bold text-[#064e3b] mt-1">
                        {topPrediction?.label}
                      </div>
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
                        Nama Umum:
                      </span>
                      <ul className="list-disc list-inside text-sm text-slate-700 mt-1 space-y-1 font-medium">
                        {topHerb.nama_umum.map((nm, idx) => (
                          <li key={idx}>{nm}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {/* BUTTON GANTI GAMBAR (ALIGNED WITH LEFT COLUMN / LEAF VIEW BOX) */}
                <button 
                  onClick={handleGoBack}
                  className="w-full py-3 px-5 rounded-xl bg-white border-2 border-[#065f46] text-[#065f46] hover:bg-[#065f46] hover:text-white font-bold text-sm shadow-xs transition-all cursor-pointer flex items-center justify-center gap-2 group"
                >
                  <RotateCcw className="h-4 w-4 transition-transform group-hover:-rotate-90" />
                  🔄 Ganti Gambar
                </button>
              </div>

              {/* RIGHT COLUMN: STATUS & TOP-5 PREDICTIONS (50/50 EQUAL RATIO) */}
              <div className="lg:col-span-1 space-y-6">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      STATUS TANAMAN:
                    </span>
                    <span className={isAntidiabetic ? "bg-[#d1fae5] text-[#065f46] border border-[#a7f3d0] px-3 py-1 rounded-full text-xs font-bold" : "bg-[#f1f5f9] text-[#334155] border border-[#cbd5e1] px-3 py-1 rounded-full text-xs font-bold"}>
                      {topHerb?.status || "Tanaman Pembanding"}
                    </span>
                  </div>
                  <hr className="border-slate-100" />
                  <div className="flex justify-between items-baseline">
                    <span className="text-xs font-semibold text-slate-500">
                      Kepercayaan Sistem:
                    </span>
                    <span className="text-2xl font-extrabold font-mono text-[#047857]">
                      {((topPrediction?.score || 0) * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                  <span className="text-sm font-bold text-slate-900 block">
                    Top-5 Prediksi Model:
                  </span>
                  <div className="space-y-3">
                    {predictions.map((pred, idx) => (
                      <div key={idx} className="space-y-1 text-xs md:text-sm">
                        <div className="flex justify-between items-center font-medium">
                          <span><b>{idx + 1}.</b> <i className="font-serif">{pred.label}</i></span>
                          <code className="text-[#047857] font-bold">{(pred.score * 100).toFixed(2)}%</code>
                        </div>
                        <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                          <div 
                            className="bg-[#047857] h-full rounded-full transition-all duration-500"
                            style={{ width: `${pred.score * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* HERBAL DETAILS SECTION */}
            <hr className="border-slate-200" />

            <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-xs space-y-6">
              <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2 border-b border-slate-100 pb-4">
                🌿 Informasi Herbal
              </h3>
              <p className="text-sm md:text-base text-slate-700 leading-relaxed">
                {topHerb?.informasi || "Tidak ada informasi khusus."}
              </p>

              {/* ARTICLES & JOURNALS LINKS GRID */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                <div>
                  <h4 className="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                    🔗 Tautan Artikel Terkait
                  </h4>
                  {topHerb?.tautan_artikel ? (
                    <a 
                      href={topHerb.tautan_artikel} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-[#065f46] font-medium hover:underline break-all inline-flex items-center gap-1"
                    >
                      {topHerb.tautan_artikel} <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  ) : (
                    <p className="text-xs text-slate-400 italic bg-slate-50 p-3 rounded-lg border border-slate-100">
                      Tidak tersedia artikel khusus untuk tanaman ini.
                    </p>
                  )}
                </div>

                <div>
                  <h4 className="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                    📚 Tautan Jurnal Penelitian
                  </h4>
                  {topHerb?.tautan_jurnal ? (
                    <a 
                      href={topHerb.tautan_jurnal} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-[#065f46] font-medium hover:underline break-all inline-flex items-center gap-1"
                    >
                      {topHerb.tautan_jurnal} <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  ) : (
                    <p className="text-xs text-slate-400 italic bg-slate-50 p-3 rounded-lg border border-slate-100">
                      Tidak tersedia jurnal khusus untuk tanaman ini.
                    </p>
                  )}
                </div>
              </div>

              {/* PREPARATION STEPS */}
              <div className="pt-2">
                <h4 className="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
                  ☕ Cara Mengolah Herbal Antidiabetes
                </h4>
                {topHerb && topHerb.cara_mengolah.length > 0 ? (
                  <ol className="list-decimal list-inside text-sm text-slate-700 space-y-2 pl-2">
                    {topHerb.cara_mengolah.map((step, idx) => (
                      <li key={idx} className="leading-relaxed"><b>{step}</b></li>
                    ))}
                  </ol>
                ) : (
                  <p className="text-xs text-slate-500 italic">
                    *(Tanaman ini merupakan tanaman pembanding dan tidak memiliki tata cara pengolahan ramuan antidiabetes).*
                  </p>
                )}
              </div>

              {/* SPECIAL NOTES */}
              {topHerb?.catatan && (
                <div className="pt-2">
                  <h4 className="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
                    ⚠️ Catatan Penting
                  </h4>
                  <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-xs md:text-sm leading-relaxed flex items-start gap-2">
                    <span className="text-base">💡</span>
                    <div dangerouslySetInnerHTML={{ __html: topHerb.catatan }} />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* DISCLAIMER BOX */}
        <div className="mt-10 p-5 bg-[#fffbeb] border border-[#fde68a] rounded-2xl text-[#78350f] text-xs md:text-sm leading-relaxed shadow-2xs">
          <b>Catatan Penafian / <i>Disclaimer Notice</i>:</b><br />
          <i>Sistem ini dikembangkan sebagai bagian dari penyusunan tugas akhir skripsi (NIM 211401034). 
          Hasil prediksi bersifat estimasi kecerdasan buatan (computer vision) dan tidak dimaksudkan sebagai rujukan medis atau botani yang bersifat final. 
          Validasi tetap disarankan melalui dokter atau ahli farmakognosi terkait.</i>
        </div>

        {/* FOOTER */}
        <footer className="text-center text-slate-500 text-xs font-semibold pt-6 border-t border-slate-200 mt-10">
          ©2026 DiaHerb | Tugas Akhir Skripsi | NIM 211401034
        </footer>
      </main>
    </div>
  );
}
