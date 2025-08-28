import express, { NextFunction, Request, Response } from 'express';

import { baseRequestURL } from 'server/constants';
import { asyncWrapper } from 'server/utils';

const router = express.Router();

// const fetchHeaders = new Headers({
//     Accept: '*/*',
//     'Content-Type': 'application/json',
// });

// TODO: I _really_ need to DRY this whole thing up @_@

router.use(
    '/article-data/:stockSlug',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [article-data by stockSlug] '.padStart(120, '=').padEnd(240, '='));
        console.log({ url: req.url, params: req.params });

        const { stockSlug } = req.params;
        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/article-data/${stockSlug}`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[article-data by stock route] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({ articleDataBySlug: initialPageData.data, reqParams: req.params }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [article-data by stockSlug]': ", e);
            return next(e);
        }
    }),
);

router.use(
    '/article-data',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [article-data list] '.padStart(120, '=').padEnd(240, '='));
        console.log({ url: req.url, params: req.params });

        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/article-data`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[article-data list route] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({ articleData: initialPageData.data, reqParams: req.params }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [article-data list]': ", e);
            return next(e);
        }
    }),
);

router.use(
    '/sentiment-analyses/:stockSlug',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [sentiment-analyses by stockSlug] '.padStart(120, '=').padEnd(240, '='));
        console.log({ url: req.url, params: req.params });

        const { stockSlug } = req.params;
        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/sentiment-analyses/${stockSlug}`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[sentiment-analyses by stock route] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({
                    sentimentAnalysesBySlug: initialPageData.data,
                    reqParams: req.params,
                }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [sentiment-analyses by stockSlug]': ", e);
            return next(e);
        }
    }),
);

router.use(
    '/stocks/:stockSlug',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [single stock view] '.padStart(120, '=').padEnd(240, '='));
        console.log({ url: req.url, params: req.params });

        const { stockSlug } = req.params;
        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/stocks/${stockSlug}`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[data-explorers - single stock view] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({ stockDataSingular: initialPageData.data, reqParams: req.params }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [single stock view]': ", e);
            return next(e);
        }
    }),
);

router.use(
    '/stocks',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [stocks list] '.padStart(120, '=').padEnd(240, '='));
        console.log({ url: req.url, params: req.params });

        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/stocks`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[data-explorers - stocks list] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({ stockDataAll: initialPageData.data, reqParams: req.params }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [stocks list]': ", e);
            return next(e);
        }
    }),
);

router.use(
    '/',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        console.log(' data-explorers handler [explorers list] '.padStart(100, '=').padEnd(200, '='));
        console.log({ url: req.url, params: req.params });

        let initialPageData = {
            data: null,
        };

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/stocks`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });

            if (pageDataResponse.status >= 400) {
                const errorMessage = await pageDataResponse.text();
                throw new Error(errorMessage);
            }

            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[data-explorers - explorers list] - caught exception:`);
            console.warn(e);
        }

        if (res.locals.user != null) {
            Object.assign(initialPageData, {
                user: {
                    ...res.locals.user,
                },
            });
        }

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify({ stockDataAll: initialPageData.data, reqParams: req.params }),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['dataExplorers'],
            });
        } catch (e) {
            console.error("ERROR encountered in 'data-explorers handler [explorers list]': ", e);
            return next(e);
        }
    }),
);

// TODO: some generic router like this might be nice...?
// router.use(
//     '/:explorerType/:stockSlug',
//     asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
//         console.log(' data-explorers handler [generic] '.padStart(100, '=').padEnd(200, '='));
//         console.log({ url: req.url, params: req.params });

//         if (/^\/\S+/im.test(req.url)) {
//             return next();
//         }

//         let initialPageData = {
//             data: null,
//         };

//         try {
//             // TODO: add some user-specific thing to request?
//             const pageDataResponse = await global.fetch(`${baseRequestURL}/api/article-data`);

//             if (pageDataResponse.status >= 400) {
//                 const errorMessage = await pageDataResponse.text();
//                 throw new Error(errorMessage);
//             }

//             initialPageData = await pageDataResponse.json();
//         } catch (e) {
//             console.warn(`[data-explorers route] - caught exception: ${e}`);
//         }

//         console.log(
//             '\n'.padStart(220, '='),
//             'data-explorers router: ',
//             { localsManifest: res.locals.manifest },
//             '\n'.padEnd(220, '='),
//         );

//         try {
//             return res.render('index', {
//                 layout: 'index',
//                 initialPageData: JSON.stringify({ articleData: initialPageData.data, reqParams: req.params }),
//                 ...res.locals.manifest['common'],
//                 ...res.locals.manifest['dataExplorers'],
//             });
//         } catch (e) {
//             return next(e);
//         }
//     }),
// );

export default router;
