
class ElemType:
    def __init__(self, elem_type: str):
        self.elem_type = elem_type

    def is_weak_to(self, other_elem_type: 'ElemType') -> bool:
        weak_elem = get_weakness(self)
        return weak_elem == other_elem_type

    def __str__(self):
        return self.elem_type

    def __hash__(self):
        return hash(self.elem_type)

    def __eq__(self, obj):
        if not hasattr(obj, "elem_type"):
            return False
        return self.elem_type == obj.elem_type


# Types RPS
MOVER = ElemType("Mover")
DOER = ElemType("Doer")
MAKER = ElemType("Maker")


def get_weakness(type: ElemType) -> ElemType:
    return {
        DOER: MAKER,
        MOVER: DOER,
        MAKER: MAKER
    }.get(type)


if __name__ == "__main__":
    print(get_weakness(DOER))
