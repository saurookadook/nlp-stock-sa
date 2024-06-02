import path from 'path';

const __dirname = path.resolve();
console.log(`in jest config: __dirname === ${__dirname}`);

/** @type {import('ts-jest').JestConfigWithTsJest} */
const jestConfig = {
    // modulePaths: [
    //     '<rootDir>',
    //     // '<rootDir>/src', path.resolve(__dirname, '../src')
    // ],
    moduleDirectories: ['node_modules'],
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
    moduleNameMapper: {
        '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
            '<rootDir>/client/__mocks__/fileMock.ts',
        '^client(.*)$': '<rootDir>/client/$1',
        '^server(.*)$': '<rootDir>/server/$1',
        '^stories(.*)$': '<rootDir>/stories/$1',
        '^types(.*)$': '<rootDir>/types/$1',
    },
    preset: 'ts-jest',
    randomize: true,
    // TODO: maybe add this....?
    // https://github.com/Ashvin-Pal/jest-console-group-reporter
    reporters: ['default', 'summary'],
    setupFilesAfterEnv: ['<rootDir>/client/setupTests.ts'],
    testEnvironment: 'jsdom',
    // transform: {
    //     '\\.[jt]sx?$': 'babel-jest',
    // },
    rootDir: path.resolve(__dirname, 'src'),
};

export default jestConfig;
