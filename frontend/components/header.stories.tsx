import { ComponentMeta } from "@storybook/react";

import { Header } from "./header";

export default {
  title: "Header",
  component: Header,
} as ComponentMeta<typeof Header>;

export const Primary = () => <Header />;
