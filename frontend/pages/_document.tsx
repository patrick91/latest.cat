import PlausibleProvider from "next-plausible";
import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html>
      <Head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="manifest" href="/site.webmanifest" />
      </Head>
      <body>
        <PlausibleProvider domain="latest.cat">
          <Main />
        </PlausibleProvider>
        <NextScript />
      </body>
    </Html>
  );
}
