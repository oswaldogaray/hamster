(() => {
    const TOAST_TYPES = {
        success: {
            icon: "M9 12.75l2.25 2.25L15 9.75",
            classes: "border-emerald-500/40 bg-emerald-500/15 text-emerald-100",
        },
        error: {
            icon: "M12 9v3.75m0 3h.008v.008H12v-.008z",
            classes: "border-rose-500/40 bg-rose-500/15 text-rose-100",
        },
        warning: {
            icon: "M12 9v3.75m0 3h.008v.008H12v-.008z",
            classes: "border-amber-500/40 bg-amber-500/15 text-amber-100",
        },
        info: {
            icon: "M12 10.5h.008v.008H12v-.008zm0 2.25v3",
            classes: "border-cyan-500/40 bg-cyan-500/15 text-cyan-100",
        },
    };

    function getContainer() {
        return document.getElementById("toast-container");
    }

    function removeToast(toast, duration = 180) {
        toast.classList.add("opacity-0", "translate-y-2");
        window.setTimeout(() => {
            toast.remove();
        }, duration);
    }

    function createToastElement(type, message) {
        const config = TOAST_TYPES[type] || TOAST_TYPES.info;
        const toast = document.createElement("div");
        toast.className = `pointer-events-auto flex items-start gap-3 rounded-xl border px-3 py-3 shadow-soft transition-all duration-200 opacity-0 -translate-y-2 ${config.classes}`;

        toast.innerHTML = `
            <span class="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-slate-950/40">
                <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="${config.icon}" />
                </svg>
            </span>
            <p class="flex-1 text-sm leading-5">${message}</p>
            <button type="button" class="rounded-md p-1 text-current/80 transition hover:bg-slate-950/20 hover:text-current" aria-label="Close notification">
                <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        `;

        const closeButton = toast.querySelector("button");
        closeButton?.addEventListener("click", () => removeToast(toast));

        return toast;
    }

    function showToast({ type = "info", message = "Notification", duration = 3500 } = {}) {
        const container = getContainer();
        if (!container) {
            return;
        }

        const toast = createToastElement(type, message);
        container.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.remove("opacity-0", "-translate-y-2");
        });

        window.setTimeout(() => removeToast(toast), Math.max(duration, 1200));
    }

    window.showToast = showToast;
})();
