import PlausibleProvider from "next-plausible";
import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html>
      <Head />
      <body>
        <PlausibleProvider domain="latest.cat">
          <Main />
        </PlausibleProvider>
        <NextScript />
      </body>
    </Html>
  );
}
