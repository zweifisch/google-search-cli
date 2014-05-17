# google-search-cli

* works like a shell
* changing keywords without quiting
* socks proxy support
* does not handle urls(leave it to termial emulator)

## setup

```sh
pip install google-search-cli
```

## usage

```sh
google-search keyword keyword2
```

using socks5 proxy, `http_proxy` should also work

```sh
SOCKS_SERVER=127.0.0.1:9090 google-search
```

## the google api

```sh
curl -Gs \
	-d v=1.0 \
	-d start=0 \
	-d rsz=3 \
	--data-urlencode q=keyword \
	http://ajax.googleapis.com/ajax/services/search/web
```
