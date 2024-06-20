import express, { NextFunction, Request, Response } from 'express';

import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await global.fetch('https://nlp-ssa.dev/api/article-data');
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[home route] - caught exception: ${e}`);
        }

        // console.log(
        //     '\n'.padStart(220, '='),
        //     'home router: ',
        //     { localsManifest: res.locals.manifest },
        //     '\n'.padEnd(220, '='),
        // );

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify(initialPageData),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['home'],
            });
        } catch (e) {
            return next(e);
        }
    }),
);

export default router;
