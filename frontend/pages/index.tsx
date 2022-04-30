import type { GetServerSideProps, NextPage } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { SearchInput } from "components/search-input";
import { FormEventHandler } from "react";
import Head from "next/head";
import { AboutBox } from "components/about-box";
import { Meta } from "components/meta";

const Home: NextPage = () => {
  const goToSoftware: FormEventHandler<HTMLFormElement> = (event) => {
    event.preventDefault();

    const data = Object.fromEntries(new FormData(event.currentTarget));

    if (data.software) {
      window.location.href = `/${data.software}`;
    }
  };

  return (
    <>
      <Head>
        <Meta
          title="latest.cat - find the latest version of your favourite software"
          path="/"
        />
      </Head>
      <Hero>
        <div className="max-w-2xl mx-auto w-11/12">
          <form onSubmit={goToSoftware}>
            <SearchInput />
          </form>
        </div>
      </Hero>
      <Marquee />

      <div className="dark:bg-dark dark:text-white">
        <div className="max-w-7xl mx-auto pt-10 w-11/12">
          <AboutBox />
          <Box title="Did you know?" className="bg-mint">
            <p className="mb-4 font-bold">
              You can also use latest.cat from the command line:
            </p>
            <div>
              <p className="mb-4 flex overflow-scroll">
                <span className="mr-4 select-none">$</span>
                <pre>
                  <code>curl -Lfs latest.cat/python</code>
                </pre>
              </p>
            </div>
            <div>
              <p className="mb-4 font-bold">
                And you can even filter the results by version number:
              </p>

              <p className="mb-4 flex overflow-scroll">
                <span className="mr-4 select-none">$</span>
                <pre>
                  <code>curl -Lfs latest.cat/python/3.6</code>
                </pre>
              </p>
            </div>
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

export const getServerSideProps: GetServerSideProps = async (context) => {
  const slug = context.query.slug as string;

  if (context.req.headers["user-agent"]?.includes("curl")) {
    context.res.end("Try running `curl -fsL latest.cat/python` 🐈 \n");

    return { props: {} };
  }

  return {
    props: {},
  };
};
