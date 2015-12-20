# PebbleKit JS `require` demo
Adds `require` support to PebbleKit JS. This project is a super mini version of
[Pebble.js](https://github.com/pebble/pebblejs) for PebbleKit JS projects using
Pebble SDK v3.8.1. This project is untested in
[CloudPebble](https://cloudpebble.net/).

## Steps to add `require` support to your PebbleKit JS project

### Verify this repo still works
1. Clone this repo: `git clone https://github.com/niedzielski/pebblekit-js-require-demo.git`
1. Build and install the repo to make sure it still works:
```bash
$ cd pebblekit-js-require-demo &&
  pebble build &&
  pebble install --emulator chalk --logs
...
[13:42:59] javascript> Hello world! - Sent from your javascript application. Woo!
```
1. Cool. Now you're confident this can work.

### Update your project
1. Commit any unsaved changes.
1. Move your project's `src/js/pebble-js-app.js` to `src/js/app/index.js`.
1. Remove any ready event listener from `src/js/app/index.js`. `index.js` will
   be loaded when the ready event is emitted.
1. Copy `src/js/loader.js` and `src/js/main.js` from this repo to your project's `src/js/`.
1. If you haven't made changes to your `wscript`, replace it with the version from this repo. If you have made changes, only add the
[deltas](https://github.com/niedzielski/pebblekit-js-require-demo/commit/5aae361efb7b4754fc1a47d02eae55f799ec0651#diff-dc6134e3d3c869a052520d86f46371dc).
1. When adding new modules, place them under `src/js/app/` and `require('./name')` will work.

## License (MIT)
Portions of wscript and all of src/js/loader.js copied from Pebble.js which is
distributed under an [MIT license](https://github.com/pebble/pebblejs/blob/master/LICENSE).
All other files are released under public domain.

[0] https://developer.getpebble.com/docs/