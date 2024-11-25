class SetForClass:
    @classmethod
    def set(cls) -> set[str]:
        keys = dir(cls)
        res = {
            getattr(cls, k)
            for k in keys
            if isinstance(k, str) and not k.startswith('__') and not k.endswith('__') and k != 'set'
        }
        return res
