#!/usr/bin/env python
# -*- coding: utf-8 -*-

STOP = object()

class Process(object):
    def __init__(self, events, init_state, trans_func):
        self.state = init_state
        self.events = events
        self.trans_func = trans_func

    def reset(self, state):
        self.state = state

    def occur(self, event):
        print('EVENT {0} occur'.format(event))
        if event not in self.events:
            return

        try:
            new_state = self.trans_func(self.state, event)
        except KeyError:
            print('RUNTIME ERROR')
            return

        if new_state == -1:
            print('   V')
            print('  TRANSITION: {0} to STOP'.format(self.state))
            print('   V')
            print('STOP!')
            return
        else:
            print('   V')
            print('  TRANSITION: {0} to {1}'.format(self.state, new_state))
            print('   V')
        self.state = new_state
        return self


class Parallel(object):
    def __init__(self, *arg):
        self.processes = arg

    def occur(self, event):
        for p in self.processes:
            p.occur(event)


def main():
    # A -> B -> A -> STOP
    def trans(state, event):
        """return next state

        causes ValueError when the next state is not defined
        """
        table = {(0, 'A'): 1,
                 (1, 'B'): 2,
                 (2, 'A'): -1}
        return table[(state, event)]

    proc = Process(('A', 'B'), 0, trans)
    print('### first process ###')
    proc.occur('A').occur('B').occur('A')

    print('### second process ###')
    proc = Process(('A', 'B'), 0, trans)
    proc.occur('B')

    # A -> B -> [restart]
    def trans2(state, event):
        table = {(0, 'A'): 1,
                 (1, 'B'): 0}
        return table[(state, event)]

    proc = Process(('A', 'B'), 0, trans2)
    print('### third process ###')
    proc.occur('A').occur('B').occur('A').occur('B')

    print('### fourth process ###')
    proc.reset(0)
    proc.occur('A').occur('A')

if __name__ == '__main__':
    main()
