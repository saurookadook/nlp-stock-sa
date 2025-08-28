import { inspect } from 'node:util';
import { NextFunction, Request, Response } from 'express';

const AUTH_COOKIE_KEY = process.env.AUTH_COOKIE_KEY || 'NLPSSA-Authorization.Dev';

export function sessionMiddleware(
    req: Request, // force formatting
    res: Response,
    next: NextFunction,
) {
    console.log(
        '\n'.padStart(220, '?'),
        `${sessionMiddleware.name} - req.cookies:\n`,
        inspect(
            {
                cookies: req.cookies,
                req,
            },
            { colors: true, compact: false },
        ),
        '\n'.padEnd(220, '?'),
    );
    const authCookie = req.cookies[AUTH_COOKIE_KEY];

    if (authCookie != null) {
        const [username, token] = authCookie.split(':');

        res.locals.auth = {
            cookie: authCookie,
            token,
        };
        res.locals.user = {
            username,
        };
    }

    next();
}
