import Hero from "../components/Hero";
import Footer from "../components/Footer";
import AboutBox from "../components/AboutBox";
import LatestVersion from "../components/LatestVersion";
import LatestReleasesMarquee from "../components/LatestReleasesMarquee";

interface SoftwareProps {
	software: {
		name: string;
		slug: string;
		links: { url: string; name: string }[];
	};
	version: string;
	requestedVersion?: string;
	latestReleases: { name: string; url: string }[];
}

export default function Software({
	software,
	version,
	requestedVersion,
	latestReleases,
}: SoftwareProps) {
	return (
		<div>
			<Hero>
				<div className="max-w-7xl mx-auto w-10/12 flex justify-center">
					<LatestVersion
						software={software.name}
						version={version}
						requestedVersion={requestedVersion}
					/>
				</div>

				<div className="max-w-6xl mx-auto flex justify-center mt-8">
					{/* UsefulLinks component can be added later */}
				</div>
			</Hero>

			<LatestReleasesMarquee releases={latestReleases} />

			<div className="dark:bg-dark dark:text-white">
				<div className="max-w-7xl mx-auto pt-10 w-11/12">
					<AboutBox />

					<div className="mt-10">
						<Footer />
					</div>
				</div>
			</div>
		</div>
	);
}
