import { ComponentMeta } from "@storybook/react";

import { Toggle } from "./toggle";

export default {
  title: "Toggle",
  component: Toggle,
} as ComponentMeta<typeof Toggle>;

export const Primary = () => (
  <Toggle onToggle={(value) => console.log("toggled", value)} checked={false} />
);
