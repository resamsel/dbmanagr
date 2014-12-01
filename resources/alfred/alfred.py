import sys
from workflow import Workflow

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
    wf = Workflow(libraries=['dbnav-0.16-py2.7.egg'])
    sys.exit(wf.run(main))
