import { ComponentMeta } from "@storybook/react";

import { SoftwareNotFound } from "./software-not-found";

export default {
  title: "SoftwareNotFound",
  component: SoftwareNotFound,
} as ComponentMeta<typeof SoftwareNotFound>;

export const Primary = () => <SoftwareNotFound />;
