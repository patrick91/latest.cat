import Marquee from "./Marquee";

interface LatestReleasesMarqueeProps {
	releases: { name: string; url: string }[];
}

export default function LatestReleasesMarquee({
	releases,
}: LatestReleasesMarqueeProps) {
	if (releases.length === 0) {
		return null;
	}

	return <Marquee releases={releases} />;
}
