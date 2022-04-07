import type { GetServerSideProps, NextPage, NextPageContext } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { SoftwareNotFound } from "components/software-not-found";
import { useRouter } from "next/router";
import { AboutBox } from "components/about-box";
import Head from "next/head";
import { Meta } from "components/meta";

const Latest404: NextPage = () => {
  const softwareName =
    typeof window !== "undefined" ? window.location.pathname.split("/")[1] : "";

  const text = `Hey @patrick91! I think "${softwareName}" is missing from https://latest.cat, can you please add it?`;

  const tweetLink = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
    text
  )}`;

  return (
    <>
      <Head>
        <Meta
          title={`404!!1 - ${softwareName} is not found on latest.cat`}
          path="/"
        />
      </Head>

      <Hero>
        <div className="max-w-7xl mx-auto w-10/12 flex justify-center">
          <SoftwareNotFound />
        </div>

        <div className="max-w-6xl mx-auto flex justify-center mt-8">
          {typeof window !== "undefined" && (
            <p className="mb-4 text-xl">
              Do you think this is a mistake? Send us a{" "}
              <a
                target="_blank"
                rel="noreferrer noopener"
                href={tweetLink}
                className="font-bold underline"
              >
                tweet
              </a>{" "}
              and we&apos;ll try to fix it as soon as possible!
            </p>
          )}
        </div>
      </Hero>
      <Marquee />

      <div className="dark:bg-dark dark:text-white">
        <div className="max-w-7xl mx-auto pt-10 w-11/12">
          <AboutBox />

          <div className="mt-10">
            <Footer />
          </div>
        </div>
      </div>
    </>
  );
};

export default Latest404;
