import { ComponentMeta } from "@storybook/react";

import { SearchInput } from "./search-input";

export default {
  title: "SearchInput",
  component: SearchInput,
} as ComponentMeta<typeof SearchInput>;

export const Primary = () => <SearchInput />;
