import { useEffect, useRef } from 'react';

/**
 * @function usePrevious
 * @description Custom hook for getting previous value of some variable
 */
export function usePrevious(value) {
    const ref = useRef();

    useEffect(() => {
        ref.current = value;
    }, [value]);

    return ref.current;
}
