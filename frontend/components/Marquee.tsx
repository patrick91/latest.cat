interface Release {
	name: string;
	url: string;
}

interface MarqueeProps {
	releases: Release[];
}

function loop<T>(items: T[], min: number = 10): T[] {
	let newItems = [...items];

	while (newItems.length < min) {
		newItems = newItems.concat(items);
	}

	return newItems;
}

export default function Marquee({ releases: originalReleases }: MarqueeProps) {
	const releases = loop(originalReleases);

	return (
		<div className="marquee bg-yellow uppercase dark:bg-dark-purple dark:text-white font-heading text-2xl overflow-hidden">
			<div className="inner flex w-fit py-6">
				{releases.map((release, index) => (
					<div key={index} className="mr-10 flex-shrink-0">
						<a className="hover:underline" href={release.url}>
							&#8226; {release.name} Released
						</a>
					</div>
				))}
			</div>
			<style jsx>{`
				.marquee {
					--offset: 20vw;
					--move-initial: calc(-25% + var(--offset));
					--move-final: calc(-50% + var(--offset));
				}

				.inner {
					transform: translate3d(var(--move-initial), 0, 0);
					animation: marquee 30s linear infinite;
					animation-play-state: running;
				}

				.inner:hover {
					animation-play-state: paused;
				}

				@keyframes marquee {
					0% {
						transform: translate3d(var(--move-initial), 0, 0);
					}

					100% {
						transform: translate3d(var(--move-final), 0, 0);
					}
				}
			`}</style>
		</div>
	);
}
