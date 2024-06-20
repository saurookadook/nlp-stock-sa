import express, { NextFunction, Request, Response } from 'express';

import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`/api/auth/login`, { method: 'GET' });
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[home route] - caught exception: ${e}`);
        }

        // const { appJs: reactVendorsJs } = res.locals.manifest['react-vendors'];
        console.log(
            '\n'.padStart(220, '='),
            'login router: ',
            { localsManifest: res.locals.manifest },
            '\n'.padEnd(220, '='),
        );

        try {
            return res.render('index', {
                layout: 'index',
                initialPageData: JSON.stringify(initialPageData),
                ...res.locals.manifest['common'],
                ...res.locals.manifest['login'],
            });
        } catch (e) {
            console.warn('\n'.padStart(220, '='), 'login router: render', e, '\n'.padEnd(220, '='));
            return next(e);
        }
    }),
);

export default router;
