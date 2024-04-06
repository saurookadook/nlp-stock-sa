import express from 'express';

import { manifestMiddleware } from 'server/middleware';
import { asyncWrapper } from 'server/utils';

const router = express.Router();

router.use(manifestMiddleware);

router.use(
    asyncWrapper(async (req, res, next) => {
        const pageDataResponse = await fetch(`/nlp-ssa/internal-api/v1/login/`);
        const initialPageData = await pageDataResponse.json();

        return res.render('index', {
            layout: 'index',
            initialPageData: JSON.stringify(initialPageData),
            ...res.locals.manifest['common'],
            ...res.locals.manifest['login'],
        })
    })
)

export default router;
