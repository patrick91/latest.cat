export const Toggle = ({
  onToggle,
}: {
  onToggle: (value: boolean) => void;
}) => (
  <div
    className="
        border border-black rounded-full shadow-drop-sm w-12 h-8 px-1 self-baseline flex justify-center
        relative flex-col
      "
  >
    <label
      htmlFor="dark-mode-toggle"
      className="absolute opacity-0 top-0 left-0 right-0 bottom-0 block cursor-pointer"
    ></label>

    <input
      type="checkbox"
      id="dark-mode-toggle"
      className="peer hidden"
      onClick={(event) => {
        // @ts-ignore
        onToggle(event.target.checked);
      }}
    />

    <div
      className="
          w-6 h-6 border-black bg-white border rounded-full shadow-drop-sm peer-checked:self-end
        "
    ></div>
  </div>
);
