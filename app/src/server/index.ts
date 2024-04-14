import expressApp from './expressApp';
import { createTerminationHandler } from './utils';

const CLIENT_PORT = Number(process.env.CLIENT_PORT || 8080);
const HOST = process.env.HOST || '0.0.0.0';
const frontendServer = expressApp.listen(CLIENT_PORT, HOST, () => {
    console.log(`Express app frontend server running on port ${CLIENT_PORT}`);
});

const exitHandler = createTerminationHandler(frontendServer);

process.on('uncaughtException', exitHandler(1, 'Unexpected Error'));
process.on('unhandledRejection', exitHandler(1, 'Unhandled Promise'));
process.on('SIGINT', exitHandler(0, 'SIGINT'));
process.on('SIGTERM', exitHandler(0, 'SIGTERM'));
