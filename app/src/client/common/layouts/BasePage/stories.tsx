import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { getStoryArticleData } from 'client/_story-data';
import { BasePage } from 'client/common/layouts';

const meta = {
    title: 'Common/BasePage',
    component: BasePage,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof BasePage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const DefaultBasePage: Story = {
    // args: { className: 'local' },
    render: (args) => <BasePage {...args}>I am a child!</BasePage>,
};

export const BasePageWithTitle: Story = {
    args: { pageTitle: 'Article Data Overview' },
    render: (args) => (
        <BasePage {...args}>
            {/* TODO: put some actual stuff here :] */}
            {getStoryArticleData().data!.map((data, i) => (
                <pre key={`article-data-${i}`}>{JSON.stringify(data, null, 4)}</pre>
            ))}
        </BasePage>
    ),
};
