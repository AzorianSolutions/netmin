

class NetminAttributeContainer:
    _attributes: dict = None

    def __init__(self, attributes: list | tuple | None = None):
        self._attributes = {}

        if isinstance(attributes, list | tuple):
            for attribute in attributes:
                if attribute[0] not in self._attributes:
                    self._attributes[attribute[0]] = []
                self._attributes[attribute[0]].append(attribute[1])

    def all(self) -> dict:
        return self._attributes

    def json(self) -> tuple:
        attrs: list = []
        for key, value in self._attributes.items():
            for item in value:
                attrs.append((key, item))
        return tuple(attrs)

    def add(self, key: str, value: str):
        if key not in self._attributes:
            self._attributes[key] = []
        self._attributes[key].append(value)

    def add_only(self, key: str, value: str):
        self._attributes[key] = []
        self._attributes[key].append(value)

    def get(self, key: str) -> list | None:
        return self._attributes.get(key, None)

    def get_first(self, key: str) -> str | None:
        if key in self._attributes and isinstance(self._attributes[key], list) and len(self._attributes[key]):
            return self._attributes[key][0]
        return None

    def get_last(self, key: str) -> str | None:
        if key in self._attributes and isinstance(self._attributes[key], list) and len(self._attributes[key]):
            return self._attributes[key][-1]
        return None


class NetminPacket:
    config: NetminAttributeContainer = NetminAttributeContainer()
    request: NetminAttributeContainer = NetminAttributeContainer()
    reply: NetminAttributeContainer = NetminAttributeContainer()
    session_state: NetminAttributeContainer = NetminAttributeContainer()
    proxy_request: NetminAttributeContainer = NetminAttributeContainer()
    proxy_reply: NetminAttributeContainer = NetminAttributeContainer()

    def __init__(self, payload: dict = None):
        if isinstance(payload, dict):
            self.load_payload(payload)

    def load_payload(self, payload: dict):
        for key, value in payload.items():
            new_key = key.replace('-', '_')
            setattr(self, new_key, NetminAttributeContainer(value))

    def json(self) -> dict:
        payload: dict = {}

        for key in dir(self):
            if key.startswith('_'):
                continue

            if hasattr(self, key) and not hasattr(getattr(self, key), '__call__'):
                new_key = key.replace('_', '-')
                value = getattr(self, key)
                if isinstance(value, NetminAttributeContainer):
                    payload[new_key] = value.json()
                else:
                    payload[new_key] = value

        return payload

    def dumps(self) -> str:
        import json
        return json.dumps(self.json())

    @classmethod
    def loads(cls, payload: str):
        import json
        return cls(json.loads(payload))


class NetminRequest(NetminPacket):
    pass


class NetminResponse(NetminPacket):
    status: int = 7
