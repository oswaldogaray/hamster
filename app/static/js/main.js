document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const backdrop = document.getElementById("sidebar-backdrop");
    const openButton = document.getElementById("sidebar-open");
    const closeButton = document.getElementById("sidebar-close");
    const desktopToggle = document.getElementById("sidebar-toggle-desktop");
    const desktopToggleIcon = document.getElementById("sidebar-toggle-icon");
    const appShell = document.getElementById("app-shell");
    const sidebarTexts = document.querySelectorAll(".sidebar-text");
    const sidebarPills = document.querySelectorAll(".sidebar-pill");
    const sidebarPanel = document.querySelector(".sidebar-panel");

    if (!sidebar || !backdrop) {
        return;
    }

    const closeSidebar = () => {
        sidebar.classList.add("-translate-x-full");
        backdrop.classList.add("hidden");
    };

    const openSidebar = () => {
        sidebar.classList.remove("-translate-x-full");
        backdrop.classList.remove("hidden");
    };

    openButton?.addEventListener("click", openSidebar);
    closeButton?.addEventListener("click", closeSidebar);
    backdrop.addEventListener("click", closeSidebar);

    desktopToggle?.addEventListener("click", () => {
        if (!appShell) {
            return;
        }

        const isCollapsed = sidebar.classList.contains("md:w-20");
        if (isCollapsed) {
            sidebar.classList.remove("md:w-20");
            sidebar.classList.add("md:w-72");
            appShell.classList.remove("md:pl-20");
            appShell.classList.add("md:pl-72");
            sidebarTexts.forEach((el) => {
                el.classList.remove("md:opacity-0", "md:max-w-0", "md:-translate-x-2");
                el.classList.add("md:opacity-100", "md:max-w-[160px]", "md:translate-x-0");
            });
            sidebarPills.forEach((el) => el.classList.remove("md:hidden"));
            sidebarPanel?.classList.remove("md:opacity-0", "md:max-h-0", "md:overflow-hidden");
            desktopToggleIcon?.classList.remove("rotate-180");
        } else {
            sidebar.classList.remove("md:w-72");
            sidebar.classList.add("md:w-20");
            appShell.classList.remove("md:pl-72");
            appShell.classList.add("md:pl-20");
            sidebarTexts.forEach((el) => {
                el.classList.remove("md:opacity-100", "md:max-w-[160px]", "md:translate-x-0");
                el.classList.add("md:opacity-0", "md:max-w-0", "md:-translate-x-2");
            });
            sidebarPills.forEach((el) => el.classList.add("md:hidden"));
            sidebarPanel?.classList.add("md:opacity-0", "md:max-h-0", "md:overflow-hidden");
            desktopToggleIcon?.classList.add("rotate-180");
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth >= 768) {
            backdrop.classList.add("hidden");
            sidebar.classList.remove("-translate-x-full");
        } else {
            sidebar.classList.add("-translate-x-full");
        }
    });
});
