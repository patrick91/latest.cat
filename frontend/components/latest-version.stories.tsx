import { ComponentMeta } from "@storybook/react";

import { LatestVersion } from "./latest-version";

export default {
  title: "LatestVersion",
  component: LatestVersion,
} as ComponentMeta<typeof LatestVersion>;

export const Primary = () => <LatestVersion version="1.2" software="Orlando" />;
