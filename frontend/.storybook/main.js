module.exports = {
  stories: ["../components/*.stories.mdx", "../components/*.stories.@(js|jsx|ts|tsx)", "../components/**/story.mdx", "../components/**/story.@(js|jsx|ts|tsx)", "../components/**/*.stories.mdx", "../components/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [{
    name: "@storybook/addon-postcss",
    options: {
      postcssLoaderOptions: {
        implementation: require("postcss")
      }
    }
  }, "@storybook/addon-links", "@storybook/addon-essentials", "@storybook/addon-interactions", "@storybook/addon-mdx-gfm"],
  framework: {
    name: "@storybook/nextjs",
    options: {}
  },
  staticDirs: ["../public"],
  docs: {
    autodocs: true
  }
};