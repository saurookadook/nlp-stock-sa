import path from 'path';

// import cors from 'cors';
import express, { RequestHandler } from 'express';
import { engine } from 'express-handlebars';

import homeRouter from './home';
import loginRouter from './login';

const __dirname = path.resolve();
console.log('\n'.padStart(220, '='), `dirname: ${__dirname}`, '\n'.padEnd(220, '='));

const expressApp = express();

expressApp.set('view engine', 'handlebars');
expressApp.engine(
    'handlebars',
    engine({
        layoutsDir: `${__dirname}/src/server/views`,
    }),
);
expressApp.set('views', path.join(__dirname, 'src/server/views'));

// Enable cors to be able to reach the backend on localhost:8080 while running React.js in dev mode on localhost:3000
// You might want to disbale this on production.
// expressApp.use(cors());
expressApp.use(express.json() as RequestHandler);

// expressApp.post('/api', async function(req: Request, res: Response) {
//     let body = plainToClass(RequestBody, req.body as Object);
//     let validationErrors = await validate(body);
//     if (validationErrors.length == 0) {
//         const responseBody: ResponseBody = new ResponseBody("Hello, " + body.name);
//         res.contentType('application/json');
//         res.status(200);
//         res.send(responseBody);
//     } else {
//         res.sendStatus(400);
//     }
// });

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

if (process.env.ENV !== 'production') {
    expressApp.use('/dist', express.static(path.join(__dirname, 'dist')));
}

expressApp.use('/login', loginRouter);
expressApp.use('/', homeRouter);

export default expressApp;