import json
import os
import logging
from pathlib import Path
from typing import Any, Dict, Annotated
import httpx
from fastapi import Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# Configure logging with basic config if not already configured
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    force=False  # Don't override if already configured
)

logger = logging.getLogger(__name__)


class Inertia:
    """Request-scoped Inertia renderer"""

    def __init__(self, request: Request, response: "InertiaResponse"):
        self.request = request
        self.response = response

    def render(self, component: str, props: Dict[str, Any] = None, errors: Dict[str, str] = None) -> JSONResponse | HTMLResponse:
        """Render an Inertia response without needing to pass request"""
        if props is None:
            props = {}
        return self.response.render(self.request, component, props, errors)

    def back(self, errors: Dict[str, str] = None) -> JSONResponse | HTMLResponse:
        """Redirect back with errors (for form validation)"""
        # Get the referring component from the request headers or props
        # For simplicity, we'll just re-render with errors
        # In a real implementation, you'd track the previous component
        return self.response.render(self.request, self.request.headers.get("X-Inertia-Component", "Home"), {}, errors)


class InertiaResponse:
    """Core Inertia protocol implementation"""

    def __init__(
        self,
        template_dir: str = "templates",
        vite_dev_url: str = "http://localhost:5173",
        manifest_path: str = "static/build/.vite/manifest.json"
    ):
        self.templates = Jinja2Templates(directory=template_dir)
        self.vite_dev_url = vite_dev_url
        self.manifest_path = manifest_path
        self._is_dev = None
        self._manifest = None

    def is_inertia_request(self, request: Request) -> bool:
        """Check if request is an Inertia XHR request"""
        return request.headers.get("X-Inertia") == "true"

    def is_dev_mode(self) -> bool:
        """Check if Vite dev server is running"""
        if self._is_dev is not None:
            return self._is_dev

        logger.info(f"Checking Vite dev server at {self.vite_dev_url}...")
        try:
            response = httpx.get(f"{self.vite_dev_url}/@vite/client", timeout=0.1)
            self._is_dev = response.status_code == 200
            if self._is_dev:
                logger.info("✓ Vite dev server detected - running in DEVELOPMENT mode")
            else:
                logger.info(f"✗ Vite dev server responded with {response.status_code} - running in PRODUCTION mode")
        except Exception as e:
            self._is_dev = False
            logger.info(f"✗ Vite dev server not reachable ({e.__class__.__name__}) - running in PRODUCTION mode")

        return self._is_dev

    def get_manifest(self) -> Dict[str, Any]:
        """Load Vite manifest for production builds"""
        if self._manifest is not None:
            return self._manifest

        manifest_file = Path(self.manifest_path)
        if manifest_file.exists():
            logger.info(f"Loading Vite manifest from {self.manifest_path}")
            with open(manifest_file) as f:
                self._manifest = json.load(f)
            logger.info(f"Manifest loaded with {len(self._manifest)} entry/entries")
        else:
            logger.warning(f"Vite manifest not found at {self.manifest_path} - no built assets available")
            self._manifest = {}

        return self._manifest

    def get_asset_version(self) -> str:
        """Get asset version for cache busting"""
        if self.is_dev_mode():
            return "dev"

        manifest = self.get_manifest()
        # Use hash of manifest as version
        return str(hash(json.dumps(manifest, sort_keys=True)))

    def get_vite_tags(self) -> str:
        """Generate script tags for Vite assets"""
        if self.is_dev_mode():
            # Development mode - use Vite dev server
            # React refresh preamble must come BEFORE Vite client
            logger.info(f"Generating DEV mode script tags (Vite server: {self.vite_dev_url})")
            return f'''
                <script type="module">
                    import RefreshRuntime from "{self.vite_dev_url}/@react-refresh"
                    RefreshRuntime.injectIntoGlobalHook(window)
                    window.$RefreshReg$ = () => {{}}
                    window.$RefreshSig$ = () => (type) => type
                    window.__vite_plugin_react_preamble_installed__ = true
                </script>
                <script type="module" src="{self.vite_dev_url}/@vite/client"></script>
                <script type="module" src="{self.vite_dev_url}/frontend/app.tsx"></script>
            '''
        else:
            # Production mode - use built assets from manifest
            manifest = self.get_manifest()
            entry = manifest.get('frontend/app.tsx', {})

            if not entry:
                logger.error("No entry found for 'frontend/app.jsx' in manifest - did you run 'npm run build'?")

            tags = []

            # Add CSS files
            css_files = entry.get('css', [])
            if css_files:
                logger.info(f"Generating PRODUCTION script tags - {len(css_files)} CSS file(s), entry: {entry.get('file', 'none')}")
            for css in css_files:
                tags.append(f'<link rel="stylesheet" href="/static/build/{css}">')

            # Add main JS file
            if 'file' in entry:
                tags.append(f'<script type="module" src="/static/build/{entry["file"]}"></script>')
            else:
                logger.warning("No JS entry file found in manifest!")

            return '\n'.join(tags)

    def render(self, request: Request, component: str, props: Dict[str, Any], errors: Dict[str, str] = None) -> JSONResponse | HTMLResponse:
        """
        Render an Inertia response.
        Returns JSON for Inertia requests, HTML for initial page loads.
        """
        page_data = {
            "component": component,
            "props": props,
            "url": str(request.url.path),
            "version": self.get_asset_version(),
        }

        # Add errors to page data if present
        if errors:
            page_data["props"]["errors"] = errors
            logger.debug(f"Rendering {component} with validation errors: {list(errors.keys())}")

        if self.is_inertia_request(request):
            # Return JSON response for Inertia XHR requests
            logger.info(f"→ Inertia XHR: {component} (props: {list(props.keys())})")
            return JSONResponse(
                content=page_data,
                headers={
                    "X-Inertia": "true",
                    "Vary": "X-Inertia",
                },
                status_code=422 if errors else 200
            )
        else:
            # Return HTML response for initial page load
            logger.info(f"→ Initial page load: {component} (props: {list(props.keys())})")
            return self.templates.TemplateResponse(
                "app.html",
                {
                    "request": request,
                    "page": json.dumps(page_data),
                    "vite_tags": self.get_vite_tags(),
                }
            )


# Singleton instance - created once on module import
# Note: This happens before main.py configures logging, so initial checks won't show logs
_inertia_response = InertiaResponse()
logger.info("Inertia module initialized")


def get_inertia(request: Request) -> Inertia:
    """FastAPI dependency to get request-scoped Inertia renderer"""
    return Inertia(request, _inertia_response)


# Type alias for dependency injection
InertiaDep = Annotated[Inertia, Depends(get_inertia)]
