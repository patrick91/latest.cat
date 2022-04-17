import { Header } from "./header";
import { Logo } from "./logo";
import { SearchInput } from "./search-input";

import * as React from "react";

const Background = () => (
  <svg
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className="absolute top-0 left-0 w-full h-full"
    preserveAspectRatio="xMinYMid slice"
    viewBox="0 0 1403 930"
  >
    <path
      d="m605.013 901.238-14.787-219.503 141.368 118.767L719.765 624.9l172.158 142.752M63.947-210l184.11 318.888-299.996-74.177L95.35 289.82l-363.946-87.504"
      stroke="#000"
      strokeOpacity={0.6}
      strokeWidth={54}
      strokeLinecap="square"
      strokeLinejoin="round"
      style={{
        mixBlendMode: "overlay",
      }}
    />
    <circle
      cx={544}
      cy={229}
      r={112}
      stroke="#000"
      strokeWidth={54}
      style={{
        mixBlendMode: "overlay",
      }}
    />
    <circle
      cx={1347.5}
      cy={608.5}
      r={41.5}
      stroke="#000"
      strokeWidth={28}
      style={{
        mixBlendMode: "overlay",
      }}
    />
    <path
      d="M164.22 686.796c-87.469-50.5-17.995-192.832 79-136.832"
      stroke="#000"
      strokeWidth={49}
      strokeLinecap="round"
      style={{
        mixBlendMode: "overlay",
      }}
    />
    <path
      d="M1205.61 218.958c-51.11 29.51-102.84-47.234-46.16-79.958"
      stroke="#000"
      strokeWidth={29}
      strokeLinecap="round"
      style={{
        mixBlendMode: "overlay",
      }}
    />
  </svg>
);

export const Hero = ({ children }: { children?: React.ReactNode }) => (
  <div className="bg-pink pb-20 relative overflow-hidden dark:bg-dark dark:text-white">
    <div className="relative z-10">
      <Header />

      <div className="max-w-xl mx-auto text-center mt-20 mb-20">
        <Logo className="text-6xl md:text-7xl mb-5" />

        <p className="text-4xl font-sans px-5 md:px-0">
          Find the latest version of your favourite software
        </p>
      </div>

      {children}
    </div>

    <Background />
  </div>
);
