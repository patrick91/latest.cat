import butter


def root(title: str = None, children: butter.Component = None) -> butter.Component:
    return butter.html() > [
        butter.head()
        > [
            butter.title() > title or "latest.cat",
            butter.link(rel="preconnect", href="https://fonts.gstatic.com"),
            butter.link(
                href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@500&display=swap",
                rel="stylesheet",
            ),
            butter.style()
            > """
            input::-webkit-input-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input:-moz-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input::-moz-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input:-ms-input-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            """,
        ],
        butter.body(style="background: #D36582; padding: 50px;") > children,
    ]
