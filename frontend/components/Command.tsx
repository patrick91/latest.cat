import { useEffect, useRef } from "react";

interface CommandProps {
	text: string;
}

export default function Command({ text }: CommandProps) {
	const audioRef = useRef<HTMLAudioElement | null>(null);

	useEffect(() => {
		// Preload audio on component mount
		if (!audioRef.current) {
			const audio = new Audio("/meow.wav");
			audio.preload = "auto";
			audio.volume = 0.2;
			audioRef.current = audio;
		}
	}, []);

	const handleCopy = () => {
		navigator.clipboard.writeText(text);
		if (audioRef.current) {
			audioRef.current.play();
		}
	};

	return (
		<div className="mb-4 flex overflow-scroll md:overflow-auto w-full">
			<span className="mr-2 sm:mr-4 select-none">$</span>
			<pre>
				<code>{text}</code>
			</pre>
			<button
				onClick={handleCopy}
				className="copy-command ml-auto px-2 py-1 font-heading font-medium rounded-full hidden sm:inline hover:bg-gray text-black transition active:bg-dark-gray active:text-white items-center dark:text-white dark:hover:text-black"
			>
				Copy
			</button>
		</div>
	);
}
