export function validateSaleInput({ customerName, paymentMethod, lines }) {
    const errors = [];

    if (!customerName || customerName.trim().length < 2) {
        errors.push("Customer name must contain at least 2 characters.");
    }

    if (!paymentMethod) {
        errors.push("Payment method is required.");
    }

    if (!Array.isArray(lines) || lines.length === 0) {
        errors.push("Add at least one product line before submitting the sale.");
    }

    return {
        isValid: errors.length === 0,
        errors,
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
