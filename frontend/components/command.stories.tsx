import { ComponentMeta } from "@storybook/react";

import { Command } from "./command";

export default {
  title: "Command",
  component: Command,
} as ComponentMeta<typeof Command>;

export const Primary = () => <Command text="curl -Lfs latest.cat/python" />;
