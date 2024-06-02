import https from 'https';
import http from 'http';

import { AmbiguousObject, NullableValue } from '@nlpssa-app-types/common/main';

type FetchyThis = {
    baseURL: string;
    headers: AmbiguousObject; // TODO
    httpAgent: NullableValue<http.Agent>;
    httpsAgent: NullableValue<https.Agent>;
    options: AmbiguousObject; // TODO
    privateSetBaseURL: (baseURL: string) => string;
};

interface Options extends RequestInit {
    agent: () => FetchyThis['httpAgent'] | FetchyThis['httpsAgent'];
    searchParams?: AmbiguousObject;
}

const fetchy = (function () {
    const _this: FetchyThis = {
        baseURL: '',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        },
        httpAgent: null,
        httpsAgent: null,
        options: {
            agent: null,
            searchParams: {},
        },
        privateSetBaseURL: function (baseURL: string) {
            if (baseURL == null || typeof baseURL !== 'string' || baseURL === '') {
                throw new TypeError("fetchy: argument 'baseURL' must be a non-empty string");
            }
            // TODO: should maybe parse 'baseURL' somehow to make sure it's URL safe?
            _this.baseURL = baseURL;

            return _this.baseURL;
        },
    };

    /**
     * @description Tests whether a given string is a valid, absolute URL by using parts 1-4
     * of the Regular Expression from {@link https://datatracker.ietf.org/doc/html/rfc3986#appendix-B|RFC 3986, Appendix B}
     */
    const isAbsoluteURL = (reqString: string): boolean => {
        return /^(([^:\/?#]+):)?(\/\/([^\/?#]*))?/im.test(reqString);
    };

    /**
     * @description Determines whether the current context is a browser by testing if
     *  the global `window` variable is defined
     */
    const isFrontend = (): boolean => typeof window !== 'undefined';

    const isHttps = (): boolean => _this.baseURL.includes('https');

    function appendSearchParamsToUrl(url: string, searchParams: NullableValue<AmbiguousObject>): string {
        if (searchParams == null || Object.keys(searchParams).length < 1) {
            return url;
        }

        let hasFirstParam = url.indexOf('?') === -1;

        return Object.entries(searchParams).reduce(function (finalUrl, paramEntry) {
            if (paramEntry[1] === '') {
                return finalUrl;
            }

            const [key, value] = paramEntry;

            if (!hasFirstParam) {
                finalUrl += `&${key}=${value}`;
            } else {
                finalUrl += `?${key}=${value}`;
                hasFirstParam = true;
            }

            return finalUrl;
        }, `${url}`);
    }

    async function doFetch(urlOrPath: string, options: AmbiguousObject = {}) {
        if (urlOrPath == null || typeof urlOrPath !== 'string' || urlOrPath === '') {
            throw new TypeError("fetchy: argument 'urlOrPath' must be a non-empty string");
        }

        if (isFrontend() && !_this.baseURL && !isAbsoluteURL(urlOrPath)) {
            _this.privateSetBaseURL(`${window.location.protocol}//${window.location.host}`);
        }

        // TODO: this feels... inefficient?
        const headersFromOptions = options.headers || {};
        delete options.headers;

        const combinedOptions: Options = {
            ..._this.options,
            ...options,
            agent: isHttps() ? () => _this.httpsAgent : () => _this.httpAgent,
            headers: new Headers({
                ..._this.headers,
                ...headersFromOptions,
            }),
        };

        const requestUrl = appendSearchParamsToUrl(
            urlOrPath,
            combinedOptions.searchParams as NullableValue<AmbiguousObject>,
        );

        // TODO: more to do here...?
        return $fetch(requestUrl, combinedOptions);
    }

    /**
     * @description Resolves and forwards arguments to correct `fetch` reference
     */
    const $fetch: Window['fetch'] = (...args) => (isFrontend() ? window.fetch(...args) : global.fetch(...args));

    function $doGET(urlOrPath: string, options = {}) {
        const getOptions = {
            ...options,
            method: 'GET',
        };
        return doFetch(urlOrPath, getOptions);
    }

    function $doPOST(urlOrPath: string, { bodyJson = {}, options = {} }) {
        const postOptions = {
            ...options,
            body: JSON.stringify(bodyJson),
            method: 'POST',
        };
        return doFetch(urlOrPath, postOptions);
    }

    function $doPUT(urlOrPath: string, { bodyJson = {}, options = {} }) {
        const putOptions = {
            ...options,
            body: JSON.stringify(bodyJson),
            method: 'PUT',
        };
        return doFetch(urlOrPath, putOptions);
    }

    function $addHeaders(headers: AmbiguousObject) {
        for (const [key, value] of Object.entries(headers)) {
            _this.headers[key] = value;
        }
        return _this.headers;
    }

    function $getHeaders() {
        return _this.headers;
    }

    function $getBaseURL(): string {
        return _this.baseURL;
    }

    function $setBaseURL(baseURL: string) {
        if (!_this.baseURL) {
            _this.baseURL = baseURL;
        }
        return _this.baseURL;
    }

    return {
        _fetch: $fetch,
        get: $doGET,
        post: $doPOST,
        put: $doPUT,
        // delete: $doDELETE,
        addHeaders: $addHeaders,
        getHeaders: $getHeaders,
        getBaseURL: $getBaseURL,
        setBaseURL: $setBaseURL,
    };
})();

export default fetchy;
