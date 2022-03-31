export const SearchInput = () => (
  <div className="border text-4xl font-heading bg-white border-black rounded-full shadow-drop flex">
    <input
      type="search"
      name="software"
      placeholder="Python"
      className="overflow-hidden bg-transparent pl-12 py-8 flex-1 outline-none focus-visible:underline"
    />
    <button className="px-12 py-8 font-heading font-bold rounded-full hover:bg-gray-200 text-black">Search</button>
  </div>
);
