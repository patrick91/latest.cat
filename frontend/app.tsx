import { createRoot } from "react-dom/client";
import { createInertiaApp } from "@inertiajs/react";
import "./index.css";

createInertiaApp({
	resolve: (name) => {
		const pages = import.meta.glob("./Pages/**/*.tsx", { eager: true });
		const page = pages[`./Pages/${name}.tsx`] as any;
		return page.default;
	},
	setup({ el, App, props }) {
		createRoot(el).render(<App {...props} />);
	},
});
