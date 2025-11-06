import { Head, router } from "@inertiajs/react";
import Hero from "../components/Hero";
import Footer from "../components/Footer";
import SearchInput from "../components/SearchInput";
import AboutBox from "../components/AboutBox";
import Box from "../components/Box";
import Command from "../components/Command";
import LatestReleasesMarquee from "../components/LatestReleasesMarquee";
import { getHomeOGMeta } from "../utils/ogMeta";

interface HomeProps {
	latestReleases: { name: string; url: string }[];
}

export default function Home({ latestReleases }: HomeProps) {
	console.log("Home component props:", { latestReleases });
	
	const ogMeta = getHomeOGMeta();
	
	const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		const formData = new FormData(e.currentTarget);
		const search = formData.get("search") as string;
		if (search) {
			router.visit(`/${search}`);
		}
	};

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
				<div className="max-w-2xl mx-auto w-11/12">
					<form onSubmit={handleSubmit}>
						<SearchInput />
					</form>
				</div>
			</Hero>

			<LatestReleasesMarquee releases={latestReleases} />

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
							<Command text="curl -Lfs latest.cat/python@3.11" />
						</div>
					</Box>

					<div className="mt-10">
						<Footer />
					</div>
				</div>
			</div>
		</div>
	</>
	);
}
