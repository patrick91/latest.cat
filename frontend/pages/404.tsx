import type { GetServerSideProps, NextPage, NextPageContext } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { SoftwareNotFound } from "components/software-not-found";
import { useRouter } from "next/router";

const Latest404: NextPage = () => {
  const softwareName =
    typeof window !== "undefined" ? window.location.pathname.split('/')[1] : "";

  const text = `Hey @patrick91! I think "${softwareName}" is missing from https://latest.cat, can you please add it?`;

  const tweetLink = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
    text
  )}`;

  return (
    <>
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
          <Box title="What is latest.cat?">
            <p className="mb-4 font-bold">
              Ever struggled to find the latest version of a programming
              language?
            </p>
            <p className="mb-4">
              <strong className="font-bold">latest.cat</strong> is a simple,
              fast and free way to browse the latest releases of your favorite
              programming language.
            </p>
            <p className="mb-4">
              Type your favorite programming language name in the search bar,
              hit enter and you will immediately see the latest releases of that
              programming language.
              <br />
              You can even use <strong className="font-bold">
                latest.cat
              </strong>{" "}
              from the command line!
            </p>
          </Box>

          <div className="mt-10">
            <Footer />
          </div>
        </div>
      </div>
    </>
  );
};

export default Latest404;
