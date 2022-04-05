/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: "https://latest-cat-65bwarhayq-ew.a.run.app/graphql",
      },
    ];
  },
};

module.exports = nextConfig;
