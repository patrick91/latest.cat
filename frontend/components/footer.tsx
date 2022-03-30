import { Logo } from "./logo";
import { Toggle } from "./toggle";

export const Footer = () => (
  <footer className="max-w-7xl mx-auto px-10 py-5 flex justify-between align-middle">
    <Logo className="text-xl" />

    <div>
      Made by <a href="https://twitter.com/patrick91">Patrick Arminio</a> and{" "}
      <a href="https://twitter.com/burromarco">Marco Burro</a>
    </div>

    <div>
      <a href="https://github.com/patrick91">GitHub</a>
    </div>
  </footer>
);
