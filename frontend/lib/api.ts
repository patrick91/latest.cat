const API_URL = "https://latest.cat/graphql";

export const fetchLatestVersion = async ({
  slug,
  version,
  fetchSoftware,
}: {
  slug: string;
  version?: string;
  fetchSoftware: boolean;
}) => {
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

export const fetchAllSoftware = async () => {
  const query = `query FetchAllSoftware {
    allSoftware {
      majorVersions
      software {
        name
        slug
      }
    }
  }`;

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
    }),
  });
  const json = await res.json();

  if (json.errors) {
    console.error(json.errors);
    throw new Error("Failed to fetch API");
  }

  return json.data.allSoftware as {
    majorVersions: string[];
    software: {
      name: string;
      slug: string;
    };
  }[];
};
