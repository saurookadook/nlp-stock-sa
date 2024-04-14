import expressApp from './expressApp';
import { createTerminationHandler } from './utils';

const PORT = process.env.CLIENBT_PORT || 8080;
const frontendServer = expressApp.listen(PORT, () => {
    console.log(`Express app frontend server running on port ${PORT}`);
});

const exitHandler = createTerminationHandler(frontendServer);

process.on('uncaughtException', exitHandler(1, 'Unexpected Error'));
process.on('unhandledRejection', exitHandler(1, 'Unhandled Promise'));
process.on('SIGINT', exitHandler(0, 'SIGINT'));
process.on('SIGTERM', exitHandler(0, 'SIGTERM'));
