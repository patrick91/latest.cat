/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: "https://latest-cat.fly.dev/graphql",
      },
    ];
  },
};

module.exports = nextConfig;
