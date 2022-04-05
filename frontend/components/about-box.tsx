import { Box } from "./box";

export const AboutBox = () => (
  <Box title="What is latest.cat?" className="mb-10 bg-green">
    <p className="mb-4 font-bold">
      Ever struggled to find the latest version of a programming language?
    </p>
    <p className="mb-4">
      <strong className="font-bold">latest.cat</strong> is a simple, fast and
      free way to browse the latest releases of your favorite programming
      language.
    </p>
    <p className="mb-4">
      Type your favorite programming language name in the search bar, hit enter
      and you will immediately see the latest releases of that programming
      language.
    </p>
    <p className="mb-4">
      You can even use <strong className="font-bold">latest.cat</strong> from
      the command line!
    </p>
  </Box>
);
