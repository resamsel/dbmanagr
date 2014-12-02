import sys
from workflow import Workflow

__version__ = "0.17.0"

def main(wf):
    from dbnav import navigator

    wf.logger.debug('Args: %s', wf.args)

    items = navigator.run(wf.args)

    for item in items:
        wf.logger.debug('Item: %s', item.__class__)
        wf.add_item(
            item.title(),
            item.subtitle(),
            uid=item.uid(),
            arg=item.value(),
            autocomplete=item.autocomplete(),
            valid=item.validity(),
            icon=item.icon())

    wf.logger.debug('Sending feedback')

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(
        libraries=["dbnav-{}-py2.7.egg".format(__version__)],
        update_settings={
            # Your username and the workflow's repo's name
            'github_slug': 'resamsel/dbnavigator',
            # The version (i.e. release/tag) of the installed workflow
            'version': __version__
        })
    sys.exit(wf.run(main))
