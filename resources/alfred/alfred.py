import sys
from workflow import Workflow

__version__ = "0.17.0"

def main(wf):
    from dbnav import navigator

    wf.logger.debug('Args: %s', wf.args)

    items = navigator.run(wf.args)

    for item in items:
        wf.add_item(
            item.title(),
            item.subtitle(),
            uid=item.uid(),
            arg=item.value(),
            autocomplete=item.autocomplete(),
            valid=item.validity(),
            icon=item.icon())

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(
        libraries=["dbnav-{}-py2.7.egg".format(__version__)],
        update_settings={
            'github_slug': 'resamsel/dbnavigator',
            'version': __version__
        })
    sys.exit(wf.run(main))
