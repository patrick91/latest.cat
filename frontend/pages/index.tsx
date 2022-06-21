import type { GetServerSideProps, NextPage } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Box } from "components/box";
import { Footer } from "components/footer";
import { SearchInput } from "components/search-input";
import { FormEventHandler } from "react";
import { AboutBox } from "components/about-box";
import { Meta } from "components/meta";
import { Command } from "components/command";

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
      <Meta
        title="latest.cat - find the latest version of your favourite software"
        path="/"
      />
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
            <Command text="curl -Lfs latest.cat/python" />
            <div>
              <p className="mb-4 font-bold">
                And you can even filter the results by version number:
              </p>
              <Command text="curl -Lfs latest.cat/python/3.6" />
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
