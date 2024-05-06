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
        const configRules = config.module?.rules || [];
        console.log({ configRules, resolve: config.resolve });
        // const defaultRules = defaultConfig().module.rules;
        return {
            ...config,
            // module: {
            //     ...config.module,
            //     // rules: [...configRules, ...defaultRules],
            // },
            resolve: {
                plugins: [
                    ...(config.resolve?.plugins || []),
                    new TsConfigPathsPlugin({
                        extensions: config.resolve?.extensions,
                    }),
                ],
            },
        };
    },
};
export default config;
