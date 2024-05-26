export const capitalize = (string: string) => {
    return string[0].toUpperCase() + string.slice(1);
};

export const toTitleCase = (string: string): string => {
    return string.replace(/[A-Za-z]\w*?(?=[A-Z]|$)/gm, (match, ...args) => {
        const offsetIndex = typeof args.at(-1) === 'object' ? args.at(-3) : args.at(-2);
        return offsetIndex === 0 ? `${capitalize(match)}` : ` ${match}`;
    });
};

export const toKebabCase = (string: string): string => {
    return string.trim().replace(/\s+/gim, '-');
};

export function deeplyMerge(target, source) {
    if (!isObject(target)) {
        throw new TypeError("[deeplyMerge] : argument 'target' must be an object!");
    }
    if (!isObject(source)) {
        throw new TypeError("[deeplyMerge] : argument 'source' must be an object!");
    }

    for (const [sourceKey, sourceValue] of Object.entries(source)) {
        target[sourceKey] = handleAssignment({
            assignmentTarget: target[sourceKey],
            targetValue: sourceValue,
        });
    }

    return target;
}

function handleAssignment({ assignmentTarget, targetValue }) {
    return isObject(targetValue) // force formatting
        ? deeplyMerge(assignmentTarget || {}, targetValue)
        : targetValue;
}

export const isInvalidKey = (key: unknown) => typeof key !== 'string' || key === '';

export const isObject = (val: unknown) => typeof val === 'object' && val != null && !Array.isArray(val);
