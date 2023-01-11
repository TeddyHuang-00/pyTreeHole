def test_import():
    import treehole

    assert treehole is not None
    assert treehole.__version__ is not None
    assert treehole.__doc__ is not None
    assert treehole.TreeHoleClient is not None
    assert treehole.Hole is not None
    assert treehole.Comment is not None
