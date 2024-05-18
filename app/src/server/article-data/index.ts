import express, { NextFunction, Request, Response } from 'express';

import { manifestMiddleware } from 'server/middleware';
import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(manifestMiddleware);

router.use(
    '/{stockSlug}',
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        const { stockSlug } = req.params;

        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            // const pageDataResponse = await global.fetch(`https://nlp-ssa.dev/api/article-data/${stockSlug}`);
            const pageDataResponse = await global.fetch(`/api/article-data/${stockSlug}`);
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[article-data route] - caught exception: ${e}`);
        }

        // console.log(
        //     '\n'.padStart(220, '='),
        //     'article-data router: ',
        //     { localsManifest: res.locals.manifest },
        //     '\n'.padEnd(220, '='),
        // );

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify(initialPageData),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['article-data'],
            });
        } catch (e) {
            return next(e);
        }
    }),
);

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await global.fetch('https://nlp-ssa.dev/api/article-data');
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[article-data route] - caught exception: ${e}`);
        }

        // console.log(
        //     '\n'.padStart(220, '='),
        //     'article-data router: ',
        //     { localsManifest: res.locals.manifest },
        //     '\n'.padEnd(220, '='),
        // );

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify(initialPageData),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['article-data'],
            });
        } catch (e) {
            return next(e);
        }
    }),
);

export default router;
