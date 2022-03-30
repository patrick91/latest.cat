import { ComponentMeta } from "@storybook/react";

import { Hero } from "./hero";

export default {
  title: "Hero",
  component: Hero,
  parameters: {
    layout: "fullscreen",
  },
} as ComponentMeta<typeof Hero>;

export const Primary = () => <Hero />;
