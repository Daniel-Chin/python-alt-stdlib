'''
e.g. Context managers to enter tags.  
'''
import typing as tp
from html.parser import HTMLParser
from enum import Enum
from dataclasses import dataclass
from contextlib import contextmanager

class EventType(Enum):
    StartTag = 'StartTag'
    EndTag = 'EndTag'
    Data = 'Data'

Attrs = tp.List[tp.Tuple[str, tp.Optional[str]]]

@dataclass(frozen=True)
class Event:
    type: EventType
    text: str
    attrs: tp.Optional[Attrs]

    def __repr__(self):
        buf = ['event: ']
        if self.type == EventType.StartTag:
            buf.append('<')
            buf.append(self.text)
            assert self.attrs is not None
            for k, v in self.attrs:
                buf.append(f' {k}={v}')
            buf.append('>')
        elif self.type == EventType.EndTag:
            buf.append('</')
            buf.append(self.text)
            buf.append('>')
        elif self.type == EventType.Data:
            buf.append('data ')
            buf.append(repr(self.text))
        else:
            assert False, self.type
        return ''.join(buf)

class ParseToList(HTMLParser):
    # RAM-heavy
    def __init__(self, **kw):
        super().__init__(**kw)
        self.events: tp.List[Event] = []

    def handle_starttag(self, tag: str, attrs: Attrs):
        self.events.append(Event(EventType.StartTag, tag, attrs))

    def handle_endtag(self, tag: str):
        self.events.append(Event(EventType.EndTag, tag, None))

    def handle_data(self, data: str):
        self.events.append(Event(EventType.Data, data, None))

TypeIterEvents = tp.Iterator[tp.Tuple[tp.List[str], Event]]
def IterEvents(
    webpage: str, 
    subscribe_tags: tp.List[str], subscribe_attrs: tp.List[str], 
) -> TypeIterEvents:
    parser = ParseToList()
    parser.feed(webpage)
    parser.close()
    stack: tp.List[str] = []
    for event in parser.events:
        if event.type in (EventType.StartTag, EventType.EndTag):
            tag = event.text
            if tag not in subscribe_tags:
                continue
            if   event.type == EventType.StartTag:
                assert event.attrs is not None
                stack.append(tag)
                yield stack, Event(event.type, tag, [(k, v) for (k, v) in event.attrs if k in subscribe_attrs])
                continue
            elif event.type == EventType.EndTag:
                popped = stack.pop()
                assert tag == popped, (tag, popped)
                yield stack, event
                continue
            elif event.type == EventType.Data:
                yield stack, event
        elif event.type == EventType.Data:
            yield stack, event
        else:
            assert False, event.type

class UnexpectedEndTag(Exception): 
    def __init__(self, tag: str, sentinel: int):
        self.tag = tag
        self.sentinel = sentinel

class ParseContext:
    def __init__(
        self, 
        webpage: str, 
        subscribe_tags: tp.List[str], subscribe_attrs: tp.List[str], 
    ):
        self.subscribe_tags = subscribe_tags
        self.subscribe_attrs = subscribe_attrs
        self.iterEvents = IterEvents(webpage, subscribe_tags, subscribe_attrs)
        self.sentinels: tp.List[int] = [-1]
    
    def seekTag(self, eventType: EventType, tag: str, debug: bool = False, **attrs: str):
        if debug:
            print('  seeking', eventType, tag, attrs)
        attrs = {k.strip('_'): v for k, v in attrs.items()}
        assert tag in self.subscribe_tags
        for k, v in attrs.items():
            assert k in self.subscribe_attrs
        while True:
            stack, nowEvent = self.next(debug)
            if nowEvent.type != eventType:
                continue
            if nowEvent.text != tag:
                continue
            if nowEvent.attrs is None:
                if attrs:
                    continue
                return stack, nowEvent
            d = dict(nowEvent.attrs)
            for k, v in attrs.items(): 
                try:
                    nowValue = d[k]
                except KeyError:
                    break
                else:
                    if k == 'class':
                        assert nowValue is not None
                        if not set(nowValue.split(' ')).issuperset(set(v.split(' '))):
                            break
                    else:
                        if nowValue != v:
                            break
            else:
                return stack, nowEvent
    
    @contextmanager
    def seekAndEnterTag(self, tag: str, debug: bool = False, **attrs: str):
        startStack, startEvent = self.seekTag(EventType.StartTag, tag, debug=debug, **attrs)
        sentinel = len(startStack) - 1
        def f():    # to allow the above to raise StopIteration
            self.sentinels.append(sentinel)
            try:
                yield sentinel
            finally:
                if self.sentinels[-1] == sentinel:
                    while True:
                        try:
                            self.next()
                        except UnexpectedEndTag as e:
                            assert e.tag == tag, (e, tag)
                            assert e.sentinel == sentinel, (e, sentinel)
                            break
        return f()
    
    def seekData(self):
        while True:
            _, nowEvent = self.next()
            if nowEvent.type == EventType.Data:
                return nowEvent.text
    
    def seekTagAndConsumeForData(self, tag: str, debug: bool = False, **attrs: str):
        buf: tp.List[str] = []
        with self.seekAndEnterTag(tag, debug, **attrs) as sentinel:
            while True:
                try:
                    data = self.seekData().strip()
                except UnexpectedEndTag as e:
                    assert e.sentinel == sentinel, (e, sentinel)
                    break
                if data:
                    buf.append(data)
        return buf
    
    def next(self, debug: bool = False):
        stack, event = next(self.iterEvents)
        if len(stack) <= self.sentinels[-1]:
            assert event.type == EventType.EndTag, event
            sentinel = self.sentinels.pop()
            raise UnexpectedEndTag(event.text, sentinel)
        if debug:
            print('   ', len(stack), event)
        return stack, event
