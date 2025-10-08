import { useState, useEffect } from "react";
import Marquee from "./Marquee";

interface Release {
	version: string;
	softwareName: string;
	softwareSlug: string;
	pushedAt: string;
}

export default function LatestReleasesMarquee() {
	const [releases, setReleases] = useState<
		{ name: string; url: string }[]
	>([]);

	useEffect(() => {
		const operation = `query {
			latestReleases {
				version
				softwareName
				softwareSlug
				pushedAt
			}
		}`;

		fetch("https://latest-cat.stellate.sh/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ query: operation }),
		})
			.then((res) => res.json())
			.then((response) => {
				const releases = response.data.latestReleases.map(
					(release: Release) => ({
						name: `${release.softwareName} ${release.version}`,
						url: `/${release.softwareSlug}`,
					}),
				);
				setReleases(releases);
			});
	}, []);

	if (releases.length === 0) {
		return null;
	}

	return <Marquee releases={releases} />;
}
