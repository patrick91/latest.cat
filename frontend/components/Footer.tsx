export default function Footer() {
	return (
		<footer className="max-w-7xl mx-auto py-5 md:px-10 md:flex justify-between align-middle">
			<div>
				Made by{" "}
				<a className="underline font-semibold" href="https://twitter.com/patrick91">
					Patrick Arminio
				</a>{" "}
				and{" "}
				<a className="underline font-semibold" href="https://twitter.com/burromarco">
					Marco Burro
				</a>
				. Design by{" "}
				<a className="underline font-semibold" href="https://twitter.com/druguinni">
					Orlando Festa
				</a>
				. Cat illustrations by{" "}
				<a
					className="underline font-semibold"
					href="https://thenounproject.com/iconka/"
				>
					Denis Sazhin
				</a>
				.
			</div>

			<div className="md:block hidden">
				<a href="https://github.com/patrick91/latest.cat">GitHub</a>
			</div>
		</footer>
	);
}
