from starlette.responses import HTMLResponse

import butter
from butter.render import render
from components.cat import cat
from components.layout import root
from components.logo import logo
from components.title import title


async def homepage(request):
    content = root(
        title="latest.cat - find the latest version of your favourite software"
    ) > [
        butter.div()
        > [
            logo(),
            title() > "find the latest version of your favourite software ✨",
            butter.form(action="/search", method="get")
            > [
                butter.input(
                    id="search-input",
                    name="q",
                    placeholder="python",
                    style=(
                        "font-family: inconsolata; font-size: 40px; background: none; border: none; "
                        "border-bottom: 4px solid currentColor; outline: none; color: #253C78; margin-top: 30px; "
                    ),
                ),
                butter.button(
                    style="border: none; background: none; font-size: 40px; cursor: pointer; margin-left: 20px;"
                )
                > "👉",
            ],
        ],
        cat(style="position: absolute; bottom: 0; right: 0;"),
        butter.script()
        > r"""
            const input = document.querySelector('#search-input');
            const clone = document.createElement('pre');
            clone.style.position = 'absolute';
            clone.style.top = '-100vh';
            clone.style.left = '-100vw';
            clone.style.width = 'auto';
            clone.style.whitespace = 'pre';

            function getKey(e) {
                if (e.type !== 'keydown') {
                    return '';
                }

                if (e.key.length > 2) {
                    return '';
                }

                return e.key;
            }

            function fit(e) {
                input.scrollLeft = 0;

                let text = input.value ? input.value + getKey(e) : input.placeholder;
                text = text.replace(/"/g, '&quot;')
                    .replace(/'/g, '&#39;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/\./g, 'l')
                    .replace(/ /g, '<span> </span>');

                clone.innerHTML = text;

                const inputStyles = getComputedStyle(input);

                clone.style.fontSize = inputStyles.fontSize;
                clone.style.fontFamily = inputStyles.fontFamily;
                clone.style.fontWeight = inputStyles.fontWeight;
                clone.style.letterSpacing = inputStyles.letterSpacing;
                clone.style.textTransform = inputStyles.textTransform;

                input.scrollLeft = 0;
                input.style.width = Math.max(130, clone.getBoundingClientRect().width + 10);
            }

            document.documentElement.appendChild(clone);
            fit({});
            input.addEventListener('blur', fit);
            input.addEventListener('focus', fit);
            input.addEventListener('change', fit);
            input.addEventListener('keydown', fit);
            input.addEventListener('keyup', fit);
        """,
    ]

    return HTMLResponse(render(content))
