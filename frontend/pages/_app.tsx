import "../styles/globals.css";
import type { AppProps } from "next/app";

import PlausibleProvider from "next-plausible";
import { useLayoutEffect } from "react";
import { getCookie } from "cookies-next";

function MyApp({ Component, pageProps }: AppProps) {
  useLayoutEffect(() => {
    const darkMode = getCookie("darkMode");
    if (darkMode) {
      document.documentElement.classList.add("dark");
    }
  }, []);

  return (
    <PlausibleProvider domain="latest.cat">
      <Component {...pageProps} />
    </PlausibleProvider>
  );
}

export default MyApp;
