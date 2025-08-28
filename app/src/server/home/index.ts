import express, { NextFunction, Request, Response } from 'express';
import { baseRequestURL } from 'server/constants';

import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/article-data`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });
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
