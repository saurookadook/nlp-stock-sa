import express, { NextFunction, Request, Response } from 'express';

import { manifestMiddleware } from 'server/middleware';
import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(manifestMiddleware);

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`/nlp-ssa/internal-api/v1/home`);
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[home route] - caught exception: ${e}`);
        }

        // const { appJs: reactVendorsJs } = res.locals.manifest['react-vendors'];
        console.log(
            '\n'.padStart(220, '='),
            'home router: ',
            { localsManifest: res.locals.manifest },
            '\n'.padEnd(220, '='),
        );

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
