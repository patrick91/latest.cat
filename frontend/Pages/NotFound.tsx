import { Head } from "@inertiajs/react";
import Hero from "../components/Hero";
import Footer from "../components/Footer";
import AboutBox from "../components/AboutBox";
import LatestReleasesMarquee from "../components/LatestReleasesMarquee";
import { getHomeOGMeta } from "../utils/ogMeta";

interface NotFoundProps {
	softwareName: string;
	latestReleases: { name: string; url: string }[];
}

export default function NotFound({ softwareName, latestReleases }: NotFoundProps) {
	const text = `Hey @patrick91! I think "${softwareName}" is missing from https://latest.cat, can you please add it?`;
	const tweetLink = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
	
	// Use home OG metadata for 404 pages
	const ogMeta = getHomeOGMeta();

	return (
		<>
			<Head>
				<title>{ogMeta.title}</title>
				<meta name="description" content={ogMeta.description} />
				
				{/* Open Graph / Facebook */}
				<meta property="og:type" content="website" />
				<meta property="og:url" content={ogMeta.url} />
				<meta property="og:title" content={ogMeta.title} />
				<meta property="og:description" content={ogMeta.description} />
				<meta property="og:image" content={ogMeta.image} />
				
				{/* Twitter */}
				<meta property="twitter:card" content="summary_large_image" />
				<meta property="twitter:url" content={ogMeta.url} />
				<meta property="twitter:title" content={ogMeta.title} />
				<meta property="twitter:description" content={ogMeta.description} />
				<meta property="twitter:image" content={ogMeta.image} />
		</Head>
		
		<div>
			<Hero>
				<div className="max-w-7xl mx-auto w-10/12 flex justify-center">
					<div className="border text-4xl font-heading font-black bg-gray border-black rounded-full shadow-drop px-12 py-8 text-center inline-block text-black">
						<svg
							width={50}
							height={43}
							fill="none"
							viewBox="0 0 50 43"
							className="inline-block mr-4"
						>
							<path
								fill="#000"
								d="M10.527 10.526h2.632v2.632h-2.632zM31.58 10.526h2.632v2.632H31.58zM13.158 13.158h2.632v2.632h-2.632zM34.211 13.158h2.632v2.632h-2.632zM10.527 15.79h2.632v2.632h-2.632zM31.58 15.79h2.632v2.632H31.58zM15.79 10.526h2.632v2.632H15.79zM36.843 10.526h2.632v2.632h-2.632zM15.79 15.79h2.632v2.632H15.79zM18.421 21.053h2.632v2.632h-2.632zM36.843 34.211h2.632v2.632h-2.632zM15.79 31.579h2.632v2.632H15.79zM26.316 21.053h2.632v2.632h-2.632z"
							/>
							<path
								fill="#000"
								d="M21.054 23.684h5.263v2.632h-5.263zM47.37 2.631H2.631V0H47.37zM47.37 42.106H2.631v-2.632H47.37zM50 2.96v36.514H47.37V2.96zM2.631 2.96v36.514H0V2.96zM31.58 31.579h5.263v2.632H31.58zM18.421 28.947h13.158v2.632H18.421zM36.843 15.79h2.632v2.632h-2.632z"
							/>
						</svg>
						Sorry, no results, try another{" "}
						<a href="/" className="text-blue hover:underline">
							search
						</a>
					</div>
				</div>

				<div className="max-w-6xl mx-auto flex justify-center mt-8">
					<p className="mb-4 text-xl">
						Do you think this is a mistake? Send us a{" "}
						<a
							target="_blank"
							rel="noreferrer noopener"
							href={tweetLink}
							className="font-bold underline"
						>
							tweet
						</a>{" "}
						and we'll try to fix it as soon as possible!
					</p>
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
	</>
	);
}
