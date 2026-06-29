export function validateCategoryPayload(rawPayload) {
    const errors = [];

    const name = String(rawPayload.name || "").trim();
    const description = String(rawPayload.description || "").trim();

    if (!name || name.length < 1 || name.length > 120) {
        errors.push("Category name must be between 1 and 120 characters.");
    }

    if (description.length > 255) {
        errors.push("Description cannot exceed 255 characters.");
    }

    return {
        isValid: errors.length === 0,
        errors,
        payload: {
            name,
            description: description || null,
        },
    };
}

export function formatFastApiValidation(details) {
    if (!Array.isArray(details)) {
        return [];
    }

    return details.map((error) => {
        const path = Array.isArray(error.loc) ? error.loc.slice(1).join(".") : "field";
        return `${path}: ${error.msg}`;
    });
}
