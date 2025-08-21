import expressApp from './expressApp';
import { createTerminationHandler } from './utils';

const CLIENT_PORT = Number(process.env.CLIENT_PORT || 8080);
const CLIENT_HOST = process.env.CLIENT_HOST || '0.0.0.0';
const frontendServer = expressApp.listen(CLIENT_PORT, CLIENT_HOST, () => {
    console.log(`Express app frontend server running on
        \n- host ${CLIENT_HOST}
        \n- port ${CLIENT_PORT}`);
});

const exitHandler = createTerminationHandler(frontendServer);

process.on('uncaughtException', exitHandler(1, 'Unexpected Error'));
process.on('unhandledRejection', exitHandler(1, 'Unhandled Promise'));
process.on('SIGINT', exitHandler(0, 'SIGINT'));
process.on('SIGTERM', exitHandler(0, 'SIGTERM'));
