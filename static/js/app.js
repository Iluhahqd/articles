document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.classList.add("fade");
        }, 3500);
    });

    const revealItems = document.querySelectorAll("[data-reveal]");
    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        revealObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );
        revealItems.forEach((item) => revealObserver.observe(item));
    } else {
        revealItems.forEach((item) => item.classList.add("is-visible"));
    }

    const progressBar = document.getElementById("reading-progress");
    const backToTop = document.getElementById("back-to-top");

    const updateScrollUi = () => {
        const scrollTop = window.scrollY;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        if (backToTop) {
            backToTop.classList.toggle("is-visible", scrollTop > 320);
        }
    };

    updateScrollUi();
    window.addEventListener("scroll", updateScrollUi, { passive: true });

    if (backToTop) {
        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    document.querySelectorAll("[data-copy-link]").forEach((button) => {
        button.addEventListener("click", async () => {
            const link = button.dataset.copyValue || window.location.href;
            try {
                await navigator.clipboard.writeText(link);
                const originalText = button.textContent;
                button.textContent = "Ссылка скопирована";
                setTimeout(() => {
                    button.textContent = originalText;
                }, 1800);
            } catch (error) {
                console.error(error);
            }
        });
    });
});
