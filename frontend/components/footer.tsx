import { Logo } from "./logo";

const FooterLink = ({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) => (
  <a href={href} className="underline font-semibold">
    {children}
  </a>
);

export const Footer = () => (
  <footer className="max-w-7xl mx-auto px-10 py-5 flex justify-between align-middle">
    <Logo className="text-xl" />

    <div>
      Made by{" "}
      <FooterLink href="https://twitter.com/patrick91">
        Patrick Arminio
      </FooterLink>{" "}
      and{" "}
      <FooterLink href="https://twitter.com/burromarco">Marco Burro</FooterLink>
      . Design by{" "}
      <FooterLink href="https://twitter.com/druguinni">
        Orlando Festa
      </FooterLink>
      .
    </div>

    <div>
      <a href="https://github.com/patrick91/latest.cat">GitHub</a>
    </div>
  </footer>
);
