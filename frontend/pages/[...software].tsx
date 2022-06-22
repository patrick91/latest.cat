import type {
  GetServerSideProps,
  GetStaticPaths,
  GetStaticProps,
  NextPage,
} from "next";

import { Hero } from "components/hero";
import { Marquee } from "components/marquee";
import { Footer } from "components/footer";
import { LatestVersion } from "components/latest-version";
import { UsefulLinks } from "components/useful-links";
import { AboutBox } from "components/about-box";
import { Meta } from "components/meta";

const SoftwarePage: NextPage<{
  latestVersion: string;
  version?: string;
  software: {
    name: string;
    links: {
      url: string;
      title: string;
    }[];
  };
}> = ({ latestVersion, software, version }) => {
  return (
    <>
      <Meta
        title={`${software.name} latest version is ${latestVersion} - latest.cat`}
        path="/"
      />

      <Hero>
        <div className="max-w-7xl mx-auto w-10/12 flex justify-center">
          <LatestVersion
            software={software.name}
            version={latestVersion}
            requestedVersion={version}
          />
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

const fetchLatestVersion = async ({
  slug,
  version,
  fetchSoftware,
}: {
  slug: string;
  version?: string;
  fetchSoftware: boolean;
}) => {
  const API_URL = "https://latest.cat/graphql";
  const query = `
    query FindVersion($slug: String!, $version: String, $fetchSoftware: Boolean!) {
      findVersion(slug: $slug, version: $version) {
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
        version: version || null,
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

export const getStaticProps: GetStaticProps = async (context) => {
  return {
    props: {
      person: 1,
    },
  };
};
export const getStaticPaths: GetStaticPaths = async () => {
  const paths = ["1"];
  return {
    paths,
    fallback: false,
  };
};
