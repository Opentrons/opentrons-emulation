/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';
module.exports = async (phase, { defaultConfig }) => {
  let internalHost = null;
  // In dev mode we use the internal-ip to serve the assets
  if (!isProd) {
    const { internalIpV4 } = await import('internal-ip');
    internalHost = await internalIpV4();
  }
  const nextConfig = {
    // Ensure Next.js uses SSG instead of SSR
    // https://nextjs.org/docs/pages/building-your-application/deploying/static-exports
    output: 'export',
    // Note: This experimental feature is required to use NextJS Image in SSG mode.
    // See https://nextjs.org/docs/messages/export-image-api for different workarounds.
    images: {
      unoptimized: true,
    },
    // Configure assetPrefix or else the server won't properly resolve your assets.
    assetPrefix: isProd ? null : `http://${internalHost}:3000`,
  };
  return nextConfig;
};