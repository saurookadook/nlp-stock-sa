import { usePrevious } from 'client/common/utils/hooks';
import renderWithContext from 'client/common/utils/renderWithContext';

const capitalize = (string: string) => {
    return string[0].toUpperCase() + string.slice(1);
};

const toTitleCase = (string: string): string => {
    return string.replace(/[A-Za-z]\w*?(?=[A-Z]|$)/gm, (match, ...args) => {
        const offsetIndex = typeof args.at(-1) === 'object' ? args.at(-3) : args.at(-2);
        return offsetIndex === 0 ? `${capitalize(match)}` : ` ${match}`;
    });
};

const toKebabCase = (string: string): string => {
    return string.trim().replace(/\s+/gim, '-');
};

function deeplyMerge(target, source) {
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

const isInvalidKey = (key: unknown) => typeof key !== 'string' || key === '';

const isObject = (val: unknown) => typeof val === 'object' && val != null && !Array.isArray(val);

export {
    capitalize, // force formatting
    deeplyMerge,
    isInvalidKey,
    renderWithContext,
    toTitleCase,
    toKebabCase,
    usePrevious,
};
