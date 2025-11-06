/**
 * Centralized Open Graph metadata configuration.
 * 
 * IMPORTANT: Keep this in sync with services/og_meta.py
 */

export interface OGMeta {
	title: string;
	description: string;
	url: string;
	image: string;
}

// Site-wide OG metadata constants
// SYNC WITH: services/og_meta.py
export const SITE_NAME = "latest.cat 🐱";
export const SITE_TAGLINE = "check latest versions of your favorite software";
export const SITE_DESCRIPTION =
	"Check the latest versions of your favorite programming languages, frameworks, and tools";

// OG Image dimensions (standard size)
export const OG_IMAGE_WIDTH = 1200;
export const OG_IMAGE_HEIGHT = 630;

export function getBaseUrl(): string {
	if (typeof window === "undefined") {
		return "https://latest.cat";
	}
	const isLocal = window.location.hostname === "localhost";
	return isLocal ? "http://localhost:8000" : "https://latest.cat";
}

export function getHomeOGMeta(): OGMeta {
	const baseUrl = getBaseUrl();
	return {
		title: `${SITE_NAME} - ${SITE_TAGLINE}`,
		description: SITE_DESCRIPTION,
		url: `${baseUrl}/`,
		image: `${baseUrl}/static/social-card.png`,
	};
}

export function getSoftwareOGMeta(
	softwareName: string,
	softwareSlug: string,
	version: string,
	path: string
): OGMeta {
	const baseUrl = getBaseUrl();
	return {
		title: `${softwareName} ${version} - ${SITE_NAME}`,
		description: `The latest version of ${softwareName} is ${version}`,
		url: `${baseUrl}${path}`,
		image: `${baseUrl}/og-image/${softwareSlug}.png`,
	};
}
