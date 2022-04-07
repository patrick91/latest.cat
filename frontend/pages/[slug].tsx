import type { GetServerSideProps, NextPage } from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Footer } from "components/footer";
import { LatestVersion } from "components/latest-version";
import { UsefulLinks } from "components/useful-links";
import { AboutBox } from "components/about-box";
import Head from "next/head";
import { Meta } from "components/meta";

const SoftwarePage: NextPage<{
  latestVersion: string;
  software: {
    name: string;
    links: {
      url: string;
      title: string;
    }[];
  };
}> = ({ latestVersion, software }) => {
  return (
    <>
      <Head>
        <Meta
          title={`${software.name} latest version is ${latestVersion} - latest.cat`}
          path="/"
        />
      </Head>
      <Hero>
        <div className="max-w-7xl mx-auto w-10/12 flex justify-center">
          <LatestVersion software={software.name} version={latestVersion} />
        </div>

        <div className="max-w-6xl mx-auto flex justify-center mt-8">
          <UsefulLinks links={software.links} />
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

export default SoftwarePage;

const fetchLatestVersion = async (slug: string, fetchSoftware: boolean) => {
  const API_URL = "https://latest.cat/graphql";
  const query = `
    query FindVersion($slug: String!, $fetchSoftware: Boolean!) {
      findVersion(slug: $slug) {
        latestVersion
        software @include(if: $fetchSoftware) {
          slug
          name
          links {
            title: name
            url
          }
        }
      }
    }
  `;

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      variables: {
        slug,
        fetchSoftware,
      },
    }),
  });
  const json = await res.json();

  if (json.errors) {
    console.error(json.errors);
    throw new Error("Failed to fetch API");
  }

  return json.data.findVersion as {
    latestVersion: string;
    software?: {
      name: string;
      slug: string;
    };
  };
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const slug = context.query.slug as string;

  if (context.req.headers["user-agent"]?.includes("curl")) {
    const result = await fetchLatestVersion(slug, false);

    if (!result) {
      return { notFound: true };
    }

    context.res.end(result?.latestVersion);

    return { props: {} };
  }

  const result = await fetchLatestVersion(slug, true);

  if (!result) {
    return { notFound: true };
  }

  return {
    props: {
      latestVersion: result?.latestVersion,
      software: result?.software,
    },
  };
};
