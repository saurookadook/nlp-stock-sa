import { inspect } from 'node:util';
import express, { NextFunction, Request, Response } from 'express';

import { baseRequestURL } from 'server/constants';
import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(
    asyncWrapper(async (req: Request, res: Response, next: NextFunction) => {
        let initialPageData = {};
        // console.log(
        //     '\n'.padStart(220, '?'),
        //     `login - res.locals:\n`,
        //     inspect(
        //         {
        //             locals: res.locals,
        //         },
        //         { colors: true, compact: false },
        //     ),
        //     '\n'.padEnd(220, '?'),
        // );

        try {
            // TODO: add some user-specific thing to request?
            const pageDataResponse = await fetch(`${baseRequestURL}/api/auth/login`, {
                headers: {
                    Cookie: req.headers.cookie || '',
                },
            });
            initialPageData = await pageDataResponse.json();
        } catch (e) {
            console.warn(`[login route] - caught exception: ${e}`);
        }

        // const { appJs: reactVendorsJs } = res.locals.manifest['react-vendors'];
        console.log(
            '\n'.padStart(220, '='),
            'login router: ',
            { localsManifest: res.locals.manifest },
            '\n'.padEnd(220, '='),
        );

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
                ...res.locals.manifest['login'],
            });
        } catch (e) {
            console.warn('\n'.padStart(220, '='), 'login router: render', e, '\n'.padEnd(220, '='));
            return next(e);
        }
    }),
);

export default router;
