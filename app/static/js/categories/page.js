import {
    ApiError,
    createCategory,
    deleteCategory,
    fetchCategories,
    fetchCategoryById,
    updateCategory,
} from "./api.js";
import { createCategoryModal } from "./modal.js";
import { createCategoriesState } from "./state.js";
import { clearError, renderCategories, showError } from "./ui.js";
import { formatFastApiValidation, validateCategoryPayload } from "./validation.js";

const state = createCategoriesState();
const modal = createCategoryModal();

const tableBody = document.getElementById("categories-table-body");
const searchInput = document.getElementById("category-search");
const errorBox = document.getElementById("categories-error");
const openModalButton = document.getElementById("open-category-modal");

let searchDebounceTimer;

function notify(type, message, duration = 3200) {
    window.showToast?.({ type, message, duration });
}

function applyFilter() {
    const query = (state.search || "").toLowerCase();
    state.filtered = state.all.filter((category) => {
        if (!query) {
            return true;
        }
        const name = String(category.name || "").toLowerCase();
        const description = String(category.description || "").toLowerCase();
        return name.includes(query) || description.includes(query);
    });
}

function renderList() {
    if (!tableBody) {
        return;
    }
    renderCategories(tableBody, state.filtered);
}

async function loadCategories() {
    if (!errorBox) {
        return;
    }

    try {
        clearError(errorBox);
        state.all = await fetchCategories();
        applyFilter();
        renderList();
    } catch (error) {
        showError(errorBox, error.message || "Unable to load categories.");
        notify("error", error.message || "Unable to load categories.");
    }
}

function openCreateModal() {
    modal.resetErrors();
    modal.setMode("create");
    modal.fillForm(null);
    modal.show();
}

async function openEditModal(categoryId) {
    try {
        modal.resetErrors();
        modal.setMode("edit");
        modal.setSubmitting(true);
        modal.show();

        const category = await fetchCategoryById(categoryId);
        modal.fillForm(category);
    } catch (error) {
        modal.hide();
        showError(errorBox, error.message || "Unable to load category details.");
    } finally {
        modal.setSubmitting(false);
    }
}

async function handleSubmitCategory(event) {
    event.preventDefault();
    modal.resetErrors();

    const rawPayload = modal.getRawValues();
    const validation = validateCategoryPayload(rawPayload);
    if (!validation.isValid) {
        modal.setErrorMessages(validation.errors);
        modal.markInvalidFields(validation.errors);
        notify("warning", "Please review category form fields.");
        return;
    }

    try {
        modal.setSubmitting(true);

        if (modal.getMode() === "edit") {
            await updateCategory(modal.getCategoryId(), validation.payload);
        } else {
            await createCategory(validation.payload);
        }

        modal.hide();
        await loadCategories();
        notify(
            "success",
            modal.getMode() === "edit" ? "Category updated successfully." : "Category created successfully."
        );
    } catch (error) {
        if (error instanceof ApiError) {
            const apiMessages = formatFastApiValidation(error.details);
            if (apiMessages.length) {
                modal.setErrorMessages(apiMessages);
                modal.markInvalidFields(apiMessages);
                notify("error", "Validation failed. Please check category details.");
            } else {
                modal.setErrorMessages([error.message]);
                notify("error", error.message);
            }
            return;
        }

        modal.setErrorMessages([error.message || "Unexpected error while saving category."]);
        notify("error", error.message || "Unexpected error while saving category.");
    } finally {
        modal.setSubmitting(false);
    }
}

function handleTableActions(event) {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
        return;
    }

    const button = target.closest("button[data-action]");
    if (!button) {
        return;
    }

    const categoryId = Number(button.dataset.id);
    const action = button.dataset.action;

    if (action === "edit") {
        openEditModal(categoryId);
        return;
    }

    if (action === "delete") {
        const categoryName = button.dataset.name || "this category";
        modal.askDelete(categoryId, categoryName);
    }
}

async function confirmDelete(categoryId) {
    if (!categoryId) {
        return;
    }

    try {
        await deleteCategory(categoryId);
        modal.hideConfirm();
        await loadCategories();
        notify("success", "Category deleted successfully.");
    } catch (error) {
        modal.hideConfirm();
        showError(errorBox, error.message || "Unable to delete category.");
        notify("error", error.message || "Unable to delete category.");
    }
}

function wireEvents() {
    openModalButton?.addEventListener("click", openCreateModal);

    searchInput?.addEventListener("input", () => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = window.setTimeout(() => {
            state.search = (searchInput.value || "").trim();
            applyFilter();
            renderList();
        }, 250);
    });

    tableBody?.addEventListener("click", handleTableActions);
    modal.form?.addEventListener("submit", handleSubmitCategory);
    modal.onConfirmDelete(confirmDelete);
}

wireEvents();
loadCategories();
