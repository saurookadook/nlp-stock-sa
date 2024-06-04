/**
 * jest-dom adds custom jest matchers for asserting on DOM nodes.
 * allows you to do things like:
 * expect(element).toHaveTextContent(/react/i)
 * learn more: https://github.com/testing-library/jest-dom
 */
import '@testing-library/jest-dom';
/**
 * more on node-fetch and fetch polyfills
 * - {@link https://npmtrends.com/isomorphic-fetch-vs-isomorphic-unfetch-vs-node-fetch-vs-whatwg-fetch|isomorphic-fetch-vs-isomorphic-unfetch-vs-node-fetch-vs-whatwg-fetch}
 * - {@link https://github.com/node-fetch/node-fetch|node-fetch}
 * - {@link https://github.com/JakeChampion/fetch|whatwg-fetch}
 */
// import fetch from 'node-fetch';
import 'whatwg-fetch';

if (typeof window !== 'undefined') {
    window.matchMedia = jest.fn().mockImplementation((query) => {
        // TODO: maybe fully implement some of these methods?
        return {
            matches: false,
            media: query,
            onchange: null,
            addListener: jest.fn(), // deprecated
            removeListener: jest.fn(), // deprecated
            addEventListener: jest.fn(),
            removeEventListener: jest.fn(),
            dispatchEvent: jest.fn(),
        };
    });
}
