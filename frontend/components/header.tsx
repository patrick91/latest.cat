import Link from "next/link";
import { useCallback } from "react";
import { Logo } from "./logo";
import { Toggle } from "./toggle";
import { getCookie, setCookies } from "cookies-next";

export const Header = () => {
  const isDarkModeEnabled = getCookie("darkMode") === true;

  const toggleDarkMode = useCallback((value: boolean) => {
    setCookies("darkMode", value);

    if (value) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  return (
    <header className="max-w-7xl mx-auto px-10 py-5 flex justify-between align-middle">
      <Link href="/">
        <Logo />
      </Link>

      <div className="text-2xl">🐾</div>

      <Toggle onToggle={toggleDarkMode} checked={isDarkModeEnabled} />
    </header>
  );
};
