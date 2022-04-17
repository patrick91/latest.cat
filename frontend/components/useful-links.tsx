import cx from "classnames";

const TitleBox = () => (
  <div
    className="
    bg-corn border-2 border-black text-center inline p-2 px-4 font-bold
      absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2
    "
  >
    Useful links
  </div>
);

export const Link = ({
  url,
  children,
  className,
}: {
  url: string;
  className?: string;
  children: React.ReactNode;
}) => (
  <a
    href={url}
    target="_blank"
    rel="noopener noreferrer"
    className={cx(
      "block border-2 border-black shadow-drop rounded-full p-4 font-bold text-xl mb-4 md:mr-4",
      className
    )}
  >
    {children}
  </a>
);

const Diamond = ({ className }: { className?: string }) => (
  <div
    className={cx(
      "w-8 h-8 bg-[#ececec] border border-black rotate-45 absolute",
      "top-1/2 -translate-y-1/2",
      className
    )}
  ></div>
);

const toTitleCase = (str: string) =>
  str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase();
  });

export const UsefulLinks = ({
  links,
}: {
  links: {
    title: string;
    url: string;
  }[];
}) => (
  <div
    className="
      mt-4 bg-opacity-60 bg-white border-2 border-cosmos rounded-3xl md:rounded-full relative
      px-5 md:px-10 py-14 dark:text-black w-full mx-5 md:mx-auto md:w-auto
    "
  >
    <TitleBox />

    <Diamond className="left-0 -translate-x-1/2 hidden md:block" />
    <Diamond className="right-0 translate-x-1/2 hidden md:block" />

    <div className="md:flex justify-around flex-wrap">
      {links.map(({ title, url }, index) => (
        <Link
          key={index}
          url={url}
          className={cx({
            "bg-gold": (index + 1) % 1 === 0,
            "bg-turquoise": (index + 1) % 2 === 0,
            "bg-spring-bud": (index + 1) % 3 === 0,
          })}
        >
          {toTitleCase(title)}
        </Link>
      ))}
    </div>
  </div>
);
