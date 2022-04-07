export const Meta = ({
  title,
  path,
  description = "Ever struggled to find the latest version of a programming language? latest.cat is a simple, fast and free way to browse the latest releases of your favorite programming language.",
}: {
  path: string;
  title: string;
  description?: string;
}) => {
  const url = `https://latest.cat${path}`;

  return (
    <>
      <title>{title}</title>
      <meta name="title" content={title} />
      <meta name="description" content="" />

      <meta property="og:type" content="website" />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content="" />

      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={url} />
      <meta property="twitter:title" content={title} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content="/social-card.png" />
    </>
  );
};
