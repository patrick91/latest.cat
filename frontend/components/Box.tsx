interface BoxProps {
	title: string;
	className?: string;
	children: React.ReactNode;
}

export default function Box({ title, className = "", children }: BoxProps) {
	return (
		<div
			className={`shadow-drop rounded-[40px] px-5 py-5 border border-black dark:bg-dark-gray lg:grid grid-cols-[1fr_2fr] gap-4 ${className}`}
		>
			<h1 className="font-heading text-4xl font-bold mt-5 mb-10 lg:m-0 lg:text-5xl lg:flex items-center md:text-center">
				{title}
			</h1>
			<div className="text-2xl">{children}</div>
		</div>
	);
}
