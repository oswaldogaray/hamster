function toNumber(value) {
    const num = Number(value);
    return Number.isFinite(num) ? num : NaN;
}

export function validateProductPayload(rawPayload) {
    const errors = [];

    const name = String(rawPayload.name || "").trim();
    const sku = String(rawPayload.sku || "").trim();
    const categoryId = Number(rawPayload.category_id);
    const stockQuantity = toNumber(rawPayload.stock_quantity);
    const cost = toNumber(rawPayload.cost);
    const salePrice = toNumber(rawPayload.sale_price);

    if (!name || name.length < 1 || name.length > 150) {
        errors.push("Product name must be between 1 and 150 characters.");
    }

    if (!sku || sku.length < 1 || sku.length > 64) {
        errors.push("SKU must be between 1 and 64 characters.");
    }

    if (!Number.isInteger(categoryId) || categoryId <= 0) {
        errors.push("Category is required.");
    }

    if (!Number.isInteger(stockQuantity) || stockQuantity < 0) {
        errors.push("Stock must be a non-negative integer.");
    }

    if (!Number.isFinite(cost) || cost < 0) {
        errors.push("Cost must be a non-negative number.");
    }

    if (!Number.isFinite(salePrice) || salePrice < 0) {
        errors.push("Sale price must be a non-negative number.");
    }

    const payload = {
        name,
        sku,
        category_id: categoryId,
        stock_quantity: stockQuantity,
        cost: cost.toFixed(2),
        sale_price: salePrice.toFixed(2),
    };

    return {
        isValid: errors.length === 0,
        errors,
        payload,
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
