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
import { fetchAllSoftware, fetchLatestVersion } from "lib/api";

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

export const getStaticProps: GetStaticProps<any, { software: string[] }> =
  async (context) => {
    const [slug, ...versionBits] = context.params!.software;
    const version = versionBits.join(".");

    const result = await fetchLatestVersion({
      slug,
      version,
      fetchSoftware: true,
    });

    return {
      props: {
        version,
        latestVersion: result?.latestVersion,
        software: result?.software,
      },
    };
  };

export const getStaticPaths: GetStaticPaths = async () => {
  const softwares = await fetchAllSoftware();

  const paths = softwares.flatMap((software) =>
    software.majorVersions.map((version) => ({
      params: { software: [software.software.slug, version] },
    }))
  );

  return {
    paths: paths.concat(
      softwares.map((software) => ({
        params: { software: [software.software.slug] },
      }))
    ),
    fallback: "blocking",
  };
};
