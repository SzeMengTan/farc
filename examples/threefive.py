#!/usr/bin/env python3


import asyncio
from time import sleep

import pq


class Three(pq.Ahsm):

    @pq.Hsm.state
    def initial(me, event):
        print("Three initial")
        me.te = pq.TimeEvent("TICK3")
        return me.tran(me, Three.running)


    @pq.Hsm.state
    def running(me, event):
        sig = event.signal
        if sig == pq.Signal.ENTRY:
            print("three enter")
            me.te.postEvery(me, 3)
            return me.handled(me, event)

        elif sig == pq.Signal.TICK3:
            print("three tick")
            sleep(0.10)
            return me.handled(me, event)

        elif sig == pq.Signal.EXIT:
            print("three exit")
            me.te.disarm()
            return me.handled(me, event)

        return me.super(me, me.top)


class Five(pq.Ahsm):

    @pq.Hsm.state
    def initial(me, event):
        print("Five initial")
        me.te = pq.TimeEvent("TICK5")
        return me.tran(me, Five.running)


    @pq.Hsm.state
    def running(me, event):
        sig = event.signal
        if sig == pq.Signal.ENTRY:
            print("five enter")
            me.te.postEvery(me, 5)
            return me.handled(me, event)

        elif sig == pq.Signal.TICK5:
            print("five tick")
            sleep(0.20)
            return me.handled(me, event)

        elif sig == pq.Signal.EXIT:
            print("five exit")
            me.te.disarm()
            return me.handled(me, event)

        return me.super(me, me.top)


if __name__ == "__main__":
    pq.Spy.enable_spy(pq.VcdSpy)

    three = Three(Three.initial)
    five = Five(Five.initial)

    three.start(3)
    five.start(5)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pq.Framework.stop()
    loop.close()
