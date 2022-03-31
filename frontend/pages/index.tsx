import type { NextPage } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { SearchInput } from "components/search-input";

const Home: NextPage = () => {
  return (
    <>
      <Hero>
        <div className="max-w-2xl mx-auto w-11/12">
          <SearchInput />
        </div>
      </Hero>
      <Marquee />

      <div className="dark:bg-dark dark:text-white">
        <div className="max-w-7xl mx-auto pt-10 w-11/12">
          <Box title="What is latest.cat?" className="mb-10">
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
          <Box title="Did you know?" className="bg-mint">
            <p className="mb-4 font-bold">
              You can also use latest.cat from the command line:
            </p>
            <p className="mb-4 flex overflow-scroll">
              <span className="mr-4 select-none">$</span>
              <pre>
                <code>curl -fs latest.cat/python</code>
              </pre>
            </p>
            <p className="mb-4 font-bold">
              And you can even filter the results by version number:
            </p>

            <p className="mb-4 flex overflow-scroll">
              <span className="mr-4 select-none">$</span>
              <pre>
                <code>curl -fs latest.cat/python/3.6</code>
              </pre>
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

export default Home;
