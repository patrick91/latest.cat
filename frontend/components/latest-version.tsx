export const LatestVersion = ({
  software,
  version,
}: {
  software: string;
  version: string;
}) => (
  <div
    className="
      border text-4xl font-heading font-black bg-mint border-black rounded-full shadow-drop px-12 py-8
      text-center inline-block text-black
    "
  >
    latest version for <span className="text-blue">{software}</span> is{" "}
    <span className="text-blue">{version}</span>
  </div>
);
