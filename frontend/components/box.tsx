import cx from "classnames";

export const Box = ({
  title,
  children,
  className,
}: {
  title: string;
  className?: string;
  children: React.ReactNode;
}) => (
  <div
    className={cx(
      "shadow-drop rounded-[40px] px-5 py-5 ",
      "border border-black dark:bg-dark-gray md:grid grid-cols-[1fr_2fr]",
      className
    )}
  >
    <h1 className="font-heading text-4xl font-bold mt-5 mb-10 md:m-0 md:text-5xl md:px-10 md:flex items-center">
      {title}
    </h1>
    <div className="text-2xl">{children}</div>
  </div>
);
