export const Command = ({ text }: { text: string }) => (
  <div className="flex flex-col sm:flex-row items-baseline justify-between">
    <div className="mb-4 flex overflow-auto">
      <span className="mr-4 select-none">$</span>
      <pre>
        <code>{text}</code>
      </pre>
    </div>
    <button
      onClick={() => navigator.clipboard.writeText(text)}
      className="px-2 py-1 font-heading font-medium rounded-full hover:bg-gray text-black transition active:bg-dark-gray active:text-white"
    >
      Copy
    </button>
  </div>
);
