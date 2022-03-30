import { ComponentMeta } from "@storybook/react";

import { Marquee } from "./marquee";

export default {
  title: "Marquee",
  component: Marquee,
  parameters: {
    layout: "fullscreen",
  },
} as ComponentMeta<typeof Marquee>;

export const Primary = () => <Marquee />;
