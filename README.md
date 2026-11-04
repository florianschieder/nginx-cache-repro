# proxy_cache: 502 "upstream sent too big header" for a window of URI lengths

## Summary

With `proxy_cache` enabled, requests whose URI length falls into a certain
window fail with **502** and `upstream sent too big header while reading
response header from upstream`, although the upstream's response headers are
small (a few hundred bytes).

The same request succeeds **without `proxy_cache`**.

Shorter URIs work, longer "do" too. By "do" I mean: nginx logs the
`proxy_buffer_size 4096 is not enough for cache key [...]` error message.

## Interpretation

It seems there is a window of URL size between "works" and "cache key does
not fit into the proxy buffer" that is not handled correctly by nginx.

## Reproduction

The reproduction script requires python and docker compose, and it will bind
to your local ports 1337 & 1338.

The nginx with the provided config can be started with `docker compose up`.

Running `reproduce.py` with `http://localhost:1337/` works (no cache involved).
Mind the trailing slashes! I know the reproduction implementation is not that
clean and beautiful, but at least it's deterministic.

Running it with `http://localhost:1338/` (cache involved) should result in
* HTTP 200 as long as `len(url) <= 3396`
* HTTP 502 for `3397 <= len(url) <= 3497`
* HTTP 200 for `len(url) > 3498` **but** nginx logs `proxy_buffer_size 4096 is not enough for cache key`
