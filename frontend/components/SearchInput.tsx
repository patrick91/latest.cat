export default function SearchInput() {
	return (
		<div className="border text-2xl md:text-4xl font-heading bg-white border-black rounded-full shadow-drop flex">
			<search className="contents">
				<input
					name="search"
					placeholder="Python"
					className="overflow-hidden bg-transparent pl-12 py-8 flex-1 min-w-0 outline-none focus-visible:underline dark:text-black"
				/>
				<button
					type="submit"
					className="px-4 md:px-12 py-8 font-heading font-bold rounded-full hover:bg-gray text-black flex-shrink-0"
				>
					Search
				</button>
			</search>
		</div>
	);
}
