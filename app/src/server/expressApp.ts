import path from 'node:path';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import express, { RequestHandler } from 'express';
import { engine } from 'express-handlebars';

import accountRouter from './account';
import dataExplorersRouter from './data-explorers';
import homeRouter from './home';
import loginRouter from './login';
import { manifestMiddleware, sessionMiddleware } from './middleware';

const __dirname = path.resolve();

const expressApp = express();

expressApp.set('view engine', 'handlebars');
expressApp.engine(
    'handlebars',
    engine({
        layoutsDir: `${__dirname}/src/server/views`,
    }),
);
expressApp.set('views', path.join(__dirname, 'src/server/views'));

expressApp.use(cookieParser() as RequestHandler);
// Enable cors to be able to reach the backend on localhost:3000 while running React.js in dev mode on localhost:8081
// You might want to disbale this on production.
expressApp.use(cors());
expressApp.use(express.json() as RequestHandler);

// // This code makes sure that any request that does not matches a static file
// // in the build folder, will just serve index.html. Client side routing is
// // going to make sure that the correct content will be loaded.
// expressApp.use((req: Request, res: Response, next: NextFunction) => {
//     if (/(.ico|.js|.css|.jpg|.png|.map)$/i.test(req.path)) {
//         next();
//     } else {
//         res.header('Cache-Control', 'private, no-cache, no-store, must-revalidate');
//         res.header('Expires', '-1');
//         res.header('Pragma', 'no-cache');
//         res.sendFile(path.join(__dirname, 'build', 'index.html'));
//     }
// });

expressApp.use(sessionMiddleware);
expressApp.use(manifestMiddleware);

if (process.env.ENV !== 'production') {
    // res.header('Cache-Control', 'private, no-cache, no-store, must-revalidate');
    // res.header('Expires', '-1');
    // res.header('Pragma', 'no-cache');
    // res.sendFile(path.join(__dirname, 'build', 'index.html'));
    expressApp.use('/dist', express.static(path.join(__dirname, 'dist')));
}

expressApp.use('/app/data-explorers', dataExplorersRouter);
expressApp.use('/app/account', accountRouter);
expressApp.use('/app/login', loginRouter);
expressApp.use('/app/', homeRouter);

export default expressApp;
