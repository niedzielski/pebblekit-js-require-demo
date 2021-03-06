
#
# This file is the default set of rules to compile a Pebble project.
#
# Feel free to customize this to your needs.
#

import json
import os
import re

from waflib.Configure import conf

top = '.'
out = 'build'

def options(ctx):
    ctx.load('pebble_sdk')

def configure(ctx):
    ctx.load('pebble_sdk')

def build(ctx):
    ctx.load('pebble_sdk')

    build_worker = os.path.exists('worker_src')
    binaries = []
    js_target = ctx.concat_javascript(js_path='src/js')

    for p in ctx.env.TARGET_PLATFORMS:
        ctx.set_env(ctx.all_envs[p])
        ctx.set_group(ctx.env.PLATFORM_NAME)
        app_elf='{}/pebble-app.elf'.format(ctx.env.BUILD_DIR)
        ctx.pbl_program(source=ctx.path.ant_glob('src/**/*.c'),
        target=app_elf)

        if build_worker:
            worker_elf='{}/pebble-worker.elf'.format(ctx.env.BUILD_DIR)
            binaries.append({'platform': p, 'app_elf': app_elf, 'worker_elf': worker_elf})
            ctx.pbl_worker(source=ctx.path.ant_glob('worker_src/**/*.c'),
            target=worker_elf)
        else:
            binaries.append({'platform': p, 'app_elf': app_elf})

    ctx.set_group('bundle')
    ctx.pbl_bundle(binaries=binaries, js=js_target)


@conf
def concat_javascript(ctx, js_path=None):
    js_nodes = (ctx.path.ant_glob(js_path + '/**/*.js') +
                ctx.path.ant_glob(js_path + '/**/*.json') +
                ctx.path.ant_glob(js_path + '/**/*.coffee'))

    if not js_nodes:
        return []

    def concat_javascript_task(task):
        LOADER_PATH = "loader.js"
        LOADER_TEMPLATE = ("__loader.define({relpath}, {lineno}, " +
                           "function(exports, module, require) {{\n{body}\n}});")
        JSON_TEMPLATE = "module.exports = {body};"
        APPINFO_PATH = "appinfo.json"

        def loader_translate(source, lineno):
            return LOADER_TEMPLATE.format(
                relpath=json.dumps(source['relpath']),
                lineno=lineno,
                body=source['body'])

        def coffeescript_compile(relpath, body):
            try:
                import coffeescript
            except ImportError:
                ctx.fatal("""
    CoffeeScript file '%s' found, but coffeescript module isn't installed.
    You may try `pip install coffeescript` or `easy_install coffeescript`.
                """ % (relpath))
            body = coffeescript.compile(body)
            # change ".coffee" or ".js.coffee" extensions to ".js"
            relpath = re.sub('(\.js)?\.coffee$', '.js', relpath)
            return relpath, body

        sources = []
        for node in task.inputs:
            relpath = os.path.relpath(node.abspath(), js_path)
            with open(node.abspath(), 'r') as f:
                body = f.read()
                if relpath.endswith('.json'):
                    body = JSON_TEMPLATE.format(body=body)
                elif relpath.endswith('.coffee'):
                    relpath, body = coffeescript_compile(relpath, body)

                    compiled_js_path = os.path.join(out, js_path, relpath)
                    compiled_js_dir = os.path.dirname(compiled_js_path)
                    if not os.path.exists(compiled_js_dir):
                        os.makedirs(compiled_js_dir)
                    with open(compiled_js_path, 'w') as f:
                        f.write(body)

                if relpath == LOADER_PATH:
                    sources.insert(0, body)
                else:
                    sources.append({'relpath': relpath, 'body': body})

        with open(APPINFO_PATH, 'r') as f:
            body = JSON_TEMPLATE.format(body=f.read())
            sources.append({'relpath': APPINFO_PATH, 'body': body})

        sources.append('__loader.require("main");')

        with open(task.outputs[0].abspath(), 'w') as f:
            lineno = 1
            for source in sources:
                if type(source) is dict:
                    body = loader_translate(source, lineno)
                else:
                    body = source
                f.write(body + '\n')
                lineno += body.count('\n') + 1

    js_target = ctx.path.make_node('build/src/js/pebble-js-app.js')

    ctx(rule=concat_javascript_task,
        source=js_nodes,
        target=js_target)

    return js_target
