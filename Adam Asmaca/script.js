const kelimeler = [
    { kelime: "bilgisayar", kategori: "Teknoloji" },
    { kelime: "javascript", kategori: "Programlama" },
    { kelime: "algoritma", kategori: "Yazılım" },
    { kelime: "internet", kategori: "Bilişim" },
    { kelime: "veritabani", kategori: "Yazılım" },
    { kelime: "donanim", kategori: "Bilgisayar" },
    { kelime: "yazilim", kategori: "Teknoloji" },
    { kelime: "klavye", kategori: "Donanım" },
    { kelime: "monitor", kategori: "Donanım" },
    { kelime: "sunucu", kategori: "Bilişim" }
];

let oncekiKelime = null;

let kelime, kategori, gorunen;
let hata = 0;
let yanlislar = [];
const maxHata = 6;

const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");

ctx.lineWidth = 6;
ctx.strokeStyle = "#ffffff";
ctx.lineCap = "round";

function temizle() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function ciz() {
    temizle();

    ctx.beginPath();
    ctx.moveTo(60, 400);
    ctx.lineTo(300, 400);
    ctx.moveTo(120, 400);
    ctx.lineTo(120, 60);
    ctx.lineTo(240, 60);
    ctx.lineTo(240, 100);
    ctx.stroke();

    if (hata > 0) { ctx.beginPath(); ctx.arc(240, 140, 28, 0, Math.PI * 2); ctx.stroke(); }
    if (hata > 1) { ctx.beginPath(); ctx.moveTo(240, 170); ctx.lineTo(240, 260); ctx.stroke(); }
    if (hata > 2) { ctx.beginPath(); ctx.moveTo(240, 200); ctx.lineTo(200, 240); ctx.stroke(); }
    if (hata > 3) { ctx.beginPath(); ctx.moveTo(240, 200); ctx.lineTo(280, 240); ctx.stroke(); }
    if (hata > 4) { ctx.beginPath(); ctx.moveTo(240, 260); ctx.lineTo(210, 320); ctx.stroke(); }
    if (hata > 5) { ctx.beginPath(); ctx.moveTo(240, 260); ctx.lineTo(270, 320); ctx.stroke(); }
}

function rastgeleKelimeSec() {
    let secilen;
    do {
        secilen = kelimeler[Math.floor(Math.random() * kelimeler.length)];
    } while (secilen.kelime === oncekiKelime);

    oncekiKelime = secilen.kelime;
    return secilen;
}

function baslat() {
    const secilen = rastgeleKelimeSec();
    kelime = secilen.kelime;
    kategori = secilen.kategori;

    gorunen = Array(kelime.length).fill("_");
    hata = 0;
    yanlislar = [];

    document.getElementById("kategori").innerText = "Kategori: " + kategori;
    document.getElementById("kelime").innerText = gorunen.join(" ");
    document.getElementById("yanlislar").innerText = "";
    document.getElementById("bilgi").innerText = "";

    ciz();
}

function tahmin() {
    const input = document.getElementById("harf");
    const harf = input.value.toLowerCase();
    input.value = "";

    if (!harf || hata >= maxHata) return;

    if (kelime.includes(harf)) {
        for (let i = 0; i < kelime.length; i++) {
            if (kelime[i] === harf) gorunen[i] = harf;
        }
    } else {
        if (!yanlislar.includes(harf)) {
            yanlislar.push(harf);
            hata++;
        }
    }

    document.getElementById("kelime").innerText = gorunen.join(" ");
    document.getElementById("yanlislar").innerText = yanlislar.join(" ");
    ciz();

    if (!gorunen.includes("_")) {
        document.getElementById("bilgi").innerText = "🎉 Kazandın!";
    }
    if (hata === maxHata) {
        document.getElementById("bilgi").innerText =
            "💀 Kaybettin! Kelime: " + kelime;
    }
}

baslat();
