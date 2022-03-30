import type { GetServerSideProps, NextPage, NextPageContext } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { LatestVersion } from "components/latest-version";
import { UsefulLinks } from "components/useful-links";

const SoftwarePage: NextPage = () => {
  return (
    <>
      <Hero>
        <div className="max-w-7xl mx-auto w-10/12 flex justify-center">
          <LatestVersion software="Python" version="3.6.5" />
        </div>

        <div className="max-w-6xl mx-auto flex justify-center mt-8">
          <UsefulLinks
            links={[
              {
                title: "Documentation",
                url: "https://docs.python.org/3/",
              },
              {
                title: "Download Python",
                url: "https://www.python.org/downloads/",
              },
              {
                title: "Changelog",
                url: "https://docs.python.org/3/whatsnew/3.7.html",
              },
            ]}
          />
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

export default SoftwarePage;

export const getServerSideProps: GetServerSideProps = async (context) => {
  // TODO: fetch data
  if (context.req.headers["user-agent"]?.includes("curl")) {
    context.res.end("hi");

    return { props: {} };
  }

  return {
    props: {
      software: "python",
    },
  };
};
