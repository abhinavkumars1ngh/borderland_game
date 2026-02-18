const stickers = ["🔥", "💀", "🎴", "⚡", "👑", "🎲"];

function spawnSticker() {
    const s = document.createElement("div");
    s.className = "sticker";
    s.innerText = stickers[Math.floor(Math.random() * stickers.length)];

    s.style.left = Math.random() * window.innerWidth + "px";
    s.style.animationDuration = (4 + Math.random() * 4) + "s";

    document.body.appendChild(s);

    setTimeout(() => s.remove(), 8000);
}


setInterval(spawnSticker, 800);