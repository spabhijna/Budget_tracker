document.addEventListener("DOMContentLoaded", () => {
    const modeToggle = document.getElementById("mode-toggle");

    modeToggle.addEventListener("click", () => {
        const body = document.body;
        body.classList.toggle("dark-mode");
        body.classList.toggle("light-mode");

        const mode = body.classList.contains("dark-mode") ? "dark" : "light";
        localStorage.setItem("theme", mode);
    });

    const savedMode = localStorage.getItem("theme") || "light";
    document.body.classList.add(savedMode + "-mode");
});
