// Sticky demo helpers
const footerMode = document.getElementById("footerMode");
const footer = document.getElementById("footer");
const toTop = document.getElementById("toTop");

function setFooterMode(isFixed){
  footer.classList.toggle("is-fixed", isFixed);
  // fixed olunca içerik altta kapanmasın diye body padding-bottom ayarla
  document.body.style.paddingBottom = isFixed ? "54px" : "0px";
  const txt = document.querySelector(".toggle-text");
  if (txt) txt.textContent = isFixed ? "Footer: Fixed" : "Footer: Sticky";
}

footerMode.addEventListener("change", (e) => {
  setFooterMode(e.target.checked);
});

// yukarı butonu
window.addEventListener("scroll", () => {
  if (window.scrollY > 400) toTop.classList.add("show");
  else toTop.classList.remove("show");
});

toTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// default
setFooterMode(false);
