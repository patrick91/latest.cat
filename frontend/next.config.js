/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: process.env.BACKEND_ENDPOINT,
      },
    ];
  },
};

module.exports = nextConfig;
