export const Command = ({ text }: { text: string }) => (
  <div className="mb-4 flex overflow-scroll md:overflow-auto w-full">
    <span className="mr-2 sm:mr-4 select-none">$</span>
    <pre>
      <code>{text}</code>
    </pre>
    <button
      onClick={() => navigator.clipboard.writeText(text)}
      className="ml-auto px-2 py-1 font-heading font-medium rounded-full hidden sm:inline hover:bg-gray text-black transition active:bg-dark-gray active:text-white items-center"
    >
      Copy
    </button>
  </div>
);
