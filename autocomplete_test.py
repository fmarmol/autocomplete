import pytest


from autocomplete import Node, AutoComplete


def test_add_child():
    node = Node("")
    node_child = Node("a")
    ptr_node_child = id(node_child)

    node_added = node.add_child(node_child)
    assert len(node.children) == 1
    assert "a" in node.children
    assert id(node_added) == ptr_node_child

    node_child_clone = Node("a")
    node_added = node.add_child(node_child_clone)
    assert len(node.children) == 1
    assert "a" in node.children
    assert id(node_added) == ptr_node_child


def test_set_top_world():
    node = Node("")
    node_child = Node("a")
    node.add_child(node_child)

    node.set_top_words()

    assert len(node.top_words) == 1
    assert "a" in node.top_words


def test_init_autocomplet():
    for list_of_words in (None, ["a", 1], 3.14):
        with pytest.raises(ValueError):
            AutoComplete(list_of_words)


def test_autocomplete():
    list_of_words = [
        "project runway",
        "pinterest",
        "river",
        "kayak",
        "progenex",
        "progeria",
        "pg&e",
        "project free tv",
        "bank",
        "proactive",
        "progesterone",
        "press democrat",
        "priceline",
        "pandora",
        "reprobe",
        "paypal",
    ]

    auto = AutoComplete(list_of_words)

    test_table = [
        {"prefix":"p", "thruth":["pandora", "paypal", "pg&e", "pinterest"]},
        {"prefix":"P", "thruth":["pandora", "paypal", "pg&e", "pinterest"]},
        {"prefix": "pr", "thruth": ["press democrat", "priceline", "proactive", "progenex"]},
        {"prefix": "pR", "thruth": ["press democrat", "priceline", "proactive", "progenex"]},
        {"prefix": "pro", "thruth": ["proactive", "progenex", "progeria", "progesterone"]},
        {"prefix": "PrO", "thruth": ["proactive", "progenex", "progeria", "progesterone"]},
        {"prefix": "prog", "thruth":["progenex", "progeria", "progesterone"]},

    ]

    for test_case in test_table:
        result = auto.autocomplete(test_case["prefix"])
        wanted = test_case["thruth"]
        assert result == wanted, f"Recieved:{result} instead of {wanted}"

    list_of_words = ["a", "b", "c", "d", "ab", "bc", "abcd"]
    auto = AutoComplete(list_of_words)
    assert auto.root.top_words == ["a", "ab", "abcd", "b"]

def test_autocomplete_with_wrong_arg():
    auto = AutoComplete([])
    for arg in (None, 1, object, 3.14, True):
        with pytest.raises(ValueError):
            auto.autocomplete(arg)

def test_autcomplete_with_unknown_prefix():
    auto = AutoComplete(["a", "b"])
    assert auto.autocomplete("c") == []
