import cx from "classnames";

export const Logo = ({ className }: { className?: string }) => (
  <h1 className={cx("font-heading font-bold text-2xl", className)}>
    latest.cat
  </h1>
);
