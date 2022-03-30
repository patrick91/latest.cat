import { ComponentMeta } from "@storybook/react";

import { Box } from "./box";

export default {
  title: "Box",
  component: Box,
} as ComponentMeta<typeof Box>;

export const Primary = () => (
  <Box title="Hello there">
    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dignissimos facere
    minima minus quibusdam odit vero rem, error voluptatum, nisi pariatur
    cupiditate ut numquam vel placeat saepe delectus a sequi molestiae!
  </Box>
);
