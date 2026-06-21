document.addEventListener("DOMContentLoaded", function () {
  try {
    // Avoid duplicates on hot reload
    if (document.querySelector(".bottom-logo")) return;

    const container = document.createElement("div");
    container.className = "bottom-logo";

    const link = document.createElement("a");
    link.className = "bottom-logo-link";
    link.href = "https://ngkorefoundation.org";
    link.title = "NgKore Foundation";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", "NgKore website");

    const img = document.createElement("img");
    img.className = "bottom-logo-image";
    img.alt = "NgKore Foundation";
    img.loading = "lazy";
    img.decoding = "async";
    const contentRoot = document.body.getAttribute("data-content_root") || "/";
    img.src = contentRoot + "_static/ngkore-logo.png";
    img.onerror = function () {
      img.onerror = null;
      img.src = "/_static/ngkore-logo.png";
    };

    link.appendChild(img);
    container.appendChild(link);
    document.body.appendChild(container);
  } catch (e) {
    console.warn("Failed to attach bottom logo:", e);
  }
});
