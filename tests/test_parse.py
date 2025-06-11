from gosynapse.parse import parse_json_stream, InitData, FiniData, PrintData


def test_parse_json_stream_simple():
    data = b'["init", {"tick": 1, "text": "t", "abstick": 2, "hash": "h", "task": "tsk"}]\n' \
           b'["node", [[["foo", "bar"]], {"iden": "id", "tags": {}, "props": {}, "tagprops": {}, "nodedata": {}, "path": {}}]]\n' \
           b'["fini", {"tock": 1, "abstock": 1, "took": 1, "count": 1}]\n'
    init, nodes, fini, prints = parse_json_stream(data)
    assert init == [InitData(tick=1, text="t", abstick=2, hash="h", task="tsk")]
    assert nodes[0].data == [["foo", "bar"]]
    assert fini == [FiniData(tock=1, abstock=1, took=1, count=1)]
    assert prints == []


def test_parse_json_stream_print():
    data = (
        b'["print", {"mesg": "hello"}]\n'
        b'["fini", {"tock": 1, "abstock": 1, "took": 1, "count": 0}]\n'
    )
    init, nodes, fini, prints = parse_json_stream(data)
    assert prints == [PrintData(mesg="hello")]
