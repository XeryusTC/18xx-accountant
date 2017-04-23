When adding a player to the game:
================================
status: `400`
statusText: `"Bad Request"`
ok: `false`
url: `/api/player/`
type: `2`
text:
```
{"non_field_errors":["There is already a player with this name in your game"]}
```

When game doesn't exist
=======================
```
{
	_body: "{"detail":"Not found."}",
	status: 404,
	ok: false,
	statusText: "Not Found",
	headers: Object,
	type: 2,
	url: "/api/game/0ec72472-f7c7-4bcd-9b08-53b5db4e432b/"
}
```
