package latestcat

import (
	"bytes"
	"io"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"sync"

	"github.com/caddyserver/caddy/v2"
	"github.com/caddyserver/caddy/v2/caddyconfig/caddyfile"
	"github.com/caddyserver/caddy/v2/caddyconfig/httpcaddyfile"
	"github.com/caddyserver/caddy/v2/modules/caddyhttp"
)

var versionRe = regexp.MustCompile(`(?m)data-version="(?P<version>[^"]+)"`)

func isCurl(r *http.Request) bool {
	return strings.HasPrefix(r.UserAgent(), "curl")
}

func init() {
	caddy.RegisterModule(Middleware{})
	httpcaddyfile.RegisterHandlerDirective("curl_response", parseCaddyfile)
}

type Middleware struct {
	Enabled bool `json:"enabled,omitempty"`

	w io.Writer
}

func (Middleware) CaddyModule() caddy.ModuleInfo {
	return caddy.ModuleInfo{
		ID:  "http.handlers.curl_response",
		New: func() caddy.Module { return new(Middleware) },
	}
}

func (m *Middleware) Provision(ctx caddy.Context) error {
	return nil
}

func (m *Middleware) Validate() error {
	return nil
}

func (m Middleware) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if !m.Enabled || !isCurl(r) || r.URL.Path == "/graphql" {
		return next.ServeHTTP(w, r)
	}

	if r.URL.Path == "/" {
		w.Write([]byte("Welcome to latest.cat, try running curl -Lfs latest.cat/python"))
	}

	respBuf := bufPool.Get().(*bytes.Buffer)
	respBuf.Reset()
	defer bufPool.Put(respBuf)

	tempWriter := &TempResponseWriter{}

	shouldBuf := func(_ int, _ http.Header) bool { return true }

	rec := caddyhttp.NewResponseRecorder(tempWriter, respBuf, shouldBuf)

	err := next.ServeHTTP(rec, r)

	if err != nil {
		return err
	}

	if !rec.Buffered() {
		return nil
	}

	response := rec.Buffer().String()

	result := versionRe.FindAllStringSubmatch(response, -1)

	var version string

	if len(result) > 0 {
		version = result[0][1]
	} else {
		version = "unknown"
	}

	updatedResponse := []byte(version)

	for k, v := range tempWriter.Header() {
		w.Header().Set(k, v[0])
	}

	// make sure the content-length header is updated
	w.Header().Set("Content-Length", strconv.Itoa(len(updatedResponse)))

	if version == "unknown" {
		w.WriteHeader(404)
	} else {
		w.WriteHeader(200)
	}

	w.Write(updatedResponse)

	return nil
}

func (m *Middleware) UnmarshalCaddyfile(d *caddyfile.Dispenser) error {
	for d.Next() {
		args := d.RemainingArgs()

		switch len(args) {
		case 1:
			value, err := strconv.ParseBool(args[0])

			if err != nil {
				return d.Err("unable to parse boolean value")
			}

			m.Enabled = value
		default:
			return d.Err("unexpected number of arguments")
		}
	}

	return nil
}

func parseCaddyfile(h httpcaddyfile.Helper) (caddyhttp.MiddlewareHandler, error) {
	var m Middleware
	err := m.UnmarshalCaddyfile(h.Dispenser)
	return m, err
}

var bufPool = sync.Pool{
	New: func() interface{} {
		return new(bytes.Buffer)
	},
}

type TempResponseWriter struct {
	header http.Header
}

func (w *TempResponseWriter) Header() http.Header {
	if w.header == nil {
		w.header = make(http.Header)
	}

	return w.header
}

func (w *TempResponseWriter) Write(b []byte) (int, error) {
	return 0, nil
}

func (w *TempResponseWriter) WriteHeader(status int) {
}

// Interface guards
var (
	_ caddy.Provisioner           = (*Middleware)(nil)
	_ caddy.Validator             = (*Middleware)(nil)
	_ caddyhttp.MiddlewareHandler = (*Middleware)(nil)
	_ caddyfile.Unmarshaler       = (*Middleware)(nil)
)
