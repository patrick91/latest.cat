import { ComponentMeta } from "@storybook/react";

import { UsefulLinks } from "./useful-links";

export default {
  title: "UsefulLinks",
  component: UsefulLinks,
} as ComponentMeta<typeof UsefulLinks>;

export const Primary = () => (
  <UsefulLinks
    links={[
      {
        title: "Documentation",
        url: "https://docs.python.org/3/",
      },
      {
        title: "Download Python",
        url: "https://www.python.org/downloads/",
      },
      {
        title: "Changelog",
        url: "https://docs.python.org/3/whatsnew/3.7.html",
      },
    ]}
  />
);
