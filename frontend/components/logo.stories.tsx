import { ComponentMeta } from "@storybook/react";

import { Logo } from "./logo";

export default {
  title: "Logo",
  component: Logo,
} as ComponentMeta<typeof Logo>;

export const Primary = () => <Logo />;
