import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { NavHeader } from 'client/common/components';

const meta = {
    title: 'Common/NavHeader',
    component: NavHeader,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof NavHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseNavHeader: Story = {
    // args: { className: 'local' },
    render: (args) => <NavHeader {...args}>I am a child!</NavHeader>,
};
