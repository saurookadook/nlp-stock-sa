import path from 'path';
import type { StorybookConfig } from '@storybook/react-webpack5';
import TsConfigPathsPlugin from 'tsconfig-paths-webpack-plugin';

// import defaultConfig from '../webpack.config';

const config: StorybookConfig = {
    addons: [
        '@storybook/addon-webpack5-compiler-swc',
        '@storybook/addon-onboarding',
        '@storybook/addon-links',
        '@storybook/addon-essentials',
        '@chromatic-com/storybook',
        '@storybook/addon-interactions',
    ],
    docs: {
        autodocs: 'tag',
    },
    framework: {
        name: '@storybook/react-webpack5',
        options: {},
    },
    stories: ['../src/**/*.mdx', '../src/**/?(*.)stories.@(js|jsx|mjs|ts|tsx)'],
    webpack: async (config) => {
        // const defaultRules = defaultConfig().module.rules;
        // module: {
        //     ...config.module,
        //     // rules: [...configRules, ...defaultRules],
        // },

        if (config.resolve) {
            const configRules = config.module?.rules || [];
            // console.log({ configRules, resolve: config.resolve });
            config.resolve.alias = {
                ...config.resolve!.alias,
                '_story-data': path.resolve(__dirname, '../src/_story-data'),
                client: path.resolve(__dirname, '../src/client'),
                server: path.resolve(__dirname, '../src/server'),
                stories: path.resolve(__dirname, '../src/stories'),
                types: path.resolve(__dirname, '../src/types'),
            };

            config.resolve.plugins = [
                ...(config.resolve?.plugins || []),
                new TsConfigPathsPlugin({
                    extensions: config.resolve?.extensions,
                }),
            ];
        }

        return config;
    },
};
export default config;
