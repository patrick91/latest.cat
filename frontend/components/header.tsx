import { useCallback } from "react";
import { Logo } from "./logo";
import { Toggle } from "./toggle";

export const Header = () => {
  const toggleDarkMode = useCallback((value: boolean) => {
    console.log("Toggle Dark Mode");
    // change class of html element
    if (value) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  return (
    <header className="max-w-7xl mx-auto px-10 py-5 flex justify-between align-middle">
      <Logo />

      <div className="text-2xl">🐾</div>

      <Toggle onToggle={toggleDarkMode} />
    </header>
  );
};
