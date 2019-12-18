# encoding: utf-8

import logging

import ckan.plugins as p
import click
from ckan.cli import config_tool
from ckan.cli import (
    jobs,
    front_end_build,
    click_config_option, db, load_config, search_index, server,
    profile,
    asset,
    sysadmin,
    translation,
    dataset,
    views,
    plugin_info,
    notify,
    tracking,
    minify,
    less,
    generate,
    user
)

from ckan.config.middleware import make_app
from ckan.cli import seed

log = logging.getLogger(__name__)


class CustomGroup(click.Group):
    def get_command(self, ctx, name):
        cmd = super(CustomGroup, self).get_command(ctx, name)
        if not cmd:
            self.invoke(ctx)
            cmd = super(CustomGroup, self).get_command(ctx, name)
        return cmd


class CkanCommand(object):

    def __init__(self, conf=None):
        self.config = load_config(conf)
        self.app = make_app(self.config.global_conf, **self.config.local_conf)


@click.group(
    invoke_without_command=True,
    cls=CustomGroup
)
@click.help_option(u'-h', u'--help')
@click_config_option
@click.pass_context
def ckan(ctx, config, *args, **kwargs):
    ctx.obj = CkanCommand(config)
    for plugin in p.PluginImplementations(p.IClick):
        for cmd in plugin.get_commands():
            ckan.add_command(cmd)


ckan.add_command(jobs.jobs)
ckan.add_command(config_tool.config_tool)
ckan.add_command(front_end_build.front_end_build)
ckan.add_command(server.run)
ckan.add_command(profile.profile)
ckan.add_command(seed.seed)
ckan.add_command(db.db)
ckan.add_command(search_index.search_index)
ckan.add_command(sysadmin.sysadmin)
ckan.add_command(asset.asset)
ckan.add_command(translation.translation)
ckan.add_command(dataset.dataset)
ckan.add_command(views.views)
ckan.add_command(plugin_info.plugin_info)
ckan.add_command(notify.notify)
ckan.add_command(tracking.tracking)
ckan.add_command(minify.minify)
ckan.add_command(less.less)
ckan.add_command(generate.generate)
ckan.add_command(user.user)
