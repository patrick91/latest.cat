import { ComponentMeta } from "@storybook/react";

import { Footer } from "./footer";

export default {
  title: "Footer",
  component: Footer,
} as ComponentMeta<typeof Footer>;

export const Primary = () => <Footer />;
